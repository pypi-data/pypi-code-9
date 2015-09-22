#!/usr/bin/env python

'''A script with simulates measurements during a selction experiment over
   timepoints.''' 
from __future__ import division
import argparse
import numpy as np
import scipy as sp
import pandas as pd
import sys
import sortseq.Models as Models
import sortseq.utils as utils

def weighted_std(df):
    '''Takes in a dataframe with seqs and cts and calculates the std'''
    values = df['val']
    weights = df['ct']
    average = np.average(values, weights=weights)
    variance = np.average((values-average)**2, weights=weights)
    return (np.sqrt(variance))

def main(df,T_Counts,timepoints,beta=None):
   '''Beta is a parameter which sets how strong the selection is, if it is not
       provided we provide the below reasonable value'''
   if not beta:
       beta = 1/weighted_std(df)  
   #Sample from Poisson distribution with mean determined by energy and time
   for i in range(timepoints):
       weights = df['ct']*np.exp(beta*i*df['val'])
       df['ct_'+str(i)] = utils.sample(weights,T_Counts)	 
   return df
    


# Define commandline wrapper
def wrapper(args):
    T_Counts = args.totalcounts
    timepoints = args.timepoints
    beta = args.beta
    # Run funciton
    df = pd.io.parsers.read_csv(sys.stdin,delimiter='\t')
    header = df.columns
    output_df = main(df,T_Counts,timepoints,beta=beta)
    if args.out:
        outloc = open(args.out,'w')
    else:
        outloc = sys.stdout
    pd.set_option('max_colwidth',int(1e8))
    output_df.to_string(
        outloc, index=False,col_space=10,float_format=utils.format_string)

# Connects argparse to wrapper
def add_subparser(subparsers):
    p = subparsers.add_parser('simulate_selection')
    p.add_argument(
        '-tp','--timepoints',type=int,default=2,help='''Number of timepoints''')
    p.add_argument('-beta','--beta',default=None,help='''Selection Constant''')
    p.add_argument(
        '-C', '--totalcounts', type=int,default=1000000,help ='''
        Number of Sequencing Counts''')
    p.add_argument('-o', '--out', default=None)
    p.set_defaults(func=wrapper)
