#!/usr/bin/env python
#Ivana Chingovska <ivana.chingovska@idiap.ch>
#Tue Jul 15 11:53:53 CEST 2014

"""
This script creates one class SVM machines for each client based on the client's real access samples, OR one-class SVM machines for the cohorts based on their attack samples
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

def main():

  parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)

  parser.add_argument('inputdirs', type=str, help='Directory containing the feature vectors. Several directories corresponding to different *independent* features can be given', nargs='*')

  parser.add_argument('-f', '--featname', type=str, help='Unique names of the *independent* features. The order of stating those should be the same as for the inputdirs parameters', nargs='*')
  
  parser.add_argument('-p', '--paramfile', dest='paramfile', type=str, default=None, help='File containing normalization and PCA reduction parameters')  
  
  parser.add_argument('-o', '--outdir', dest='outdir', type=str, default='./tmp/svmmodels', help='Directory to write the client-specific SVMs')

  parser.add_argument('--gr', '--group', type=str, dest='group', default='train', help='The group of clients to create models for (defaults to "%(default)s")', choices = ('train', 'devel', 'test'))

  parser.add_argument('--cs', '--clss', type=str, dest='clss', default='enroll', help='The class of data to adapt the models to (defaults to "%(default)s")', choices = ('real', 'attack', 'enroll'))

  parser.add_argument('--mn', '--min-max-normalize', action='store_true', dest='min_max_normalize', default=False, help='If True, will do normalization on the data between [-1, 1] before training the SVM machine')

  parser.add_argument('--sn', '--std-normalize', action='store_true', dest='std_normalize', default=False, help='If True, will do standard normalization on the data before training the SVM machine')
  
  parser.add_argument('-r', '--pca_reduction', action='store_true', dest='pca_reduction', default=False, help='If set, PCA dimensionality reduction will be performed to the data before training SVM')
  
  parser.add_argument('-e', '--energy', type=str, dest="energy", default='0.99', help='The energy which needs to be preserved after the dimensionality reduction if PCA is performed prior to SVM training')

  parser.add_argument('--kt', '--kernel-type', type=str, dest='kernel_type', default='RBF', help='The type of kernel to use for the SVM machine (defaults to "%(default)s")', choices = ('RBF', 'LINEAR', 'POLY', 'SIGMOID'))

  parser.add_argument('-g', '--gamma', type=float, dest='gamma', default=0.0, help='Gamma parameter for polynomial, RBF and sigmoid kernels (defaults to "%(default)s")')
  
  #parser.add_argument('-c', type=float, dest='c', default=1.0, help='C parameter for polynomial, RBF and sigmoid kernels (defaults to "%(default)s")')
  
  parser.add_argument('--degree', type=int, dest='degree', default=3, help='Degree parameter for polynomial kernel (defaults to "%(default)s")')

  parser.add_argument('--nu', type=float, dest='nu', default=0.5, help='Nu parameter for all kernels (defaults to "%(default)s")')
 
  #parser.add_argument('-w', '--weight', type=float, dest='weight', default=None, help='Weight parameter for the positive class (defaults to "%(default)s")')
  parser.add_argument('-w', '--weight', action='store_true', dest='weight', default=False, help='If True, the positive class will get a weight (as it has less samples than the negative)')
  
  parser.add_argument('--scikit', action='store_true', dest='scikit', default=False, help='If True, the SVM machine will be ltrained using scikit routines')

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
  
  sys.stdout.write("Let's train client-specific One-Class SVMs of %s data...\n" % args.group)
  
  # associate features with directories
  if args.featname:
    dir_assoc = {args.featname[i]:args.inputdirs[i] for i in range(len(args.featname))}
  else:
    dir_assoc = {i:args.inputdirs[i] for i in range(len(args.inputdirs))}  
  
  # Read the normalization and PCA parameters
  
  norm_assoc = {}
  pca_machine_assoc = {}
  scores_assoc = {}
  
  if args.paramfile != None:
    sys.stdout.write("Reading parameters from a file...\n")   
    f = bob.io.base.HDF5File(args.paramfile, 'r')
    for featname in args.featname:
      f.cd(featname)
      if f.has_group('norm'):
        f.cd('norm')
        norm_assoc[featname] = f.get_attribute('norm')
        f.cd('..')
      if f.has_group('pca_machine'):
        f.cd('pca_machine')
        pca_machine_assoc[featname] = bob.learn.linear.Machine(f)
        f.cd('..')
      f.cd('/')
  else:
    process_train_real, process_train_attack = database.get_train_data() # get and read the training data
    
    for featname, featdir in dir_assoc.items(): 
      train_real = sm.create_full_dataset_frameinfo(featdir, process_train_real)[1]; train_attack = sm.create_full_dataset_frameinfo(featdir, process_train_attack)[1]; 
      train_data = numpy.concatenate((train_real, train_attack), axis=0)

      if args.min_max_normalize:
        mins, maxs = norm.calc_min_max(train_data)
        train_real = norm.norm_range(train_real, mins, maxs, -1, 1); train_attack = norm.norm_range(train_attack, mins, maxs, -1, 1)

      if args.std_normalize:
        print "Computing normalization parameters..."
        mean, std = norm.calc_mean_std(train_data, nonStdZero = True)
        train_real = norm.zeromean_unitvar_norm(train_real, mean, std); train_attack = norm.zeromean_unitvar_norm(train_attack, mean, std)
        norm_assoc[featname] = numpy.array([mean, std], dtype='float64') #[mins, maxs]

      if args.pca_reduction: # PCA dimensionality reduction of the data
        print "Computing PCA parameters..."
        for featname, featdir in dir_assoc.items():
          train_data = numpy.concatenate((train_real, train_attack), axis=0)
          pca_machine = pca.make_pca(train_data, float(args.energy)) # performing PCA
          pca_machine_assoc[featname] = pca_machine
  
  # Query the videos used to create the SVM machine
  if args.clss == 'enroll':
    process = database.get_enroll_data(args.group) 
  else:
    if args.group == 'train':
      process_real, process_attack = database.get_train_data() # contains a list of real and attack videos  
    elif args.group == 'devel':
      process_real, process_attack = database.get_devel_data() # contains a list of real and attack videos  
    else:
      process_real, process_attack = database.get_test_data() # contains a list of real and attack videos  
    if args.clss == 'real':
      process = process_real
    else:
      process = process_attack    
  
  # Process each client
  for client in clients:
    sys.stdout.write("Processing client %d...\n" % client)   
    for featname, featdir in dir_assoc.items():
      sys.stdout.write("Creating SVM for %s features...\n" % featname)     
      
      # Read the samples to be used for training
      client_samples = [c for c in process if c.get_client_id() == client]  # positive samples are only the enrollment samples of this client
      data_info, data = sm.create_full_dataset_frameinfo(featdir, client_samples);
    
      # Normalization of the data
      if norm_assoc.has_key(featname):
        mean = norm_assoc[featname][0]; std = norm_assoc[featname][1]
        data = norm.zeromean_unitvar_norm(data, mean, std);
        if args.min_max_normalize:
          mins = norm_assoc[featname][0]; maxs = norm_assoc[featname][1]
          data = norm.norm_range(data, mins, maxs, -1, 1);
        if args.std_normalize:
          mean = norm_assoc[featname][0]; std = norm_assoc[featname][1]
          data = norm.zeromean_unitvar_norm(data, mean, std);

      # PCA reduction of the data 
      if pca_machine_assoc.has_key(featname):
        pca_machine = pca_machine_assoc[featname]
        data = pca.pcareduce(pca_machine, data);
        
      # SVM machine is created here
      if not args.scikit: # SVM with Bob

        svm_type = 'ONE_CLASS'
        svm_trainer = bob.learn.libsvm.Trainer(machine_type=svm_type, kernel_type=args.kernel_type, probability = True)
        svm_trainer.gamma = args.gamma
        svm_trainer.degree = args.degree
        svm_trainer.nu = args.nu
        
        svm_machine = svm_trainer.train([data, None]);
      
      else: # SVM with scikit
        kernel='linear' if args.kernel_type == 'LINEAR' else 'rbf'
        svm_trainer = svm.OneClassSVM(nu=args.nu, gamma=args.gamma, kernel=kernel) #C=args.c
        svm_machine = svm_trainer.fit(data) # just the positive data is used to train        
        
      # Save the parameters and the machine for this client
      sys.stdout.write("...saving parameters...\n") 
      outdir = os.path.join(args.outdir, args.group)
      ensure_dir(outdir)
        
      if not args.scikit:
        fout = bob.io.base.HDF5File(os.path.join(outdir, 'SVM-client%d.hdf5' % (client)), 'w')
      else:
        fout = bob.io.base.HDF5File(os.path.join(outdir, 'norm-client%d.hdf5' % (client)), 'w')
      fout.create_group(featname)  
      fout.cd(featname)
      if norm_assoc.has_key(featname):
        if args.min_max_normalize:
          fout.create_group('min-max-norm')
          fout.cd('min-max-norm')
          fout.set_attribute('min-max-norm',norm_assoc[featname])
          fout.cd('..')
        if args.std_normalize:   
          fout.create_group('stdnorm')
          fout.cd('stdnorm')
          fout.set_attribute('stdnorm',norm_assoc[featname])
          fout.cd('..')
      if pca_machine_assoc.has_key(featname):
        fout.create_group('pca_machine')
        fout.cd('pca_machine')
        pca_machine_assoc[featname].save(fout)
        fout.cd('..')
      if not args.scikit:
        fout.create_group('svm_machine')
        fout.cd('svm_machine')
        svm_machine.save(fout)
        fout.cd('/')
      else:
        joblib.dump(svm_machine, os.path.join(outdir, 'SVM-client%d.pkl' % (client)))  

  sys.stdout.write("Done!\n")  
    
if __name__ == "__main__":
  main()




