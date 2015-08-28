#!/usr/bin/env python

import pysam
import pdb
import argparse
import random

import sys
import time
import os

from numpy import sqrt,genfromtxt
from parabam.command import subset,stat

######################################################################
##
##      Estimate the mean and standard deviation
##      of insertsize for a whole gemone sequencing sample
##
##      Author: jhrf
##
######################################################################

class NoBamIndex(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class EstimationFailure(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class InsertEstimator(object):

    def __init__(self,master_path,temp_dir,verbose,proc,task_size):
        self.master_path = master_path
        self._temp_dir = temp_dir
        self._proc = proc
        self._task_size = task_size
        self._verbose = verbose

    def insert_stats_from_csv(self,stats_path):
        insert_dat = genfromtxt(stats_path,delimiter=",",names=True,dtype=("S256",float,float,float))
        sample,N,power_2,ins_sum = insert_dat.tolist()
        return(ins_sum/N , sqrt(N * power_2 - ins_sum**2) / N)

    def insert_size_of_sample(self,insert_path):

        def engine(read,constants,master):
            stats = {}

            insert_size = abs(read.template_length)

            stats["sum"] = {"result":insert_size}
            stats["power_2"] = {"result":insert_size**2}
            stats["N"] = {"result":1}

            return stats

        def get_gc_count(seq):
            return len(filter(lambda b: b == "G" or b == "C",seq))

        structures = {}
        structures["sum"] = {"data":0,"store_method":"cumu"}
        structures["power_2"] = {"data":0,"store_method":"cumu"}
        structures["N"] = {"data":0,"store_method":"cumu"}

        constants = {"get_gc":get_gc_count}

        stat_interface = stat.Interface(self._temp_dir)
        out_paths = stat_interface.run(
            input_bams= [insert_path],
            total_procs = self._proc,
            task_size = 10000,
            user_constants = constants,
            user_engine = engine,
            user_struc_blueprint = structures,
            verbose=self._verbose,
            keep_in_temp=True)
        
        return out_paths

class FullEstimator(InsertEstimator):

    def __init__(self,master_path,temp_dir,verbose,proc,task_size):
        super(FullEstimator,self).__init__(master_path=master_path,
            temp_dir=temp_dir,
            verbose=verbose,
            proc=proc,
            task_size=task_size)

    def estimate(self):
        verbose = self._verbose
        unique = int(time.time())
        sort_path = "%s/insert_sort_%d.bam" % (self._temp_dir,unique) 

        if verbose: print "[Status] Collecting reads from BAM file"
        proper_pair_path = self.proper_pair_subset()

        pysam.sort("-f",proper_pair_path,sort_path)
        os.rename(sort_path,proper_pair_path)
        pysam.index(proper_pair_path)
        sample_size = int(pysam.view("-c",proper_pair_path)[0])

        if verbose: print "[Status] Sample size is %d" % (sample_size,)

        if verbose: print "[Status] Finding insert size for collected reads"
        insert_stat_path = self.insert_size_of_sample(proper_pair_path)["global"][0]

        if verbose: print "[Status] Estimation complete"
    
        stats = self.insert_stats_from_csv(insert_stat_path)

        os.remove(insert_stat_path)
        os.remove(proper_pair_path)
        os.remove(proper_pair_path + ".bai")

        return stats

    def proper_pair_subset(self):
        master_object = pysam.Samfile(self.master_path,"rb")

        def engine(read,constants,master):
            if read.is_read1 and read.mapq > 58 and read.is_proper_pair:
                return True
            else:
                return False

        subset_interface = subset.Interface(self._temp_dir)
        out_file_paths = subset_interface.run([self.master_path],
            total_procs=self._proc,
            task_size=self._task_size,
            verbose=False,
            user_subsets=["insert"],
            user_constants={},
            user_engine=engine,
            keep_in_temp = True,
            ensure_unique_output=True)
        
        master_object.close()
        return( out_file_paths[self.master_path][0] )


class SubsetEstimator(InsertEstimator):

    def __init__(self,master_path,sample_size,temp_dir,region_size,verbose,proc,task_size):
        super(SubsetEstimator,self).__init__(master_path=master_path,
            temp_dir=temp_dir,
            verbose=verbose,
            proc=proc,
            task_size=task_size)

        self.sample_size = sample_size
        self._region_size = region_size

    def generate_random_region(self,master):
        master.seek(0) #ensure master is pointing to start 
        tid,chrm = random.sample(zip(range(len(master.references)),master.references),1)[0]
        length = master.lengths[tid]
        range_start,range_end = (10000,length-(self._region_size+10000))
        if range_end > 1000000:
            start = random.randint(range_start,range_end)
            end = start + self._region_size
            return "%s:%d:%d" % (chrm,start,end,)
        else:
            return ""

    def estimate(self):
        if not os.path.exists(self.master_path + '.bai'):
            raise NoBamIndex("No index file detected")

        verbose = self._verbose
        unique = int(time.time())
        superset_path = "%s/insert_est_%d.bam" % (self._temp_dir,unique) 
        sort_path = "%s/insert_sort_%d.bam" % (self._temp_dir,unique) 

        if verbose: print "[Status] Collecting reads from BAM file"
        subset_paths = self.generate_insert_subsets()
        
        if len(subset_paths) == 0:
            raise EstimationFailure("Could not estimate insert mean")

        if verbose: print "[Status] Merging read sets"
        pysam.merge(superset_path,*subset_paths)
        pysam.sort("-f",superset_path,sort_path)
        os.rename(sort_path,superset_path)
        pysam.index(superset_path)
        self.delete_files(subset_paths)

        if verbose: print "[Status] Finding insert size for collected reads"
        insert_stat_path = self.insert_size_of_sample(superset_path)["global"][0]

        if verbose: print "[Status] Estimation complete"
        os.remove(superset_path)
        
        return self.insert_stats_from_csv(insert_stat_path)

    def delete_files(self,file_paths):
        for path in file_paths:
            os.remove(path)

    def generate_insert_subsets(self):
        master_object = pysam.Samfile(self.master_path,"rb")
        limit = self.sample_size
        subset_paths = []
        reads_accumulated = 0
        subset_count = 0
        tries = 0

        def engine(read,constants,master):
            if read.is_read1 and read.mapq > 58 and read.is_proper_pair:
                return True
            else:
                return False

        while(reads_accumulated < limit):
            if tries > 499:
                return []
            elif len(subset_paths) > 249:
                #More than 249 files will crash samtools merge
                break

            random_region = self.generate_random_region(master_object)
            master_object.seek(0)

            if not random_region: continue #region generation failed. Start the loop again

            subset_count += 1
            tries += 1

            subset_interface = subset.Interface(self._temp_dir)
            return_paths = subset_interface.run([self.master_path],
                total_procs=self._proc,
                task_size=self._task_size,
                verbose=False,
                user_subsets=["insert"],
                user_constants={},
                user_engine=engine,
                fetch_region = random_region,
                keep_in_temp = True,
                ensure_unique_output=True)

            out_file_path = return_paths[self.master_path][0]

            reads_from_run = int(pysam.view("-c",out_file_path)[0])
            reads_accumulated += reads_from_run
            if self._verbose: sys.stdout.write("\r[Status] Collecting Reads: %d" % (reads_accumulated,))

            if reads_from_run > 0:
                subset_paths.append(out_file_path)
            else:
                os.remove(out_file_path)
        if self._verbose:
            sys.stdout.write("\n") 
        master_object.close()
        return( subset_paths )

def run_estimation_subset(master_path,proc,task_size=250000,sample_size=750000,
                          temp_dir="./",region_size=1000000,verbose=False):
    estimator = SubsetEstimator(master_path,sample_size,temp_dir,region_size,verbose,proc,task_size)
    return estimator.estimate()

def run_estimation_full(master_path,proc,task_size=25000,temp_dir="./",verbose=False):
    estimator = FullEstimator(master_path,temp_dir,verbose,proc,task_size)
    return estimator.estimate()

#  COMMAND LINE HANDLING: IN THE EVENT THIS PROGRAM 
#  IS RUN FROM THE CMD LINE INSTALISE THE FOLLOWING
#  PARAMETERS AND INSTALISE THE CLASSES AS FOLLOWS
if __name__ == "__main__":
    #print run_estimation_full(sys.argv[1], 16,verbose=True)
    print "Type telomerecat into your terminal for more details"

