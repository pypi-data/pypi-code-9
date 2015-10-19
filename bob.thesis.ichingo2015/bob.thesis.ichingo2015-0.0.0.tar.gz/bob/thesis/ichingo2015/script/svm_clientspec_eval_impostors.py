#!/usr/bin/env python
#Ivana Chingovska <ivana.chingovska@idiap.ch>
#Wed  7 Oct 17:10:00 CEST 2015

"""
This script evaluates samples using client-specific SVM machines. It generate scores for licit and spoof protocol, considering that zero-effort impostors need to be scored against each other identity
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

  parser.add_argument('inputdirs', type=str, help='Directory containing the feature vectors')

  parser.add_argument('-f', '--featname', type=str, help='Unique names of the features.')
  
  parser.add_argument('-s', '--svmdir', dest='svmdir', type=str, default='./tmp/svmmodels', help='Directory to read the client-specific SVMs')

  parser.add_argument('--gr', '--group', type=str, dest='group', default='train', help='The group of clients to evaluate (defaults to "%(default)s")', choices = ('train', 'devel', 'test'))
  
  parser.add_argument('-o', '--outdir', dest='outdir', type=str, default='./tmp/', help='Directory to write the output scores')

  parser.add_argument('--scikit', action='store_true', dest='scikit', default=False, help='If True, the SVM machine will be trained using scikit routines')

  parser.add_argument('--proba', action='store_true', dest='proba', default=False, help='If True, the output scores will be log-probabilities (valid only with scikit')

  parser.add_argument('--fold', dest='fold', type=int, default=0, help='The number of the fold of the database. If different than 0, will be set as part of the name of the input and  output file')
  parser.add_argument('--eq', '--enroll-quality', dest='enroll_quality', type=str, default=None, choices=('low', 'high', 'normal', 'laptop', 'mobile'), help='The quality for the enrolment samples of MSU-MFSD and CASIA-FASD database. The REAL samples with the specified quality are used for enrolment and will be excluded from testing and evaluation (for CASIA: low, high, normal; for MSU: laptop, mobile)', nargs='+')

  parser.add_argument('-v', '--verbose', action='store_true', dest='verbose', default=False, help='Increases this script verbosity')

  parser.add_argument('--grid', dest='grid', action='store_true', default=False, help=argparse.SUPPRESS)
  
  # The next option just returns the total number of cases we will be running
  # It can be used to set jman --array option. To avoid user confusion, this
  # option is suppressed # from the --help menu
  parser.add_argument('--grid-count', dest='grid_count', action='store_true', default=False, help=argparse.SUPPRESS)


  os.umask(002)
  #######
  # Database especific configuration
  #######
  Database.create_parser(parser, implements_any_of='video')

  args = parser.parse_args()
  
  sys.stdout.write("Client-specific SVMs of %s data...\n" % args.group)
  
  #######################
  # Loading the database objects
  #######################
  database = args.cls(args)
  
  if database.short_name() == 'replay':
    if args.group == 'train':
      process_real, process_attack = database.get_train_data()
    elif args.group == 'devel':  
      process_real, process_attack = database.get_devel_data()
    else:  
      process_real, process_attack = database.get_test_data()
  else:
    if args.group == 'train':
      process_real, process_attack = database.get_train_data(enroll_quality = args.enroll_quality)
    elif args.group == 'devel':  
      process_real, process_attack = database.get_devel_data(enroll_quality = args.enroll_quality)
    else:  
      process_real, process_attack = database.get_test_data(enroll_quality = args.enroll_quality)
  process = process_real + process_attack

  if args.grid_count:
    print len(process)
    sys.exit(0)
 
  if args.grid:
    key = int(os.environ['SGE_TASK_ID']) - 1
    if key >= len(process):
      raise RuntimeError, "Grid request for job %d on a setup with %d jobs" % \
          (key, len(process))
    process = (process[key],)
 
  # associate features with directories
  if args.featname:
    dir_assoc = {args.featname[i]:args.inputdirs[i] for i in range(len(args.featname))}
  else:
    dir_assoc = {i:args.inputdirs[i] for i in range(len(args.inputdirs))}  
  
  
  # Process each file
    
  for key, obj in enumerate(process):
    sys.stdout.write("Processing %s (%d/%d)...\n" % (obj, key, len(process)))
    featname = args.featname
    featdir = args.inputdirs

    data_info, data_orig = sm.create_full_dataset_frameinfo(featdir, (obj,)); # read the data
      
    # Read SVM and pre-processing parameters from input file

    svmdir = os.path.join(args.svmdir, args.group) # for two-class SVM
      
    #import ipdb; ipdb.set_trace()  

    if obj.is_real(): 
      match_clients = database.get_clients(args.group) # match against all clients to get real access and zero-effort impostor scores
    else:
      match_clients = (obj.get_client_id(),) # match just for the current client to get spoofing scores

    for client in match_clients:
      # read the machines and norm parameters for the match client 
      fin = bob.io.base.HDF5File(os.path.join(svmdir, 'norm-client%d.hdf5' % int(client)), 'r')
      
      fin.cd(featname)
      if fin.has_group('min-max-norm'):
        fin.cd('min-max-norm')
        norm_params = fin.get_attribute('min-max-norm')
        mins = norm_params[0,:] #mean = norm_params[0,:]
        maxs = norm_params[1,:] #std = norm_params[1,:]
        fin.cd('..')
      else:
        mins = None; maxs = None
      if fin.has_group('stdnorm'):
        fin.cd('stdnorm')
        norm_params = fin.get_attribute('stdnorm')
        mean = norm_params[0,:] #mean = norm_params[0,:]
        std = norm_params[1,:] #std = norm_params[1,:]
        fin.cd('..')
      else: mean = None; std = None   #mins = None; maxs = None  

      if fin.has_group('pca_machine'):
        fin.cd('pca_machine')
        pca_machine = bob.learn.linear.Machine(fin)
        fin.cd('..')
      else: pca_machine = None   

      svm_machine = joblib.load(os.path.join(svmdir, 'SVM-client%d.pkl' % int(client)))

      data = data_orig # refresh data before any pre-processing with the match client parameters
        
      # Do pre-processing
      if not mins is None and not maxs is None:  # normalization in the range [-1, 1] (recommended by LIBSVM)
        data = norm.norm_range(data, mins, maxs, -1, 1);

      if not mean is None and not std is None:  # standard normalziation (recommended by Scikit)
        data = norm.zeromean_unitvar_norm(data, mean, std);
      
      if not pca_machine is None: # PCA dimensionality reduction of the data
        data = pca.pcareduce(pca_machine, data)
        
      scores = svm_machine.decision_function(data)    
      
      final_score = sm.reverse_nans(data_info, (obj,), scores)
      
      if obj.is_real():
        outdir = os.path.join(args.outdir, 'licit', 'client%03d' % int(client))
        ensure_dir(outdir)
        sm.save_scores(final_score, data_info, (obj,), outdir)
        if obj.get_client_id() == client: # save the real accesses also in the spoof protocol
          outdir = os.path.join(args.outdir, 'spoof')  
          ensure_dir(outdir)
          sm.save_scores(final_score, data_info, (obj,), outdir)
      else:
        outdir = os.path.join(args.outdir, 'spoof')
        ensure_dir(outdir)
        sm.save_scores(final_score, data_info, (obj,), outdir)
    
  sys.stdout.write("Done!\n")  
    
if __name__ == "__main__":
  main()




