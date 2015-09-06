#!/usr/bin/env python

'''A script with computes logratios for mpra, selex, or selection experiments.'''
from __future__ import division
#Our standard Modules
import argparse
import numpy as np
import sys
#Our miscellaneous functions
import pandas as pd
import sortseq.utils as utils



def main(df,dicttype,wtseq,start=0,end=None,pseudo=1):
    # add pseudocounts
    df['ct_0'] = df['ct_0'] + pseudo
    df['ct_1'] = df['ct_1'] + pseudo

    if not wtseq:
        wtseq = df['seq'][np.argmax(df['ct_0'])]
    seq_dict,inv_dict = utils.choose_dict(dicttype)
    # Check that we have the right dictionary
    if not utils.is_seq_valid(df['seq'][0],seq_dict):
        sys.exit('Incorrect Sequence Dictionary')
    Ldict = len(seq_dict)
    df['seq'] = df['seq'].str.slice(start,end)
    seqL = len(df['seq'][0])
    
    ratio = df['ct_1']/df['ct_0']
    normalization = float(ratio[df['seq']==wtseq])
    logratio = np.log(ratio/normalization)
    output_df = pd.DataFrame()
    output_df['lr'] = logratio
    # Remove inf values, if we have no pseudocounts
    output_df = output_df.replace([-np.inf,np.inf],np.nan)
    output_df = output_df.dropna()
    try:
        output_df['tag'] = df['tag']
    except:
        pass
    output_df['seq'] = df['seq']
    return output_df

# Define commandline wrapper
def wrapper(args):        
    # Run funciton
    start = args.start
    end = args.end
    dicttype = args.type
    wtseq = args.wtseq
    pseudo = args.pseudo

    if args.i:
        df = pd.io.parsers.read_csv(args.i,delim_whitespace=True)
    else:
        df = pd.io.parsers.read_csv(sys.stdin,delim_whitespace=True)
    
    output_df = main(df,dicttype,wtseq,start=start,end=end,pseudo=pseudo)
    if args.out:
        outloc = open(args.out,'w')
    else:
        outloc = sys.stdout
    pd.set_option('max_colwidth',int(1e8))
    output_df.to_string(
        outloc, index=False,col_space=10,float_format=utils.format_string)

# Connects argparse to wrapper
def add_subparser(subparsers):
    p = subparsers.add_parser('logratio')
    p.add_argument(
        '-s','--start',type=int,default=0,
        help ='Position to start your analyzed region')
    p.add_argument('-e','--end',type=int,default = None, 
        help='Position to end your analyzed region')
    p.add_argument(
        '-w','--wtseq',default=None,help='Wild type sequence')
    p.add_argument('--pseudo',default=1,help='Pseudo counts to add')
    p.add_argument(
        '-t', '--type', choices=['dna','rna','protein'], default='dna')
    p.add_argument(
        '-i', '--i', default=None,help='''Input file, otherwise input
        through the standard input.''')
    p.add_argument('-o', '--out', default=None)
    p.set_defaults(func=wrapper)
