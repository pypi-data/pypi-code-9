#!/usr/bin/env python
#Ivana Chingovska <ivana.chingovska@idiap.ch>
#Wed Jul  9 18:08:27 CEST 2014
"""
This script sorts cohort clients for each enrolled client by the similarity between their models and the models of the clients. Afterwards, it writes down the sorted cohorts order in a file. 
The sorting is performed by a criteria defined in "Speaker verification and Identification Using GMM" - D. Reynolds (Sec.3.3.2; Eq.9)
"""

import os, sys
import argparse
import bob.learn.linear
import bob.learn.em
import bob.io.base
import numpy

from antispoofing.utils.db import *
from antispoofing.utils.helpers import *
from antispoofing.utils.ml import *
from ..helpers import score_manipulate as sm
from ..helpers import gmm_operations as gmmo

  


def main():

  parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)

  parser.add_argument('inputdirs', type=str, help='Directory containing the feature vectors. Several directories corresponding to different *independent* features can be given', nargs='*')

  parser.add_argument('-f', '--featname', type=str, help='Unique names of the *independent* features. The order of stating those should be the same as for the inputdirs parameters', nargs='*')

  parser.add_argument('--mf', '--mapmodelfile', dest='mapmodelfile', type=str, default='./mapmodels.hdf5', help='File containing the real access models of all the clients')  
  
  parser.add_argument('--cf', '--cohortfile', dest='cohortfile', type=str, default='./cohortmodels.hdf5', help='File containing the attack or real access models of the cohort clients')

  parser.add_argument('--cm', '--comparemodel', dest='comparemodel', type=str, default='attack', help='Model used for comparison ("real" or "attack") (defaults to "%(default)s")')
  
  parser.add_argument('-o', '--outfile', dest='outfile', type=str, default='./tmp/sorted_cohorts.hdf5', help='Output file')

  parser.add_argument('--gr', '--group', type=str, dest='group', default='train', help='The group of data to adapt the models for (defaults to "%(default)s")', choices = ('train', 'devel', 'test'))

  parser.add_argument('-v', '--verbose', action='store_true', dest='verbose', default=False, help='Increases this script verbosity')
  
  #######
  # Database especific configuration
  #######
  Database.create_parser(parser, implements_any_of='video')

  args = parser.parse_args()
    
  sys.stdout.write("Sorting cohort models for %s data...\n" % args.group)   
  
  #######################
  # Loading the database objects
  #######################
  database = args.cls(args)
  
  # Associate features with directories
  if args.featname:
    dir_assoc = {args.featname[i]:args.inputdirs[i] for i in range(len(args.featname))}
  else:
    dir_assoc = {i:args.inputdirs[i] for i in range(len(args.inputdirs))}  
  
  
  # Read the GMMs and other parameters
  fmapmodels = bob.io.base.HDF5File(args.mapmodelfile, 'r')
  fcohort = bob.io.base.HDF5File(args.cohortfile, 'r')
  
  # Read the samples from the clients (we are interested only in the real access models)
  '''
  if args.group == 'train':
    process_clients, _ = database.get_train_data()
  elif args.group == 'devel':
    process_clients, _ = database.get_devel_data()   
  else:
    process_clients, _ = database.get_test_data()
  '''  
  process_clients = database.get_enroll_data(args.group)  
  #Read the samples of the cohorts (we are interested only in the real access models)      
  #process_cohorts, _ = database.get_train_data() # contains a list of real and attack videos
  if args.comparemodel == 'real':
    _ , process_cohorts = database.get_train_data() # contains a list of real and attack videos
  else:
    process_cohorts, _ = database.get_train_data() # contains a list of real and attack videos  
  
  # Reading the cohort models
  sys.stdout.write("Reading the cohort models parameters...\n")   
  data_read = True
  gmm_cohort_assoc = {}; norm_cohort_assoc = {}; pca_cohort_assoc = {}
  for featname in args.featname:
    if not fcohort.has_group(featname):
      data_read = False
      break  
    fcohort.cd(featname)
    if fcohort.has_group('norm'):
      fcohort.cd('norm')
      norm_cohort_assoc[featname] = fcohort.get_attribute('norm')
      fcohort.cd('..')
    if fcohort.has_group('pca_machine'):
      fcohort.cd('pca_machine')
      pca_cohort_assoc[featname] = bob.learn.linear.Machine(fcohort)
      fcohort.cd('..')
    fcohort.cd('client_models') 
    machines = {}
    available_models = fcohort.sub_groups(relative=True, recursive=False)
    for m in available_models:
      fcohort.cd(m)
      machines[m] = bob.learn.em.GMMMachine(fcohort)
      fcohort.cd('..')
    gmm_cohort_assoc[featname] = machines
    fcohort.cd('/')
    
  # Reading the clients models
  sys.stdout.write("Reading the clients models parameters...\n")   
  data_read = True
  gmm_client_assoc = {}; norm_client_assoc = {}; pca_client_assoc = {}
  for featname in args.featname:
    if not fmapmodels.has_group(featname):
      data_read = False
      break  
    fmapmodels.cd(featname)
    if fmapmodels.has_group('norm'):
      fmapmodels.cd('norm')
      norm_client_assoc[featname] = fmapmodels.get_attribute('norm')
      fmapmodels.cd('..')
    if fmapmodels.has_group('pca_machine'):
      fmapmodels.cd('pca_machine')
      pca_client_assoc[featname] = bob.learn.linear.Machine(fmapmodels)
      fmapmodels.cd('..')
    fmapmodels.cd('client_models') 
    machines = {}
    available_models = fmapmodels.sub_groups(relative=True, recursive=False)
    for m in available_models:
      fmapmodels.cd(m)
      machines[m] = bob.learn.em.GMMMachine(fmapmodels)
      fmapmodels.cd('..')
    gmm_client_assoc[featname] = machines
    fmapmodels.cd('/')  
  
  if data_read == True:
    ensure_dir(os.path.dirname(args.outfile))
    fout = bob.io.base.HDF5File(args.outfile, 'w')
  
    #import ipdb; ipdb.set_trace()
    for client in database.get_clients(args.group):
      sys.stdout.write("Processing client %s...\n" % client)   
      dist_cohort_sum = {}
      for featname, featdir in dir_assoc.items():
        dist_cohort = {}
        
        norm_client = norm_client_assoc[featname]
        pca_client = pca_client_assoc[featname]
        gmm_client = gmm_client_assoc[featname]["gmm_client_%d" % client]
        
        sub_process_client = [p for p in process_clients if p.get_client_id() == client]
        data_client_info, data_client = sm.create_full_dataset_frameinfo(featdir, sub_process_client)
                
        #for cohort_id, gmm_cohort in gmm_cohort_assoc[featname].items():
        for cohort in database.get_clients('train'):
          cohort_id = "gmm_client_%d" % cohort
          norm_cohort = norm_cohort_assoc[featname]
          pca_cohort = pca_cohort_assoc[featname]
          gmm_cohort = gmm_cohort_assoc[featname][cohort_id]
          
          sub_process_cohort = [p for p in process_cohorts if p.get_client_id() == cohort]
          data_cohort_info, data_cohort = sm.create_full_dataset_frameinfo(featdir, sub_process_cohort)
        
          score_client = 2 * (gmmo.compute_likelihood(data_client, gmm_client, norm_client, pca_client) - gmmo.compute_likelihood(data_client, gmm_cohort, norm_cohort, pca_cohort))
          score_cohort = 2 * (gmmo.compute_likelihood(data_cohort, gmm_cohort, norm_cohort, pca_cohort) - gmmo.compute_likelihood(data_cohort, gmm_client, norm_client, pca_client))
          
          dist_cohort[cohort_id] = numpy.mean(numpy.fabs(score_client)) + numpy.mean(numpy.fabs(score_cohort))
          if dist_cohort_sum.has_key(cohort_id):
            dist_cohort_sum[cohort_id] += dist_cohort[cohort_id]
          else:
            dist_cohort_sum[cohort_id] = dist_cohort[cohort_id]
            
        # write the sorted cohort models for this particular featname 
        
        sorted_cohorts = sorted(dist_cohort.items(), key=lambda x: x[1])
        if not fout.has_group(featname):
          fout.create_group(featname)
        fout.cd(featname)
        fout.create_group("gmm_client_%d" % client)
        fout.cd("gmm_client_%d" % client)
        sorted_cohort_ids = []
        for cohort_id in sorted_cohorts:
          idind = cohort_id[0].rfind('_')
          sorted_cohort_ids.append(int(cohort_id[0][idind+1:]))
        fout.set_attribute("gmm_client_%d" % client, numpy.array(sorted_cohort_ids))
        fout.cd('/')
        
      # write the sorted cohort models for the sum of all the featnames
      sorted_cohorts = sorted(dist_cohort_sum.items(), key=lambda x: x[1])
      if not fout.has_group("all"):
        fout.create_group("all")
      fout.cd("all")
      fout.create_group("gmm_client_%d" % client)
      fout.cd("gmm_client_%d" % client)
      sorted_cohort_ids = []
      for cohort_id in sorted_cohorts:
        idind = cohort_id[0].rfind('_')
        sorted_cohort_ids.append(int(cohort_id[0][idind+1:]))
      fout.set_attribute("gmm_client_%d" % client, numpy.array(sorted_cohort_ids))
      fout.cd('/')

          
    sys.stdout.write("Done!\n")  
    
  else:
    sys.stdout.write("Cohort model data are not available! No error is raised, but also no output is generated!\n")           
  
if __name__ == "__main__":
  main()




