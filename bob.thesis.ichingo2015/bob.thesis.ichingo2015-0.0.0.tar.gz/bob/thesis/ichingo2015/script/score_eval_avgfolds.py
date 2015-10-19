#!/usr/bin/env python
#Ivana Chingovska <ivana.chingovska@idiap.ch>
#Fri 17 Apr 15:38:58 CEST 2015

"""
This script will run the result analysis on all the folds of CASIA-FASD or MSU-MFSD database and will compute their average
"""

import os, sys
import argparse
import bob.measure
import numpy

from antispoofing.utils.ml import *
from antispoofing.utils.helpers import *
from antispoofing.utils.db import *
from ..helpers import *


def main():

  available_dbs = utils.get_db_names()
  db_attack_types = utils.get_db_attack_types(utils.get_db_by_name(available_dbs[1])) + utils.get_db_attack_types(utils.get_db_by_name(available_dbs[2])) # only CASIA-FASD and MSU-MFSD can be evaluated using this script

  ##########
  # General configuration
  ##########

  parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)

  parser.add_argument('--sd', '--scoresdir', type=str, dest='scoresdir', default='', help='Base directory containing the Scores of the database to be evaluated (defaults to "%(default)s")')

  parser.add_argument('-v', '--verbose', action='store_true', dest='verbose', default=False, help='Increases this script verbosity')

  parser.add_argument('-d', '--dataset', type=str, dest='dataset', default=available_dbs[1], choices=available_dbs, help='The database to be evaluated')
  
  parser.add_argument('-o', '--outfile', dest='outfile', type=str, default=None, help='Output file to write the results')
  
  parser.add_argument('--ad', '--attack-devel', type=str, dest='attack_devel', default='', choices=db_attack_types, nargs='+', help='The types of attacks to be used in the development stage (for CASIA: cut, warped, video; for MSU: video_hd, video_mobile, print)')

  parser.add_argument('--at', '--attack-test', type=str, dest='attack_test', default='', choices=db_attack_types, nargs='+', help='The types of attacks to be used in the test stage (for CASIA: cut, warped, video; for MSU: video_hd, video_mobile, print)')
  
  parser.add_argument('--qd', '--quality-devel', type=str, dest='quality_devel', default='', choices=('laptop', 'mobile', 'low', 'normal', 'high'), nargs='+', help='The quality of the samples to be used in the development stage (for CASIA: low, normal, high; for MSU: laptop, mobile)')

  parser.add_argument('--qt', '--quality-test', type=str, dest='quality_test', default='', choices=('laptop', 'mobile', 'low', 'normal', 'high'), nargs='+', help='The quality of the samples to be used in the development stage (for CASIA: low, normal, high; for MSU: laptop, mobile)')

  parser.add_argument('-f', '--numfolds', type=int, dest='number_of_folds', default=5, help='The number of folds defined for this database (defaults to "%(default)s")')
  
  parser.add_argument('--eq', '--enroll-quality', dest='enroll_quality', type=str, default=None, choices=('low', 'high', 'normal', 'laptop', 'mobile'), help='The quality for the enrolment samples of MSU-MFSD and CASIA-FASD database. The REAL samples with the specified quality are used for enrolment and therefore will be excluded from evaluation (for CASIA: low, high, normal; for MSU: laptop, mobile)', nargs='+')

  parser.add_argument('--si', '--score-inversion', action='store_true', dest='score_inversion', default=False, help='If True, scores will be inverted (multiplied by -1)')
  
  args = parser.parse_args()

  os.umask(002)

  ## Parsing
  scoresDir     = args.scoresdir
  verbose            = args.verbose
    
  #Loading databases
  db = get_db_by_name(args.dataset)

  if not os.path.exists(scoresDir):
    parser.error("The input directory does not exist")

  #if not args.enroll_quality is None and (args.attack_devel != '' or args.attack_test != ''):
  #  parser.error("It is not possible to evaluate on data filtered by attack type and enroll quality at the same time")

  if args.attack_devel != '' and not set(args.attack_devel).issubset(set(utils.get_db_attack_types(db))):
    parser.error("The specified development attack type is not valid for the specified database")

  if args.attack_test != '' and not set(args.attack_test).issubset(set(utils.get_db_attack_types(db))):
    parser.error("The specified test attack type is not valid for the specified database")


  #########
  # Loading some dataset
  #########

  final_dev_far = []; final_dev_frr = []
  final_test_far = []; final_test_frr = []
  final_eer = []; final_hter = []
  final_dev_hter = []; final_test_hter = []

  for f in range(1, args.number_of_folds+1):

    if(verbose):
      print("Processing fold %d\n... " % f)


    #import ipdb; ipdb.set_trace()
    if args.attack_devel == '':
      tuneReal, tuneAttack = db.get_devel_data(fold_no=f, enroll_quality = args.enroll_quality)
    else:
      tuneReal = []; tuneAttack = []
      for at in args.attack_devel:
        r, a = db.get_filtered_devel_data('types', fold_no=f, enroll_quality = args.enroll_quality)[at]
        tuneReal += r; tuneAttack += a

      
    if args.attack_test == '':
      develReal, develAttack = db.get_devel_data(fold_no=f, enroll_quality = args.enroll_quality)
      testReal, testAttack   = db.get_test_data(fold_no=f, enroll_quality = args.enroll_quality)
    else: 
      develReal = []; develAttack = []
      testReal = []; testAttack = [] 
      for at in args.attack_test:
        rd, ad = db.get_filtered_devel_data('types', fold_no=f, enroll_quality = args.enroll_quality)[at]
        rt, at = db.get_filtered_test_data('types', fold_no=f, enroll_quality = args.enroll_quality)[at]
        develReal += rd; develAttack += ad
        testReal += rt; testAttack += at

    if args.quality_devel != '':
      tuneReal = [x for x in tuneReal if x.get_quality() in args.quality_devel]
      tuneAttack = [x for x in tuneAttack if x.get_quality() in args.quality_devel]
    if args.quality_test != '':  
      develReal = [x for x in develReal if x.get_quality() in args.quality_test]; develAttack = [x for x in develAttack if x.get_quality() in args.quality_test];
      testReal = [x for x in testReal if x.get_quality() in args.quality_test]; testAttack = [x for x in testAttack if x.get_quality() in args.quality_test]
    

    #Getting the scores

    #Tunning (dev) set D1
    realScores   = ScoreReader(tuneReal,os.path.join(scoresDir, str(f)))
    attackScores = ScoreReader(tuneAttack,os.path.join(scoresDir, str(f)))
    tune_real_scores = realScores.getScores()
    tune_attack_scores = attackScores.getScores()


    #Devel set D2
    realScores   = ScoreReader(develReal, os.path.join(scoresDir, str(f)))
    attackScores = ScoreReader(develAttack,os.path.join(scoresDir, str(f)))
    devel_real_scores = realScores.getScores()
    devel_attack_scores = attackScores.getScores()


    #Test set D2
    realScores   = ScoreReader(testReal,os.path.join(scoresDir, str(f)))
    attackScores = ScoreReader(testAttack,os.path.join(scoresDir, str(f)))
    test_real_scores = realScores.getScores()
    test_attack_scores = attackScores.getScores()

    if args.score_inversion:
      tune_real_scores = tune_real_scores * -1; tune_attack_scores = tune_attack_scores * -1
      devel_real_scores = devel_real_scores * -1; devel_attack_scores = devel_attack_scores * -1
      test_real_scores = test_real_scores * -1; test_attack_scores = test_attack_scores * -1

    #Defining threshold
    thres  = bob.measure.eer_threshold(tune_attack_scores,tune_real_scores)

    #EER on the tune set
    far,frr = bob.measure.farfrr(tune_attack_scores, tune_real_scores, thres)
    EER = 100*((far+frr)/2) #In this case far and frr are the same
    HTER = 100* ((far+frr)/2)

    #HTER on the test set
    dev_far, dev_frr = bob.measure.farfrr(devel_attack_scores, devel_real_scores, thres)
    test_far, test_frr = bob.measure.farfrr(test_attack_scores, test_real_scores, thres)
    HTER_dev = 100* ((dev_far+dev_frr)/2)
    HTER_test = 100* ((test_far+test_frr)/2)

    if args.verbose: # print the details of this fold
      print("HTER dev: %.2f%%, HTER test: %.2f%%\n" % (HTER_dev, HTER_test))
      print("Dev set: FAR: %.2f%% / FRR: %.2f%%\n" % (100*dev_far, 100*dev_frr))
      print("Test set: FAR: %.2f%% / FRR: %.2f%%\n" % (100*test_far, 100*test_frr))


    # adding the values of the error rates
    final_eer.append(EER); final_hter.append(HTER)
    final_dev_hter.append(HTER_dev); final_test_hter.append(HTER_test)
    final_dev_far.append(dev_far); final_dev_frr.append(dev_frr)
    final_test_far.append(test_far); final_test_frr.append(test_frr)

  mean_eer = numpy.mean(final_eer); mean_hter = numpy.mean(final_hter)
  mean_dev_hter = numpy.mean(final_dev_hter); mean_test_hter = numpy.mean(final_test_hter);
  mean_dev_far = numpy.mean(final_dev_far); mean_dev_frr = numpy.mean(final_dev_frr);
  mean_test_far = numpy.mean(final_test_far); mean_test_frr = numpy.mean(final_test_frr);

  std_eer = numpy.std(final_eer)
  std_dev_hter = numpy.std(final_dev_hter)
  std_test_hter = numpy.std(final_test_hter)
  std_dev_far = numpy.std(final_dev_far); std_dev_frr = numpy.std(final_dev_frr);
  std_test_far = numpy.std(final_test_far); std_test_frr = numpy.std(final_test_frr);

  if args.outfile != None:
    ensure_dir(os.path.dirname(args.outfile))
    f = open(args.outfile, 'a+')
    f.write(args.dataset + '\t' + scoresDir + '\t' + "%.2f" % (mean_hter) + '\t' + "%.2f" % (mean_test_hter) + '\n')
    f.close()

  print("Average EER in the " + args.dataset + " database: %.2f%% +- %.2f%%" % (mean_eer, std_eer) )
  print("Average HTER in dev set in the " + args.dataset + " database: %.2f%% +- %.2f%%" % (mean_dev_hter, std_dev_hter))
  print("Average HTER in test set in the " + args.dataset + " database: %.2f%% +- %.2f%%" % (mean_test_hter, std_test_hter))
  print("")
 
  if args.verbose:
    print("Details:\n")
    print("Dev set in the " + args.dataset + " database: FAR: %.2f%% +- %.f%%/  FRR: %.2f%% +- %.f%%" % (100*mean_dev_far, 100*std_dev_far, 100*mean_dev_frr, 100*std_dev_frr))
    print("Test set in the " + args.dataset + " database: FAR: %.2f%% +- %.f%% /  FRR: %.2f%% +- %.f%%" % (100*mean_test_far, 100*std_test_far, 100*mean_test_frr, 100*std_test_frr))
 
  return 0


if __name__ == "__main__":
  main()
