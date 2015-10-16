import subprocess
import sys
import textwrap
import time
import os
import glob
import platform

from shutil import copy
from numpy import genfromtxt
from itertools import izip

import parabam
import pysam
import argparse

import simulator
from estimateinsert import run_estimation_full

######################################################################
##
##      Create a length estimate given a telbam or group of telbams.
##
##      Author: jhrf
##
######################################################################

class ReadLogic(object):
    #These methods are used in various places
    #notably merecat-tools simulate and split

    def get_read_type(self,read1,read2):
        comps = map( lambda alig: alig.cigar == [(0,len(alig.seq))] , (read1,read2) )
        if all(comps):
            #Reads both completely mapped to reference are true telomere
            return "F1"
        elif any(comps):
            #One read not complete, test if it's on the telomere boundary
            return self.__check_orientation__(*self.__order_reads_by_strand__(read1,read2))
        else:
            return "F3"

    def __check_orientation__(self,pos_strand_read,neg_strand_read):
        #This function is only called when at least one read was 
        #completely mapped to the telomeric reference
        if neg_strand_read.cigar == [(0,len(neg_strand_read.seq))]:
            #Wrong end is complete! This is a TTAGGG read (originally), 
            #We know that this read originated from an ITS region or
            #malformed proximal telomere
            return "F4"
        else:
            #This read may be on the boundary, or could be the opposite
            #side of an interestitial read.
            return "F2"

    def __order_reads_by_strand__(self,read1,read2):
        #This function requires at least one mapped read
        unclassified = None
        operation = None
        ordered = []
        for read in (read1,read2):
            if read.is_unmapped:
                unclassified = read
            else:
                if read.is_reverse:
                    operation = "append"
                    ordered.append(read)
                else:
                    operation = "insert"
                    ordered.insert(0,read)
        
        if unclassified:
            if operation == "append":
                ordered.insert(0,unclassified)
            else:
                ordered.append(unclassified)

        return tuple(ordered)


class Interface(parabam.core.Interface):
    def __init__(self,temp_dir):
        super(Interface,self).__init__(temp_dir)
        self._compliments = {"A":"T","T":"A","C":"G","G":"C","N":"N"}

    def run_cmd(self,parser):
        cmd_args = parser.parse_args()
        self.run(input_paths = cmd_args.input,
            total_procs = cmd_args.p,
            task_size = cmd_args.s,
            reader_n = cmd_args.f,
            verbose = cmd_args.v,
            save_alignment = cmd_args.a,
            inserts_path=cmd_args.insert,
            output = cmd_args.out,
            announce=True)

    def run(self,input_paths,total_procs,task_size,verbose,output,reader_n,inserts_path=None,
        save_alignment=False,alig_params=None,announce=False,keep_in_temp=False):
        
        if not verbose:
            announce = False
        self.verbose = verbose
        program_name = "telomerecat telbam2length"
        self.__introduce__(program_name,announce)

        names = map(lambda b: self.__get_basename__(b),input_paths)
        names = map(lambda nm: nm.replace("_telbam",""),names)
        insert_length_generator = self.__get_insert_data__(inserts_path,input_paths,total_procs)
        
        output_csv_path = self.__create_output_file__(output)

        for sample_path,sample_name, in izip(input_paths,names):
            self.__output__("[Status] Estimating telomere length of sample: %s\n" % (sample_name))
            telref_path = self.__get_aligner_output__(sample_path,
                                  total_procs,save_alignment,
                                  alig_params,keep_in_temp)
            
            read_type_counts = self.__analyse_aligner_output__(telref_path,
                                  total_procs,task_size,reader_n,
                                  save_alignment,keep_in_temp)

            insert_mean,insert_sd = insert_length_generator.next()

            simulation_results = self.__run_simulation__(insert_mean, insert_sd,
                                                         read_type_counts,total_procs)

            read_type_counts.update(simulation_results)

            self.__write_to_csv__(read_type_counts,output_csv_path,sample_name)

            self.__output__("[Status] Estimation process completed succesfully\n\n")

        self.__goodbye__(program_name,announce)
        if keep_in_temp:
            return output_csv_path
        else:
            self.__copy_out_of_temp__([output_csv_path])
            return os.path.join(".",os.path.split(output_csv_path)[1])

    def __get_insert_data__(self,inserts_path,input_paths,total_procs):
        if inserts_path == None:
            for path in input_paths:
                self.__output__("[Status] Estimating insert length distribution\n")
                yield run_estimation_full(path,total_procs,temp_dir=self._temp_dir)
        else:
            with open(inserts_path,"r") as inserts_file:
                for line in inserts_file:
                    yield map(float,line.split(","))

    def __get_aligner_output__(self,sample_path,total_procs,save_alignment,
                                  alig_params,keep_in_temp,fastq_paths=[]):

        self.__output__("[Status] Aligning reads to telomeric reference\n")
        if not fastq_paths:
            fastq_paths = self.__bam_to_fastq__(sample_path)
        telref_path_sam = self.__get_telref_path__(sample_path,".sam")
        
        if alig_params == None:
            self.__run_telref_aligner__(telref_path_sam,fastq_paths,total_procs)         
        else:
            self.__run_telref_aligner__(telref_path_sam,fastq_paths,total_procs,alig_params)         
        
        telref_path_bam = self.__get_telref_path__(sample_path,".bam")
        self.__sam_to_bam__(telref_path_sam,telref_path_bam,sample_path)
        os.remove(telref_path_sam)

        self.__keep_files_decision__(fastq_paths,save_alignment,keep_in_temp)

        return telref_path_bam

    def __analyse_aligner_output__(self,telref_path_bam,total_procs,task_size,
                                          reader_n,save_alignment,keep_in_temp):
        self.__output__("[Status] Analysing results of alignment\n")
        read_type_counts = self.__get_read_type_counts__(telref_path_bam,
                                        task_size,
                                        total_procs,
                                        reader_n)
        self.__keep_files_decision__([telref_path_bam],save_alignment,keep_in_temp)
        return read_type_counts

    def __keep_files_decision__(self,file_paths,save_alignment,keep_in_temp):
        if save_alignment:
            if not keep_in_temp:
                self.__copy_out_of_temp__(file_paths)
        
        if not keep_in_temp:
            map(os.remove,file_paths)

    def __create_output_file__(self,output):
        if output:
            unqiue_file_ID = output
        else:
            unqiue_file_ID = "telomerecat_length_%d.csv" % (time.time(),)

        output_csv_path = os.path.join(self._temp_dir,unqiue_file_ID)
        with open(output_csv_path,"w") as total:
            header = "Sample,F1,F2a,F2b_F4,Uncertainty,Insert_mean,Insert_sd,Length\n"
            total.write(header)
        return output_csv_path

    def __output__(self,outstr):
        if self.verbose:
            sys.stdout.write(outstr)
            sys.stdout.flush()

    def __write_to_csv__(self,read_type_counts,output_csv_path,name):
        with open(output_csv_path,"a") as counts:
            counts.write("%s,%d,%d,%d,%.3f,%.3f,%.3f,%d\n" %\
                (name,
                read_type_counts["F1"],
                read_type_counts["F2a"],
                read_type_counts["F2b_F4"],
                read_type_counts["uncertainty"],
                read_type_counts["insert_mean"],
                read_type_counts["insert_sd"],
                read_type_counts["length"]))

    def __sam_to_bam__(self,sam_path,bam_path,template_path):
        sam_file = pysam.AlignmentFile(sam_path,"r")

        master = pysam.AlignmentFile(template_path,"rb")
        bam_file = pysam.AlignmentFile(bam_path,"wb",template=master)
        master.close()

        for read in sam_file.fetch(until_eof=True):
            bam_file.write(read)

        sam_file.close()
        bam_file.close()

    def __run_simulation__(self,insert_mean,insert_sd,read_type_counts,total_procs):
        self.__output__("[Status] Running simulation to estimate length\n")
        total_F2 = read_type_counts["F2a"]
        total_f1 = read_type_counts["F1"]
        read_length = read_type_counts["read_length"]

        len_mean,len_std = simulator.run_simulator_par(insert_mean,insert_sd,
                                         total_f1,total_F2,
                                          total_procs,read_length,N=16)

        return {"insert_mean":insert_mean,
                "insert_sd":insert_sd,
                "length":len_mean,
                "uncertainty":len_std}
        
    def __get_read_type_counts__(self,telref_path,task_size,total_procs,reader_n):

        def engine(reads,constants,parent):
            read_logic = constants["read_logic"]
            read_type = read_logic.get_read_type(*reads)

            readlen_max = max( [ len(read.seq) for read in reads ]  )

            return {read_type:{"result":1},
                    "readlen_max":{"result":readlen_max}}

        constants = {"read_logic":ReadLogic()}
        structures = {"F1":{"data":0,"store_method":"cumu"},
                      "F2":{"data":0,"store_method":"cumu"},
                      "F4":{"data":0,"store_method":"cumu"},
                      "F3":{"data":0,"store_method":"cumu"},
                      "readlen_max":{"data":0,"store_method":"max"}
                      }


        interface = parabam.command.stat.Interface(self._temp_dir)
        output_files = interface.run(input_bams=[telref_path],
                            total_procs = total_procs,
                            reader_n = reader_n,
                            task_size = task_size,
                            user_constants = constants,
                            user_engine = engine,
                            user_struc_blueprint = structures,
                            keep_in_temp = True,#TODO: insert csv not staying in temp
                            pair_process = True)

        return self.__parabam_results_to_dict__(output_files["global"][0])

    def __parabam_results_to_dict__(self,csv_path):
        results_array = genfromtxt(csv_path,
                                    delimiter=",",
                                    names=True,
                                    dtype=("S256",float,float,float,float,float))

        called_F2 = results_array["F2"].tolist()
        
        total_F4 = results_array["F4"].tolist()
        total_F1 = results_array["F1"].tolist()

        total_F2a = called_F2 - total_F4 #Find the F2a by removing the
                                          #probablistic amount of F2bs
                                          #For each F4 we assume an F2b thus

        total_F2b_F4 = total_F4 * 2 #Reflect the removal of F2b from F2a
                                     #by inflating the F4 count

        read_length = results_array["readlen_max"]

        return {"F1":int(total_F1),"F2b_F4":int(total_F2b_F4),
                "F2a":int(total_F2a),
                "F2a_F2b":int(called_F2),
                "read_length":read_length}

    def __copy_out_of_temp__(self,file_paths,copy_path="."):
        map(lambda fil: copy(fil,copy_path),file_paths)

    def __get_telref_path__(self,path,path_ext=".bam"):
        root,filename = os.path.split(path)
        head,ext = os.path.splitext(filename)
        head = head.replace("_telbam","")
        return os.path.join(self._temp_dir,"%s_telref%s" % (head,path_ext,))

    def __bam_read_to_fq__(self,read):
        read_num = 1 if read.is_read1 else 2
        seq = read.seq
        qual = read.qual
        if read.is_reverse:
            seq,qual = self.__flip_and_compliment__(read)
        fqStr = ("@%s/%d\n" % (read.qname,read_num) +
                "%s\n" % (seq,)+
                "+\n" + 
                "%s\n" % (qual,)
                )
        return (read_num,fqStr)

    def __flip_and_compliment__(self,read):
        seq_compliment = map(lambda base: self._compliments[base],read.seq)
        seq_compliment = "".join(seq_compliment)
        return(seq_compliment[::-1],read.qual[::-1])

    def __bam_to_fastq__(self,master_file_path):
        fastq_paths = self.__get_fastq_paths__(master_file_path,self._temp_dir)
        output_paths = [open(fastq_paths[0],"w"),open(fastq_paths[1],"w")]
        master = pysam.Samfile(master_file_path,"rb")
        
        loners = {}

        for i,alig in enumerate(master.fetch(until_eof=True)):
            if alig.qname in loners:
                if not alig.is_secondary:
                    mate = loners[alig.qname]

                    if mate.is_read1 == alig.is_read1:
                        continue

                    fastqised = map(self.__bam_read_to_fq__,(alig,mate))
                    for (read_num,read) in fastqised:
                        output_paths[read_num-1].write(read)
                        output_paths[read_num-1].flush()
                    del loners[alig.qname]
            else:
                if not alig.is_secondary:
                    loners[alig.qname] = alig

        del loners
        
        map(lambda o: o.close(),output_paths)
        return (fastq_paths)

    def __get_fastq_paths__(self,bam_path,temp_dir="."):
        template = os.path.basename(bam_path)
        template = template.replace(".bam","")
        return ["%s/%s-%d.fq" % (temp_dir,template,i+1,) for i in range(2)]

    #Here we align the fastq files against a telomeric referene
    def __run_telref_aligner__(self,tel_ref_path,fastq_paths,proc,
        parameters='--mp 14'):
        bowtie2 = self.__get_bowtie2_binary_path__()
        reference_path = self.__get_telomere_ref_path__()
        
        call_string = "%s -p %d -x %s -1 %s -2 %s -S %s" %\
            (parameters,proc,reference_path,fastq_paths[0],fastq_paths[1],tel_ref_path)
        return_code = subprocess.call([bowtie2,call_string],stderr=open(os.devnull, 'wb'))
        return return_code

    def __get_telomerecat_dir__(self):
        if hasattr(sys,"_MEIPASS"):
            #find the correct path when bundeled by pyinstaller
            return sys._MEIPASS
        else:
            return os.path.dirname(__file__)

    def __get_bowtie2_dir__(self,telomerecat_dir):
        if platform.system() == "Darwin":
            sys_tag = "macos"
        elif platform.system() == "Linux":
            sys_tag = "linux"

        bowtie_search = "bowtie2*%s*" % (sys_tag,)
        return glob.glob(os.path.join(telomerecat_dir,bowtie_search))[0]

    def __get_bowtie2_binary_path__(self):

        bowtie2_dir = self.__get_bowtie2_dir__(self.__get_telomerecat_dir__())
        return os.path.join(bowtie2_dir,"bowtie2")

    def __get_telomere_ref_path__(self):
        telomerecat_dir = self.__get_telomerecat_dir__()
        return os.path.join(telomerecat_dir,"telomere_reference","telomere.fa")

    def get_parser(self):
        parser = self.default_parser()
        parser.description = textwrap.dedent(
        '''\
        telomerecat telbam2length
        ----------------------------------------------------------------------

            The telbam2length command allows the user to genereate a telomere
            length estimate from a previously generated TELBAM file.

            Example useage:

            telomerecat telbam2length /path/to/some_telbam.bam

            This will generate a .csv file with an telomere length estimate
            for the `some_telbam.bam` file.

        ----------------------------------------------------------------------
        ''')

        parser.add_argument('input',metavar='TELBAM(S)', nargs='+',
            help="The telbam(s) that we wish to analyse")
        parser.add_argument('--out',metavar='CSV',type=str,nargs='?',default=None,
            help='Specify output path for length estimation CSV.\n'+\
                'Automatically generated if left blank [Default: None]')
        parser.add_argument('--insert',metavar='CSV',nargs='?',type=str,default=None,
            help="A file specifying the insert length mean and std for\n"+\
                 "each input sample. If not present telomerecat will\n"+\
                 "automatically estimate insert length of sample [Default: None]")
        parser.add_argument('-a',action="store_true",default=False
            ,help="Retain fastq and telref files created by analysis")
        parser.add_argument('-v',choices=[0,1,2],default=0,type=int,
            help="Verbosity. The amount of information output by the program:\n"\
            "\t0: Silent [Default]\n"\
            "\t1: Output\n"\
            "\t2: Detailed Output")

        return parser

if __name__ == "__main__":
    print "Do not run this script directly. Type `telomerecat` for help."
