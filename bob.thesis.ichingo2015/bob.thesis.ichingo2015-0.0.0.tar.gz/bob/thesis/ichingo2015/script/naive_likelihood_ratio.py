#!/usr/bin/env python
#Ivana Chingovska <ivana.chingovska@idiap.ch>
#Tue 21 Apr 16:01:50 CEST 2015

"""
This script computes scores for samples based on the ratio of log-likelihood obtained using a GMM based generative model for real accesses and spoofing attacks. It utilizes already pre-computed log-likelihood scores for the two models (score directories need to be given as parameters)

The script is supposed to run on the grid and will run parametric job, where the parameter is the number of Gaussians for the attacks model. The number of Gaussians for the real model is fixed (given as argument)

IMPORTANT NOTE: This script can be used only for a single value of the number of Gaussian components i.e. only for models with single features
"""

import os, sys
import argparse
import bob.io.base
import numpy

import antispoofing

from antispoofing.utils.db import *
from antispoofing.utils.helpers import *
from antispoofing.utils.ml import *
from ..helpers import score_manipulate as sm

def main():

  parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)

  parser.add_argument('--dr', '--dirreal', dest='dirreal', type=str, default='./tmp/real', help='Base directory containing the scores obtained using real access model')  
  
  parser.add_argument('--da', '--dirattack', dest='dirattack', type=str, default='./tmp/attacks', help='Base directory containing the scores obtained using attack model')
  
  parser.add_argument('--gr', '--gauss_real', type=int, dest='gauss_real', default=1, help='The number of Gaussians for the real access model (defaults to "%(default)s")')

  parser.add_argument('--ga', '--gauss_attack', type=int, dest='gauss_attack', default=1, help='The number of Gaussians for the real access model (defaults to "%(default)s")')

  parser.add_argument('-o', '--outdir', dest='outdir', type=str, default='./tmp', help='Directory to output the calculated scores')

  parser.add_argument('--fold', dest='fold', type=int, default=0, help='The number of the fold of the database (valid for MSU-MFSD and CASIA-FASD databases). If different than 0, will be set as part of the name of output file')

  parser.add_argument('-v', '--verbose', action='store_true', dest='verbose', default=False, help='Increases this script verbosity')
 
  parser.add_argument('--grid', dest='grid', action='store_true', default=False, help=argparse.SUPPRESS)

  os.umask(002)
  
  #######
  # Database especific configuration
  #######
  Database.create_parser(parser, implements_any_of='video')

  args = parser.parse_args()
 
  sys.stdout.write("Calculate likelihood ratio...\n")   
 
  gauss_real = args.gauss_real
  if args.grid:
    gauss_attack = int(os.environ['SGE_TASK_ID']) #grid_indices[int(os.environ['SGE_TASK_ID'])] #int(os.environ['SGE_TASK_ID']) - 1
  else:
    gauss_attack = args.gauss_attack

  if args.fold == 0:
    dirreal = os.path.join(args.dirreal, 'GMM-'+str(gauss_real))
    dirattack = os.path.join(args.dirattack, 'GMM-'+str(gauss_attack))
    outdir = os.path.join(args.outdir, 'GMM-'+str(gauss_real), 'GMM-'+str(gauss_attack))
  else:
    dirreal = os.path.join(args.dirreal, 'GMM-'+str(gauss_real), str(args.fold))
    dirattack = os.path.join(args.dirattack, 'GMM-'+str(gauss_attack), str(args.fold))
    outdir = os.path.join(args.outdir, 'GMM-'+str(gauss_real), 'GMM-'+str(gauss_attack), str(args.fold))

  if not os.path.exists(dirreal) or not os.path.exists(dirattack):
    sys.stdout.write("Input directories don't exist: nothing to be done!\n")
    sys.exit(0)     
 
  if not os.listdir(dirreal) or not os.listdir(dirattack):
    sys.stdout.write("Input directories are empty: nothing to be done!\n")
    sys.exit(0)    
 
  #######################
  # Loading the database objects
  #######################
  database = args.cls(args)
  
  # Read the data to be classified
  for subset in ('train', 'devel', 'test'):
    sys.stdout.write("Processing %s data...\n" % subset)   
    if subset == 'train':
      process_real, process_attack = database.get_train_data() # contains a list of real and attack videos  
    elif subset == 'devel':
      process_real, process_attack = database.get_devel_data() # contains a list of real and attack videos  
    else:
      process_real, process_attack = database.get_test_data() # contains a list of real and attack videos  

    for group in (process_real, process_attack):
      for obj in group:
        scores_real = bob.io.base.load(os.path.expanduser(obj.make_path(dirreal, '.hdf5')))
        scores_attack = bob.io.base.load(os.path.expanduser(obj.make_path(dirattack, '.hdf5')))
        scores = 2 * (scores_real - scores_attack)
        obj.save(scores, outdir, '.hdf5') # save the scores
      
  sys.stdout.write("Done!\n")  
  
if __name__ == "__main__":
  main()




