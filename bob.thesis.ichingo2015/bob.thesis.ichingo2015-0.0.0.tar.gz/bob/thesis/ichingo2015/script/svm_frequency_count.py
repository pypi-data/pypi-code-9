#!/usr/bin/env python
#Ivana Chingovska <ivana.chingovska@idiap.ch>
#Tue 28 Jul 14:14:54 CEST 2015

"""
This script creates SVM machines for each client in the development set on the client's enrollment samples (as a positive class) and the cohort attack samples (as a negative class). It counts the frequency of the cohort attack samples as support vectors.

There is an option for normalizing between [-1, 1] or standard normalization prior to the SVM classification.

There is also an option for dimensionality reduction of the data prior to SVM classification.

There is an option to do weighted SVM using scikit-learn.

This file works with database folds and is specially designed for MSU-MFSD and CASIA-FASD database.

"""

import os, sys
import argparse
import bob.io.base
import bob.learn.linear
import bob.learn.libsvm
import numpy
from sklearn import svm
from sklearn.externals import joblib
from sklearn.metrics.pairwise import chi2_kernel


import antispoofing

from antispoofing.utils.db import *
from antispoofing.utils.helpers import *
from antispoofing.utils.ml import *
from ..helpers import score_manipulate as sm

def histogram_intersection_kernel(x, y):
  #kernel_map = numpy.dot(x, y.T)
  #import ipdb; ipdb.set_trace()
  kernel_map = numpy.ndarray([x.shape[0], y.shape[0]], dtype='float32')
  for i in range(x.shape[0]):
    for j in range(y.shape[0]):
      kernel_map[i,j] = numpy.sum(numpy.minimum(x[i,:],y[j,:]))
  return kernel_map

def main():

  parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)

  parser.add_argument('inputdirs', type=str, help='Directory containing the feature vectors. Several directories corresponding to different *independent* features can be given', nargs='+')

  parser.add_argument('-f', '--featname', type=str, help='Unique names of the *independent* features. The order of stating those should be the same as for the inputdirs parameters', nargs='*')
  
  parser.add_argument('-o', '--outdir', dest='outdir', type=str, default='./tmp/svmmodels', help='Directory to write the client-specific SVMs')

  parser.add_argument('--gr', '--group', type=str, dest='group', default='train', help='The group of clients to create models for (defaults to "%(default)s")', choices = ('train', 'devel', 'test'))

  parser.add_argument('--mn', '--min-max-normalize', action='store_true', dest='min_max_normalize', default=False, help='If True, will do normalization on the data between [-1, 1] before training the SVM machine')
  parser.add_argument('--sn', '--std-normalize', action='store_true', dest='std_normalize', default=False, help='If True, will do standard normalization on the data before training the SVM machine')
  
  parser.add_argument('-r', '--pca_reduction', action='store_true', dest='pca_reduction', default=False, help='If set, PCA dimensionality reduction will be performed to the data before training SVM')
  
  parser.add_argument('-e', '--energy', type=str, dest="energy", default='0.99', help='The energy which needs to be preserved after the dimensionality reduction if PCA is performed prior to SVM training')

  parser.add_argument('--kt', '--kernel-type', type=str, dest='kernel_type', default='RBF', help='The type of kernel to use for the SVM machine (defaults to "%(default)s")', choices = ('RBF', 'LINEAR', 'POLY', 'SIGMOID', 'HIST', 'CHI2'))

  parser.add_argument('-g', '--gamma', type=float, dest='gamma', default=0.0, help='Gamma parameter for polynomial, RBF and sigmoid kernels (defaults to "%(default)s")')
  
  parser.add_argument('-c', type=float, dest='c', default=1.0, help='C parameter for polynomial, RBF and sigmoid kernels (defaults to "%(default)s")')
  
  parser.add_argument('--degree', type=int, dest='degree', default=3, help='Degree parameter for polynomial kernel (defaults to "%(default)s")')

  parser.add_argument('--coef0', type=int, dest='coef0', default=1, help='Coef0 (r) parameter for polynomial kernel (defaults to "%(default)s")')

  parser.add_argument('--nu', type=float, dest='nu', default=0.5, help='Nu parameter for all kernels (defaults to "%(default)s")')
 
  #parser.add_argument('-w', '--weight', type=float, dest='weight', default=None, help='Weight parameter for the positive class (defaults to "%(default)s")')
  parser.add_argument('-w', '--weight', action='store_true', dest='weight', default=False, help='If True, the positive class will get a weight (as it has less samples than the negative)')
  
  parser.add_argument('--proba', action='store_true', dest='proba', default=False, help='If True, the machine will be trained to predict log-probabilities (valid only with scikit')

  parser.add_argument('--fold', dest='fold', type=int, default=0, help='The number of the fold of the database. If different than 0, will be set as part of the name of output file')
  parser.add_argument('--eq', '--enroll-quality', dest='enroll_quality', type=str, default=None, choices=('low', 'high', 'normal', 'laptop', 'mobile'), help='The quality for the enrolment samples of MSU-MFSD and CASIA-FASD database. The REAL samples with the specified quality will be used for enrolment and will be excluded from training (for CASIA: low, high, normal; for MSU: laptop, mobile)', nargs='+')

  parser.add_argument('-v', '--verbose', action='store_true', dest='verbose', default=False, help='Increases this script verbosity')
  
  # The next two options are relevant only when running the script on the SGE grid environment at Idiap. The first one should be used with the ./bin/jman submit command. The second returns the total number of jobs we will be running. It can be used to set jman --array option. To avoid user confusion, these options are suppressed from the --help menu
  parser.add_argument('--grid', dest='grid', action='store_true', default=False, help=argparse.SUPPRESS) 
  parser.add_argument('--grid-count', dest='grid_count', action='store_true', default=False, help=argparse.SUPPRESS)  

  os.umask(002)
  #######
  # Database especific configuration
  #######
  Database.create_parser(parser, implements_any_of='video')

  args = parser.parse_args()
  
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
  
  sys.stdout.write("Let's train client-specific SVMs of %s data...\n" % args.group)
  
  # associate features with directories
  if args.featname:
    dir_assoc = {args.featname[i]:args.inputdirs[i] for i in range(len(args.featname))}
  else:
    dir_assoc = {i:args.inputdirs[i] for i in range(len(args.inputdirs))}  
  
  # Read the normalization and PCA parameters
  
  norm_assoc = {}
  pca_machine_assoc = {}
  scores_assoc = {}
  
  process_train_real, process_train_attack = database.get_train_data() # get and read the training data #???? Do I need to remove the enrolment quality samples here?
    
  for featname, featdir in dir_assoc.items(): 
    train_real = sm.create_full_dataset_frameinfo(featdir, process_train_real)[1]; train_attack = sm.create_full_dataset_frameinfo(featdir, process_train_attack)[1]; 
    train_data = numpy.concatenate((train_real, train_attack), axis=0)

    if args.min_max_normalize:  # normalization in the range [-1, 1] (recommended by LIBSVM)
      print "Running min max normalization in range[-1, 1]..."
      mins, maxs = norm.calc_min_max(train_data)
      norm_assoc[featname] = numpy.array([mins, maxs], dtype='float64') #[mins, maxs]
      train_real = norm.norm_range(train_real, mins, maxs, -1, 1);
      train_attack = norm.norm_range(train_attack, mins, maxs, -1, 1);
    if args.std_normalize: 
      print "Running standard normalization..."  
      mean, std = norm.calc_mean_std(train_data, nonStdZero = True)
      train_real = norm.zeromean_unitvar_norm(train_real, mean, std); train_attack = norm.zeromean_unitvar_norm(train_attack, mean, std)
      norm_assoc[featname] = numpy.array([mean, std], dtype='float64') #[mins, maxs]
        
    if args.pca_reduction: # PCA dimensionality reduction of the data
      print "Computing PCA parameters..."
      train_data = numpy.concatenate((train_real, train_attack), axis=0)
      pca_machine = pca.make_pca(train_data, float(args.energy)) # performing PCA
      pca_machine_assoc[featname] = pca_machine
  
  # Query the videos used to create the SVM machine
  if database.short_name() == 'replay':
    process_positive = database.get_enroll_data(args.group)
    _, process_negative = database.get_train_data()  
  else:
    process_positive = database.get_enroll_data(args.group, enroll_quality = args.enroll_quality)
    _, process_negative = database.get_train_data(enroll_quality = args.enroll_quality)  
  
  # Set up a list to count the support vector frequencies
  negdata_info, negdata = sm.create_full_dataset_frameinfo(featdir, process_negative)
  freq_count = numpy.zeros((negdata.shape[0],), dtype='int')

  # Process each client
  for client in clients:
    sys.stdout.write("Processing client %d...\n" % int(client))   
    for featname, featdir in dir_assoc.items():
      sys.stdout.write("Creating SVM for %s features...\n" % featname)     
      
      # Read the positive and negative samples to be used
      client_positive = [c for c in process_positive if c.get_client_id() == client]  # positive samples are only the enrollment samples of this client
      posdata_info, posdata = sm.create_full_dataset_frameinfo(featdir, client_positive);
      negdata_info, negdata = sm.create_full_dataset_frameinfo(featdir, process_negative); # all the negative training samples
      #negdata = negdata[range(0,len(negdata),100),:]
    
      # Normalization of the data
      if norm_assoc.has_key(featname):
        if args.min_max_normalize:
          mins = norm_assoc[featname][0]; maxs = norm_assoc[featname][1]
          posdata = norm.norm_range(posdata, mins, maxs, -1, 1);
          negdata = norm.norm_range(negdata, mins, maxs, -1, 1);
        if args.std_normalize:
          mean = norm_assoc[featname][0]; std = norm_assoc[featname][1]
          posdata = norm.zeromean_unitvar_norm(posdata, mean, std);
          negdata = norm.zeromean_unitvar_norm(negdata, mean, std);
        
      # PCA reduction of the data 
      if pca_machine_assoc.has_key(featname):
        pca_machine = pca_machine_assoc[featname]
        posdata = pca.pcareduce(pca_machine, posdata);
        negdata = pca.pcareduce(pca_machine, negdata);     
        
      # SVM machine is created here
      
      kerneldict = {'LINEAR':'linear', 'POLY':'poly', 'RBF':'rbf', 'HIST':histogram_intersection_kernel, 'CHI2':chi2_kernel}
      kernel = kerneldict[args.kernel_type]
      alldata = numpy.concatenate((posdata, negdata), axis=0)
      alllabels = numpy.concatenate((numpy.ones(posdata.shape[0]), numpy.zeros(negdata.shape[0])))
      random_state=0 if args.proba else None

      if args.weight: # C_SVC type
        weight = negdata.shape[0] / posdata.shape[0] # the weight of the less frequent class
        svm_trainer = svm.SVC(C=args.c, gamma=args.gamma, coef0 = args.coef0, degree = args.degree, class_weight={1:weight}, kernel=kernel, probability=args.proba, random_state=random_state)
      else:
        svm_trainer = svm.SVC(C=args.c, gamma=args.gamma, coef0 = args.coef0, degree = args.degree, kernel=kernel, probability=args.proba, random_state=random_state)   
        svm_machine = svm_trainer.fit(alldata, alllabels) # both positive and negative data is used to train
      
      neg_sv_indices = svm_machine.support_[:svm_machine.n_support_[0]] # the indices of the SV from the negative class
      neg_sv_indices = neg_sv_indices - posdata.shape[0] # this way we get the indices of the SV as stored in the set of negative data (negdata)
      freq_count[neg_sv_indices] += 1  

  outdir=args.outdir
  ensure_dir(outdir)

  sorted_ind_freq = freq_count.argsort()[::-1]
  sorted_ind_freq_prunned = sorted_ind_freq[:len(freq_count[freq_count!=0])]
  
  #import ipdb; ipdb.set_trace()
  fout = bob.io.base.HDF5File(os.path.join(outdir, 'sv_freq_count.hdf5'), 'w')
  fout.set_attribute('sorted_ind_freq',sorted_ind_freq_prunned)

  sys.stdout.write("Done!\n")  
    
if __name__ == "__main__":
  main()




