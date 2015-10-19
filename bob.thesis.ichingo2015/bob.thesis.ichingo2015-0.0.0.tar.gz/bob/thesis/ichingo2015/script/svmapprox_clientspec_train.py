#!/usr/bin/env python
#Ivana Chingovska <ivana.chingovska@idiap.ch>
#Mon 13 Jul 13:53:40 CEST 2015

"""
This script creates client-specific SVM machines based on kernel approximations. It is done with scikit-learn

There is an option for normalizing between [-1, 1] or standard normalization prior to the SVM classification.

There is also an option for dimensionality reduction of the data prior to SVM classification.

This file works with database folds and is specially designed for MSU-MFSD and CASIA-FASD database.

The available approximatons are: Chi-2 using Additive Chi-2 sampler, Chi-2 using Nystrom approximation and histogram intersection using Nystrom approximation

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
import sklearn.kernel_approximation as kernel_approx
from time import time


import antispoofing

from antispoofing.utils.db import *
from antispoofing.utils.helpers import *
from antispoofing.utils.ml import *
from ..helpers import score_manipulate as sm

'''
def histogram_intersection_kernel(x, y):
  import ipdb; ipdb.set_trace()
  kernel_map = numpy.ndarray([x.shape[0], y.shape[0]], dtype='float32')
  for i in range(x.shape[0]):
    for j in range(y.shape[0]):
      kernel_map[i,j] = numpy.sum(numpy.minimum(x[i,:],y[j,:]))
  return kernel_map
'''

def histogram_intersection_kernel(x, y):
  #kernel_map = numpy.ndarray([x.shape[0], y.shape[0]], dtype='float32')
  return numpy.sum(numpy.minimum(x,y))
  

def main():

  parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)

  parser.add_argument('inputdirs', type=str, help='Directory containing the feature vectors. Several directories corresponding to different *independent* features can be given', nargs='+')

  parser.add_argument('-f', '--featname', type=str, help='Unique names of the *independent* features. The order of stating those should be the same as for the inputdirs parameters', nargs='*')
  
  parser.add_argument('-p', '--paramfile', dest='paramfile', type=str, default=None, help='File containing normalization and PCA reduction parameters')  
  
  parser.add_argument('-o', '--outdir', dest='outdir', type=str, default='./tmp/svmmodels', help='Directory to write the client-specific SVMs')

  parser.add_argument('--gr', '--group', type=str, dest='group', default='train', help='The group of clients to create models for (defaults to "%(default)s")', choices = ('train', 'devel', 'test'))

  parser.add_argument('--mn', '--min-max-normalize', action='store_true', dest='min_max_normalize', default=False, help='If True, will do normalization on the data between [-1, 1] before training the SVM machine')
  parser.add_argument('--sn', '--std-normalize', action='store_true', dest='std_normalize', default=False, help='If True, will do standard normalization on the data before training the SVM machine')
  
  parser.add_argument('-r', '--pca_reduction', action='store_true', dest='pca_reduction', default=False, help='If set, PCA dimensionality reduction will be performed to the data before training SVM')
  
  parser.add_argument('-e', '--energy', type=str, dest="energy", default='0.99', help='The energy which needs to be preserved after the dimensionality reduction if PCA is performed prior to SVM training')

  parser.add_argument('--kat', '--kernel-approx-type', type=str, dest='kernel_approx_type', default='nystrom-chi2', help='The type of kernel approximation "%(default)s")', choices = ('nystrom-chi2', 'nystrom-intersect', 'nystrom-rbf', 'chi2-additive'))
  
  parser.add_argument('-c', type=float, dest='c', default=1.0, help='C parameter for polynomial, RBF and sigmoid kernels (defaults to "%(default)s")')
  parser.add_argument('-n', type=int, dest='num_components', default=100, help='Number of components for the kernel approximatons (defaults to "%(default)s")')
 
  #parser.add_argument('-w', '--weight', type=float, dest='weight', default=None, help='Weight parameter for the positive class (defaults to "%(default)s")')
  parser.add_argument('-w', '--weight', action='store_true', dest='weight', default=False, help='If True, the positive class will get a weight (as it has less samples than the negative)')
  
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
  
  # Define the feature map
  if args.kernel_approx_type == 'chi2-additive':
    feature_map = kernel_approx.AdditiveChi2Sampler()
  elif args.kernel_approx_type == 'nystrom-chi2':
    feature_map = kernel_approx.Nystroem(kernel=chi2_kernel, random_state=1, n_components =args.num_components)
  elif args.kernel_approx_type == 'nystrom-intersect': # histogram intersection kernel
    feature_map = kernel_approx.Nystroem(kernel=histogram_intersection_kernel, random_state=1, n_components =args.num_components)
  else: #rbf kernel
    feature_map = kernel_approx.Nystroem(kernel='rbf', random_state=1, n_components =args.num_components)  

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
        
      alldata = numpy.concatenate((posdata, negdata), axis=0)       
      alllabels = numpy.concatenate((numpy.ones(posdata.shape[0]), numpy.zeros(negdata.shape[0])))
     
      #import ipdb; ipdb.set_trace()
      fit_transform_time = time()
      sys.stdout.write("Computing the kernel...\n")
      alldata_approx = feature_map.fit_transform(alldata, alllabels)
      sys.stdout.write("Fit transform time = %.2f s...\n" % (time()-fit_transform_time))

      if args.weight: # C_SVC type
        weight = negdata.shape[0] / posdata.shape[0] # the weight of the less frequent class
        svm_trainer = svm.LinearSVC(C=args.c, class_weight={1:weight})
      else:
        svm_trainer = svm.LinearSVC(C=args.c)   
      
      train_time = time()
      sys.stdout.write("Training the SVM...\n")
      svm_machine = svm_trainer.fit(alldata_approx, alllabels) # both positive and negative data is used to train
      sys.stdout.write("SVM training time = %.2f s..\n" % (time()-train_time))

      # Save the parameters and the machine for this client
      sys.stdout.write("...saving parameters...\n")
      if args.fold == 0:
        outdir = os.path.join(args.outdir, args.group)
      else:
        outdir = os.path.join(args.outdir, args.group, str(args.fold))
      ensure_dir(outdir)
  
      fout = bob.io.base.HDF5File(os.path.join(outdir, 'norm-client%d.hdf5' % int(client)), 'w')
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
      
      joblib.dump(svm_machine, os.path.join(outdir, 'SVM-client%d.pkl' % int(client)))  
      joblib.dump(feature_map, os.path.join(outdir, 'featmap-client%d.pkl' % int(client)))

  sys.stdout.write("Done!\n")  
    
if __name__ == "__main__":
  main()




