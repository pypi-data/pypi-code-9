#!/usr/bin/env python

'''A script which sub-samples our library.''' 
from __future__ import division
import argparse
import numpy as np
import scipy as sp
import pandas as pd
import sys

import sortseq.utils as utils





# main function for simulating library
def main(df,numsub=200,numcopies=1000,decay_constant = 100,disttype='constant'):
    
    n_seqs = len(df['seqs'])
    parr = df['ct']/np.sum(df['ct'])
    output_df = pd.DataFrame(
        np.random.choice(df['seqs'],size=numsub,p=parr),columns=['seqs'])
    
    if disttype == 'constant':
        output_df['ct'] = [numcopies for z in range(len(output_df['seqs']))]
    return output_df

    


# Define commandline wrapper
def wrapper(args):
    disttype = args.disttype
    numsub = args.numsub
    numcopies = args.numcopies
    decayconstant = args.decayconstant
    

    df = pd.io.parsers.read_csv(sys.stdin,delimiter='\t')
    # Run funciton
    output_df = main(
        df,numsub=200,numcopies=1000,decay_constant = 100,disttype='constant')
    
    if args.out:
        outloc = open(args.out,'w')
    else:
        outloc = sys.stdout
    pd.set_option('max_colwidth',int(1e8))
    output_df.to_string(
        outloc, index=False, columns=['seqs','ct'],col_space=10,
        float_format=utils.format_string)

# Connects argparse to wrapper
def add_subparser(subparsers):
    p = subparsers.add_parser('simulate_sublibrary')
    
    p.add_argument(
        '-d','--disttype',default='constant',
        choices = ['constant', 'exponential'],help ='''how should the number 
        of times each sequence appears be distributed?''')
    p.add_argument(
        '-ns','--numsub',type=int,default=200,help='''Number of 
        Different SubLib Sequences''')
    p.add_argument(
        '-nc','--numcopies',type=int,default=1e3,help='''Number of 
        times to measure a given sequence, if an exponential distrubtion 
        type is selected. This will be the maximum number of seqs''')
    p.add_argument(
        '-dc','--decayconstant',type=float,default=100,help='''If 
        exponential distribution is selected, the decay constant of 
        the distribution''')
    p.add_argument(
        '-t', '--type', choices=['dna','rna','protein'], default='dna')
    p.add_argument('-o', '--out', default=None)
    p.set_defaults(func=wrapper)
