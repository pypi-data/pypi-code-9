#!/usr/bin/env python

'''A Script which accepts a data frame with collumns ct_0, ct_1, tag, seq and 
    finds the standard deviation of lr by using seqs with multiple tags.'''
from __future__ import division
#Our standard Modules
import argparse
import numpy as np
import sys
import sortseq.nsbestimator as nsb
#Our miscellaneous functions
import pandas as pd
import sortseq.utils as utils
import logratio


def main(df):
    
    seqs_unique = list(set(df['seq']))
    groups = df.groupby('seq')
    L = len(seqs_unique)
    lr = np.zeros(L)
    lr_err = np.zeros(L)
    output_df = pd.DataFrame()
    #Find mean and std of each sequence
    output_df['lr'] = groups.mean()['lr']
    output_df['lr_err'] = groups.std()['lr']
    output_df.reset_index(inplace=True)
    output_df.rename(columns={'index':'seq'},inplace=True)
    return output_df

# Define commandline wrapper
def wrapper(args):        
    #Rename args
    start = args.start
    end = args.end
    dicttype = args.type
    #read dataframe from stdin
    if args.i:
        df = pd.io.parsers.read_csv(args.i,delim_whitespace=True)
    else:
        df = pd.io.parsers.read_csv(sys.stdin,delim_whitespace=True)
    output_df = main(df)

    if args.out:
        outloc = open(args.out,'w')
    else:
        outloc = sys.stdout
    pd.set_option('max_colwidth',int(1e8)) # Make sure columns are not truncated
    output_df.to_string(
        outloc, index=False,col_space=10,float_format=utils.format_string)

# Connects argparse to wrapper
def add_subparser(subparsers):
    p = subparsers.add_parser('errfromtags')
    p.add_argument(
        '-s','--start',type=int,default=0,
        help ='Position to start your analyzed region')
    p.add_argument(
        '-e','--end',type=int,default = None,
        help='Position to end your analyzed region')
    p.add_argument(
        '-w','--wtseq',default=None,help='Wild type sequence')
    p.add_argument(
        '-t', '--type', choices=['dna','rna','protein'], default='dna')
    p.add_argument(
        '-i', '--i', default=None,help='''Input file, otherwise input
        through the standard input.''')
    p.add_argument('-o', '--out', default=None)
    p.set_defaults(func=wrapper)
