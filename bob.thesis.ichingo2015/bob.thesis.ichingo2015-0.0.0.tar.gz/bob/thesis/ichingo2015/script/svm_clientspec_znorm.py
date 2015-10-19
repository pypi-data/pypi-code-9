#!/usr/bin/env python
#Ivana Chingovska <ivana.chingovska@idiap.ch>
#Fri May 23 15:00:22 CEST 2014

"""
This script performs z-score normalization for files given the scores of the cohort samples.
If joining of the scores is needed, it is assumed that they are log-likelihoods and thus will be joined by subtraction.

WARNING: At the moment, this script can be used only with single features (not with combinations of features)
"""

import os, sys
import argparse
import bob.io.base
import bob.learn.em
import numpy

import antispoofing

from antispoofing.utils.db import *
from antispoofing.utils.helpers import *
from antispoofing.utils.ml import *
from ..helpers import score_manipulate as sm


def main():

  parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)

  parser.add_argument('inputdir', type=str, help='Directory containing the scores to be normalized.')

  parser.add_argument('-z', '--zprobedir', dest='zprobedir', type=str, default='./tmp/', help='Directory containing the files with scores of the Z probes (attack samples of the cohorts) with regards to the client models')  
  
  parser.add_argument('-o', '--outdir', dest='outdir', type=str, default='./tmp', help='Output directory for the normalized scores')
  
  parser.add_argument('--gr', '--group', type=str, dest='group', default='train', help='The group of clients (models) to compute the likelihood for (defaults to "%(default)s")', choices = ('train', 'devel', 'test'))

  parser.add_argument('-j', '--joinlevel', type=str, dest='joinlevel', default='nojoin', help='If more then 1 score is given per sample (i.e. the score array is 2 dimensional), determines when and how to join the multiple scores (defaults to "%(default)s"). This can happen, for example, if we have class probabilities as scores. "nojoin" means that the multiple scores will be saved separately after normalization. "probajoin" means the multiple scores will be joined before normalization. "scorejoin" means they will be joined after they are separately normalized. "doublejoin" means that both "probajoin" and "scorejoin" will be performed. "singledim" means that no join is performed, by only the first score dimension will be normalized and saved', choices = ('nojoin', 'probajoin', 'scorejoin', 'doublejoin', "singledim"))

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
  
  sys.stdout.write("Normalizing scores for %s data...\n" % args.group)   
  ensure_dir(args.outdir)
  
  # Querying for the files to be evaluated
  if args.group == 'train':
    process_real, process_attack = database.get_train_data() # contains a list of real and attack videos
  elif args.group == 'devel':
    process_real, process_attack = database.get_devel_data() # contains a list of real and attack videos   
  else:
    process_real, process_attack = database.get_test_data() # contains a list of real and attack videos
  process = process_real + process_attack
  
  ensure_dir(args.outdir)
  
  # Compute z-scores for the samples for each client separately
  for client in clients:
    sys.stdout.write("Processing data for client %d...\n" % client)
    
    #import ipdb; ipdb.set_trace()
    # Read the scores that need to be normalized   
    client_obj = [c for c in process if c.get_client_id() == client]  
    scores_info, scores = sm.create_full_dataset_frameinfo(args.inputdir, client_obj) 
  
    # Read the scores of the Z probes with regards to the client models
    fznormfile = bob.io.base.HDF5File(os.path.join(args.zprobedir, "zprobes_client_%d.hdf5" % client), 'r')
    zprobe_scores = fznormfile.read('zprobe_scores')
    
    if (args.joinlevel == 'probajoin' or args.joinlevel == 'doublejoin') and len(scores.shape) > 1:
      scores = scores[:,0] - scores[:,1] # we subtract the log-probabilities of the two classes
      zprobe_scores = zprobe_scores[:,0] - zprobe_scores[:,1]

    if args.joinlevel == "singledim" and len(scores.shape) > 1 and scores.shape[1] > 1:
      scores = scores[:,0]
      zprobe_scores = zprobe_scores[:,0]
    else:
      scores = scores.flatten()
      zprobe_scores = zprobe_scores.flatten()  

    empty = numpy.zeros(shape=(0,0), dtype=numpy.float64) # this is needed just because znorm does not work properly atm.
    if len(scores.shape) == 1:
      znorm_scores = bob.learn.em.ztnorm(numpy.reshape(scores, [1, len(scores)]), numpy.reshape(zprobe_scores, [1,len(zprobe_scores)]), empty, empty) # forced to use ztnorm, znorm is buggy
    else:
      znorm_scores = numpy.ndarray((scores.shape), dtype='float64')      
      for col in range(0,scores.shape[1]):
        znorm_scores[:,col] = bob.learn.em.ztnorm(numpy.reshape(scores[:,col], [1, scores.shape[0]]), numpy.reshape(zprobe_scores[:,col], [1, zprobe_scores.shape[0]]), empty, empty) # forced to use ztnorm, znorm is buggy

    sys.stdout.write("Saving normalized scores for client %d...\n" % client) 
    if (args.joinlevel == "scorejoin" or args.joinlevel == "doublejoin") and len(scores.shape) > 1:
      znorm_scores = znorm_scores[:,0] - znorm_scores[:,1]
      sm.save_scores(znorm_scores.flatten(), scores_info, client_obj, args.outdir)
    elif args.joinlevel == "probajoin" or args.joinlevel == "nojoin":
      sm.save_scores(znorm_scores, scores_info, client_obj, args.outdir)   
    
    sm.save_scores(znorm_scores.flatten(), scores_info, client_obj, args.outdir)
  
  sys.stdout.write("Done!\n")    
  
if __name__ == "__main__":
  main()




