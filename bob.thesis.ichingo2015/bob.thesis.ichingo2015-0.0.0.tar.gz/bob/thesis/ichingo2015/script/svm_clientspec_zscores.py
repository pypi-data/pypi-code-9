#!/usr/bin/env python
#Ivana Chingovska <ivana.chingovska@idiap.ch>
#Fri May 23 13:14:14 CEST 2014

"""
This script evaluates cohort samples using client-specific SVM machines, in order to compute the scores needed for Z-normalization

WARNING: At the moment, this script can be used only with single feature (not with combinations of features)
"""

import os, sys
import argparse
import bob.io.base
import bob.learn.linear
import bob.learn.libsvm
import numpy
from sklearn import svm
from sklearn.externals import joblib

import antispoofing

from antispoofing.utils.db import *
from antispoofing.utils.helpers import *
from antispoofing.utils.ml import *
from ..helpers import score_manipulate as sm

def svm_predict(svm_machine, data):
    labels = [svm_machine.predict_class_and_scores(x)[1][0] for x in data]
    return labels

def main():

  parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)

  parser.add_argument('inputdirs', type=str, help='Directory containing the feature vectors. Several directories corresponding to different *independent* features can be given', nargs='*')

  parser.add_argument('-f', '--featname', type=str, help='Unique names of the *independent* features. The order of stating those should be the same as for the inputdirs parameters', nargs='*')
  
  parser.add_argument('-s', '--svmdir', dest='svmdir', type=str, default='./tmp/svmmodels', help='Directory to read the client-specific SVMs')

  parser.add_argument('--gr', '--group', type=str, dest='group', default='train', help='The group of clients to create z-scores for (defaults to "%(default)s")', choices = ('train', 'devel', 'test'))

  parser.add_argument('--mt', '--modeltype', dest='modeltype', type=str, default='two-class', help='The type of samples that the model will be created for', choices={'real', 'two-class'})

  parser.add_argument('--scikit', action='store_true', dest='scikit', default=False, help='If True, the SVM machine will be trained using scikit routines')

  parser.add_argument('--proba', action='store_true', dest='proba', default=False, help='If True, the output scores will be log-probabilities (valid only with scikit')

  parser.add_argument('-d', '--divdir', dest='divdir', type=str, default=None, help='Directory with scores to be used to divide the Z probe scores with')

  parser.add_argument('-o', '--outdir', dest='outdir', type=str, default='./tmp/', help='Directory to write the output z-scores for each client')

  parser.add_argument('-v', '--verbose', action='store_true', dest='verbose', default=False, help='Increases this script verbosity')

  parser.add_argument('--grid', dest='grid', action='store_true', default=False, help=argparse.SUPPRESS)
  
  # The next option just returns the total number of cases we will be running
  # It can be used to set jman --array option. To avoid user confusion, this
  # option is suppressed # from the --help menu
  parser.add_argument('--grid-count', dest='grid_count', action='store_true', default=False, help=argparse.SUPPRESS)


  #######
  # Database especific configuration
  #######
  Database.create_parser(parser, implements_any_of='video')

  args = parser.parse_args()
  
  sys.stdout.write("Z-scores computation using SVMs for %s data...\n" % args.group)
  
  #######################
  # Loading the database objects
  #######################
  database = args.cls(args)
  clients = database.get_clients(args.group)
  
  if args.grid_count:
    print len(clients)
    sys.exit(0)
 
  if args.grid:
    key = int(os.environ['SGE_TASK_ID']) - 1
    if key >= len(clients):
      raise RuntimeError, "Grid request for job %d on a setup with %d jobs" % \
          (key, len(clients))
    clients = (clients[key],)
    
  # Querying for the Z probe files to be evaluated
  _, process_attack = database.get_train_data() # contains a list of real and attack videos
  process = process_attack # we need just the attack data in the training set
 
  # associate features with directories
  if args.featname:
    dir_assoc = {args.featname[i]:args.inputdirs[i] for i in range(len(args.featname))}
  else:
    dir_assoc = {i:args.inputdirs[i] for i in range(len(args.inputdirs))}  
  
  ensure_dir(args.outdir)
  
  # Process each client
  
  if args.divdir != None:
    data_div_info, data_div = sm.create_full_dataset_frameinfo(args.divdir, process) # scores for the likelihood to the cohort models
  
  for client in clients:
    sys.stdout.write("Processing client %d\n" % client)
    fout = bob.io.base.HDF5File(os.path.join(args.outdir,"zprobes_client_%d.hdf5" % client), 'w')
    #fout.create_group("zprobes_client_%d" % client)
    #fout.cd("zprobes_client_%d" % client)

    for featname, featdir in dir_assoc.items():
      data_info, data = sm.create_full_dataset_frameinfo(featdir, process); # read the cohort data
      
      # Read SVM and pre-processing parameters from input file
      if args.modeltype == 'real':
        svmdir = os.path.join(args.svmdir, args.group, args.modeltype)
      else:
        svmdir = os.path.join(args.svmdir, args.group)
      if not args.scikit:
        fin = bob.io.base.HDF5File(os.path.join(svmdir, 'SVM-client%d.hdf5' % (client)), 'r')    
      else:
        fin = bob.io.base.HDF5File(os.path.join(svmdir, 'norm-client%d.hdf5' % (client)), 'r')
      fin.cd(featname)
      if fin.has_group('norm'):
        fin.cd('norm')
        norm_params = fin.get_attribute('norm')
        mean = norm_params[0,:]
        std = norm_params[1,:]
        fin.cd('..')
      else: mean = None; std = None  
      if fin.has_group('pca_machine'):
        fin.cd('pca_machine')
        pca_machine = bob.learn.linear.Machine(fin)
        fin.cd('..')
      else: pca_machine = None  
      if not args.scikit:
        fin.cd('svm_machine')      
        svm_machine = bob.learn.libsvm.Machine(fin)
        fin.cd('/')
      else: 
        svm_machine = joblib.load(os.path.join(svmdir, 'SVM-client%d.pkl' % (client)))
  
      # Do pre-processing
      if mean != None and std != None:  # standard normalization
        #data = norm.norm_range(data, mins, maxs, -1, 1);
        data = norm.zeromean_unitvar_norm(data, mean, std);
  
      if pca_machine != None: # PCA dimensionality reduction of the data
        data = pca.pcareduce(pca_machine, data)
       
      if not args.scikit:
        scores = svm_predict(svm_machine, data);
      else:
        if args.proba:
          scores = svm_machine.predict_log_proba(data)
        else:
          scores = svm_machine.decision_function(data)
      
      if args.divdir != None:
        #import ipdb; ipdb.set_trace()
        scores = scores / data_div
        scores = scores *-1
      
      fout.set('zprobe_scores', scores)
    
  sys.stdout.write("Done!\n")  
    
if __name__ == "__main__":
  main()




