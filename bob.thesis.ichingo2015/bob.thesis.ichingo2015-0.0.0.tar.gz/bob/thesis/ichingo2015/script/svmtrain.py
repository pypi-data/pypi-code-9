#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
#Ivana Chingovska <ivana.chingovska@idiap.ch>
#Thu 16 Apr 14:55:06 CEST 2015

"""This script can make an two-class SVM classification of data into two categories: real accesses and spoofing attacks. 

There is an option for normalizing between [-1, 1] or standard normalization prior to the SVM classification.

There is also an option for dimensionality reduction of the data prior to SVM classification.

There is an option to do weighted SVM using scikit-learn.

The probabilities obtained with the SVM are considered as scores for the data. Firstly, the EER threshold on the development set is calculated. The, according to this EER, the FAR, FRR and HTER for the test and development set are calculated. The script outputs a text file with the performance results.

The script initially trains an SVM classifier, and if the correct flag is selected, it also does the evaluation of the data using the trained SVM. Otherwise, the SVM, as well as the normalization and PCA parameters are saved in a file and can be used later.
"""

import os, sys
import argparse
import bob.io.base
import bob.learn.libsvm
import bob.measure
import numpy
from sklearn import svm
from sklearn.externals import joblib

from antispoofing.utils.db import *
from antispoofing.utils.ml import *
from antispoofing.utils.helpers import *


def svm_predict(svm_machine, data):
  labels = [svm_machine.predict_class_and_scores(x)[1][0] for x in data]
  return labels


def main():

  basedir = os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[0])))

  INPUT_DIR = os.path.join(basedir, 'lbp_features')
  OUTPUT_DIR = os.path.join(basedir, 'res')

  parser = argparse.ArgumentParser(description=__doc__,
      formatter_class=argparse.RawDescriptionHelpFormatter)
  parser.add_argument('-i', '--input-dir', metavar='DIR', type=str, dest='inputdir', default=INPUT_DIR, help='Base directory containing the scores to be loaded')
  parser.add_argument('-o', '--output-dir', metavar='DIR', type=str, dest='outputdir', default=OUTPUT_DIR, help='Base directory that will be used to save the results.')
  parser.add_argument('--mn', '--min-max-normalize', action='store_true', dest='min_max_normalize', default=False, help='If True, will do normalization on the data between [-1, 1] before training the SVM machine')
  parser.add_argument('--sn', '--std-normalize', action='store_true', dest='std_normalize', default=False, help='If True, will do standard normalization on the data before training the SVM machine')
  parser.add_argument('-r', '--pca_reduction', action='store_true', dest='pca_reduction', default=False, help='If set, PCA dimensionality reduction will be performed to the data before training SVM')
  parser.add_argument('-e', '--energy', type=str, dest="energy", default='0.99', help='The energy which needs to be preserved after the dimensionality reduction if PCA is performed prior to SVM training')

  parser.add_argument('--kt', '--kernel-type', type=str, dest='kernel_type', default='RBF', help='The type of kernel to use for the SVM machine (defaults to "%(default)s")', choices = ('RBF', 'LINEAR', 'POLY', 'SIGMOID'))
  parser.add_argument('-g', '--gamma', type=float, dest='gamma', default=0.0, help='Gamma parameter for polynomial, RBF and sigmoid kernels (defaults to "%(default)s")')
  parser.add_argument('-c', type=float, dest='c', default=1.0, help='C parameter for polynomial, RBF and sigmoid kernels (defaults to "%(default)s")')
  parser.add_argument('--degree', type=int, dest='degree', default=3, help='Degree parameter for polynomial kernel (defaults to "%(default)s")')
  parser.add_argument('--nu', type=float, dest='nu', default=0.5, help='Nu parameter for all kernels (defaults to "%(default)s")')
 
  parser.add_argument('-w', '--weight', action='store_true', dest='weight', default=False, help='If True, the positive class will get a weight (as it has less samples than the negative)')
  
  parser.add_argument('--scikit', action='store_true', dest='scikit', default=False, help='If True, the SVM machine will be trained using scikit routines, instead of bob')

  parser.add_argument('--eval', dest='eval', action='store_true', default=False, help='If set, evaluation will be performed using the trained SVM')
  parser.add_argument('-s', '--score', dest='score', action='store_true', default=False, help='If set, the final classification scores of all the frames will be dumped in a file')
  parser.add_argument('-f', '--fold', dest='fold', type=int, default=0, help='The number of the fold of the database. If different than 0, will be set as part of the name of output file')

  os.umask(002)

  from ..helpers import score_manipulate as sm

  #######
  # Database especific configuration
  #######
  Database.create_parser(parser, implements_any_of='video')

  args = parser.parse_args()

  if not os.path.exists(args.inputdir):
    parser.error("input directory does not exist")

  energy = float(args.energy)

  print "Loading input files..."
  # loading the input files
  database = args.cls(args)
  
  process_train_real, process_train_attack = database.get_train_data()
  process_devel_real, process_devel_attack = database.get_devel_data()
  process_test_real, process_test_attack = database.get_test_data()
  
  # create the full datasets from the file data
  train_real = sm.create_full_dataset(args.inputdir, process_train_real); train_attack = sm.create_full_dataset(args.inputdir, process_train_attack); 
  devel_real = sm.create_full_dataset(args.inputdir, process_devel_real); devel_attack = sm.create_full_dataset(args.inputdir, process_devel_attack); 
  test_real = sm.create_full_dataset(args.inputdir, process_test_real); test_attack = sm.create_full_dataset(args.inputdir, process_test_attack); 

  if args.min_max_normalize:  # normalization in the range [-1, 1] (recommended by LIBSVM)
    print "Running min max normalization in range[-1, 1]..."
    train_data = numpy.concatenate((train_real, train_attack), axis=0) 
    mins, maxs = norm.calc_min_max(train_data)
    train_real = norm.norm_range(train_real, mins, maxs, -1, 1); train_attack = norm.norm_range(train_attack, mins, maxs, -1, 1)
    devel_real = norm.norm_range(devel_real, mins, maxs, -1, 1); devel_attack = norm.norm_range(devel_attack, mins, maxs, -1, 1)
    test_real = norm.norm_range(test_real, mins, maxs, -1, 1); test_attack = norm.norm_range(test_attack, mins, maxs, -1, 1)
    
  if args.std_normalize: 
    print "Running standard normalization..."
    train_data = numpy.concatenate((train_real, train_attack), axis=0) 
    mean, std = norm.calc_mean_std(train_data, nonStdZero = True)
    train_real = norm.zeromean_unitvar_norm(train_real, mean, std); train_attack = norm.zeromean_unitvar_norm(train_attack, mean, std)
    devel_real = norm.zeromean_unitvar_norm(devel_real, mean, std); devel_attack = norm.zeromean_unitvar_norm(devel_attack, mean, std)
    test_real = norm.zeromean_unitvar_norm(test_real, mean, std); test_attack = norm.zeromean_unitvar_norm(test_attack, mean, std)
  
  if args.pca_reduction: # PCA dimensionality reduction of the data
    print "Running PCA reduction..."
    train=numpy.append(train_real, train_attack, axis=0)
    pca_machine = pca.make_pca(train, energy, cov=True) # performing PCA
    train_real = pca.pcareduce(pca_machine, train_real); train_attack = pca.pcareduce(pca_machine, train_attack)
    devel_real = pca.pcareduce(pca_machine, devel_real); devel_attack = pca.pcareduce(pca_machine, devel_attack)
    test_real = pca.pcareduce(pca_machine, test_real); test_attack = pca.pcareduce(pca_machine, test_attack)

  print "Training SVM machine..."
  if not args.scikit: # SVM with Bob    
    svm_type = 'C_SVC'
    svm_trainer = bob.learn.libsvm.Trainer(svm_type=svm_type, kernel_type=args.kernel_type, gamma=args.gamma, degree=args.degree, nu=args.nu) 
    svm_trainer.probability = True  
    svm_machine = svm_trainer.train([train_real, train_attack])
  else:
    kernel='linear' if args.kernel_type == 'LINEAR' else 'rbf'  
    alldata = numpy.concatenate((train_real, train_attack), axis=0)
    alllabels = numpy.concatenate((numpy.ones(train_real.shape[0]), numpy.zeros(train_attack.shape[0])))
    if args.weight: # C_SVC type
      weight = train_attack.shape[0] / train_real.shape[0] # the weight of the less frequent class
      svm_trainer = svm.SVC(C=args.c, gamma=args.gamma, class_weight={1:weight}, kernel=kernel)
    else:
      svm_trainer = svm.SVC(C=args.c, gamma=args.gamma, kernel=kernel)  
    svm_machine = svm_trainer.fit(alldata, alllabels) # both positive and negative data is used to train

  # Saving the parameters and the machine

  sys.stdout.write("...saving parameters...\n")   
  # Setting the output file
  if args.fold == 0:
    outdir = args.outputdir
  else:
    outdir = os.path.join(args.outputdir, str(args.fold))
  ensure_dir(outdir)
        
  if not args.scikit:
    fout = bob.io.base.HDF5File(os.path.join(outdir, 'svm-machine.hdf5'), 'w')
  else: # computes using scikit-learn
    fout = bob.io.base.HDF5File(os.path.join(outdir, 'norm-params.hdf5'), 'w') # because the normalization parameters can not be saved in the same file as SVM machine with scikit

  if args.min_max_normalize: 
    fout.create_group('min-max-norm')
    fout.cd('min-max-norm')
    fout.set_attribute('mins', mins)
    fout.set_attribute('maxs', maxs)
    fout.cd('..')
  if args.std_normalize:   
    fout.create_group('stdnorm')
    fout.cd('stdnorm')
    fout.set_attribute('mean', mean)
    fout.set_attribute('std', std)
    fout.cd('..')
    
  if args.pca_reduction:  
    fout.create_group('pca_machine')
    fout.cd('pca_machine')
    pca_machine.save(fout)
    fout.cd('..')

  if not args.scikit:
    fout.create_group('svm_machine')
    fout.cd('svm_machine')
    svm_machine.save(fout)
    fout.cd('/')
  else:
    joblib.dump(svm_machine, os.path.join(outdir, 'svm-machine.pkl'))

  if args.eval:
    
    print "Computing devel and test scores..."
    if not args.scikit:
      devel_real_out = svm_predict(svm_machine, devel_real);
      devel_attack_out = svm_predict(svm_machine, devel_attack);
      test_real_out = svm_predict(svm_machine, test_real);
      test_attack_out = svm_predict(svm_machine, test_attack);
      train_real_out = svm_predict(svm_machine, train_real);
      train_attack_out = svm_predict(svm_machine, train_attack);
    else:
      devel_real_out = svm_machine.decision_function(devel_real)
      devel_attack_out = svm_machine.decision_function(devel_attack)
      test_real_out = svm_machine.decision_function(test_real)
      test_attack_out = svm_machine.decision_function(test_attack)
      train_real_out = svm_machine.decision_function(train_real)
      train_attack_out = svm_machine.decision_function(train_attack)

    # it is expected that the scores of the real accesses are always higher then the scores of the attacks. Therefore, a check is first made, if the average of the scores of real accesses is smaller then the average of the scores of the attacks, all the scores are inverted by multiplying with -1.
    if numpy.mean(devel_real_out) < numpy.mean(devel_attack_out):
      devel_real_out = devel_real_out * -1; devel_attack_out = devel_attack_out * -1
      test_real_out = test_real_out * -1; test_attack_out = test_attack_out * -1
      train_real_out = train_real_out * -1; train_attack_out = train_attack_out * -1
    

    
    score_dir = os.path.join(outdir, 'scores') # output directory for the socre files
    ensure_dir(score_dir)

    if args.score: # save the scores in a file
      sm.map_scores(args.inputdir, score_dir, process_devel_real, numpy.reshape(devel_real_out, [len(devel_real_out), 1])) 
      sm.map_scores(args.inputdir, score_dir, process_devel_attack, numpy.reshape(devel_attack_out, [len(devel_attack_out), 1]))
      sm.map_scores(args.inputdir, score_dir, process_test_real, numpy.reshape(test_real_out, [len(test_real_out), 1]))
      sm.map_scores(args.inputdir, score_dir, process_test_attack, numpy.reshape(test_attack_out, [len(test_attack_out), 1]))
      sm.map_scores(args.inputdir, score_dir, process_train_real, numpy.reshape(train_real_out, [len(train_real_out), 1]))
      sm.map_scores(args.inputdir, score_dir, process_train_attack, numpy.reshape(train_attack_out, [len(train_attack_out), 1]))
  
    thres = bob.measure.eer_threshold(devel_attack_out, devel_real_out)
    dev_far, dev_frr = bob.measure.farfrr(devel_attack_out, devel_real_out, thres)
    test_far, test_frr = bob.measure.farfrr(test_attack_out, test_real_out, thres)
  
    tbl = []
    tbl.append(" ")
    if args.pca_reduction:
      tbl.append("EER @devel - (energy kept after PCA = %.2f" % (energy))
    tbl.append(" threshold: %.4f" % thres)
    tbl.append(" dev:  FAR %.2f%% (%d / %d) | FRR %.2f%% (%d / %d) | HTER %.2f%% " % \
      (100*dev_far, int(round(dev_far*len(devel_attack))), len(devel_attack), 
       100*dev_frr, int(round(dev_frr*len(devel_real))), len(devel_real),
       50*(dev_far+dev_frr)))
    tbl.append(" test: FAR %.2f%% (%d / %d) | FRR %.2f%% (%d / %d) | HTER %.2f%% " % \
      (100*test_far, int(round(test_far*len(test_attack))), len(test_attack),
       100*test_frr, int(round(test_frr*len(test_real))), len(test_real),
       50*(test_far+test_frr)))
    txt = ''.join([k+'\n' for k in tbl])

    print txt

    # write the results to a file 
    tf = open(os.path.join(score_dir, 'perf_table.txt'), 'w')
    tf.write(txt)
 
if __name__ == '__main__':
  main()
