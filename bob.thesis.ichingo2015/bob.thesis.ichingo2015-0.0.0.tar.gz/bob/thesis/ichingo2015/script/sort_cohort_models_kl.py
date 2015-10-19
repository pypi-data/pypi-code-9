#!/usr/bin/env python
#Ivana Chingovska <ivana.chingovska@idiap.ch>
#Mon Nov 11 15:28:55 CET 2013
"""
This script sorts cohort clients for each enrolled client by the similarity between their models and the models of the clients. Afterwards, it writes down the sorted cohorts order in a file.
The sorting is performed using GMM distance measurement based on KL divergence, as defined in: "An Efficient Image Similarity Measure based on Approximations of
KL-Divergence Between Two Gaussian Mixtures" - J. Goldberger, S. Gordon, H. Greenspan (Eq. 4)
"""

import os, sys
import argparse
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

  parser.add_argument('-f', '--featname', type=str, help='Unique names of the *independent* features. The order of stating those should be the same as for the inputdirs parameters', nargs='*')

  parser.add_argument('--mf', '--mapmodelfile', dest='mapmodelfile', type=str, default='./mapmodels.hdf5', help='File containing the real access models of all the clients')  
  
  parser.add_argument('--cf', '--cohortfile', dest='cohortfile', type=str, default='./cohortmodels.hdf5', help='File containing the attack or real access models of the cohort clients')
  
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
  
  # Read the GMMs and other parameters
  fmapmodels = bob.io.base.HDF5File(args.mapmodelfile, 'r')
  fcohort = bob.io.base.HDF5File(args.cohortfile, 'r')
  
  gmm_machine_assoc = {}
  
  sys.stdout.write("Reading the cohort models parameters...\n")   
  data_read = True
  for featname in args.featname:
    if not fcohort.has_group(featname):
      data_read = False
      break  
    fcohort.cd(featname)
    fcohort.cd('client_models') 
    machines = {}
    available_models = fcohort.sub_groups(relative=True, recursive=False)
    for m in available_models:
      fcohort.cd(m)
      machines[m] = bob.learn.em.GMMMachine(fcohort)
      fcohort.cd('..')
    gmm_machine_assoc[featname] = machines
    fcohort.cd('/')
  
  if data_read == True:
    ensure_dir(os.path.dirname(args.outfile))
    fout = bob.io.base.HDF5File(args.outfile, 'w')
  
    #import ipdb; ipdb.set_trace()
    for client in database.get_clients(args.group):
      sys.stdout.write("Processing client %s...\n" % client)   
      dist_cohort_sum = {}
      for featname in args.featname:
        dist_cohort = {}
        fmapmodels.cd(featname)
        fmapmodels.cd('client_models')  
        fmapmodels.cd("gmm_client_%d" % client) # get the model for this client 
        client_machine = bob.learn.em.GMMMachine(fmapmodels)
        
        for cohort_id, cohort_machine in gmm_machine_assoc[featname].items():
          sys.stdout.write("Cohort %s...\n" % cohort_id)  
          dist_cohort[cohort_id] = gmmo.gmm_distance(client_machine, cohort_machine)
          if dist_cohort_sum.has_key(cohort_id):
            dist_cohort_sum[cohort_id] += dist_cohort[cohort_id]
          else:
            dist_cohort_sum[cohort_id] = dist_cohort[cohort_id]
            
        fmapmodels.cd('/')
        
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




