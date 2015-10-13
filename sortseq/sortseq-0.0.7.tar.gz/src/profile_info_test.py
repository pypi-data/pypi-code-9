#!/usr/bin/env python

'''A script which accept a DataFrame with columns seqs, ct,ct_0....ct_K, and 
    returns mutual information of each position.'''
from __future__ import division
#Our standard Modules
import argparse
import numpy as np
import sys

import csv
import sortseq.nsbestimator as nsb
#Our miscellaneous functions
#This module will allow us to easily tally the letter counts at a particular position
import pandas as pd
import sortseq.utils as utils

def nsb_for_pandas(df):
    return nsb.S(df,df.sum(),len(df))

def var_for_pandas(df):
    return nsb.dS(df,df.sum(),len(df))

def main(df,start,end,dicttype):
    seq_dict,inv_dict = utils.choose_dict(dicttype)
    #Check that we have the right dictionary
    if not utils.is_seq_valid(df['seq'][0],seq_dict):
        sys.exit('Incorrect Sequence Dictionary')
    #if we have the library sequenced in bin 0, drop it from the analysis
    try:
        df.drop('ct_0',1,inplace=True)
    except:
        pass
    Lseq = len(seq_dict)
    df['seq'] = df['seq'].str.slice(start,end)
    #Find number of bins    
    nbins = 0    
    include = True
    while include:
        if 'ct_' + str(nbins) not in df.columns:
            break
        nbins = nbins + 1
    tempdf = df.copy()
    seqL = len(df['seq'][0])
    MI = np.zeros(seqL)
    MIstd = np.zeros(seqL)
    pbatch = df.sum(axis=0)
    ct = df.sum(axis=1) #total counts for each seq
    for i in range(seqL):
        #Find entries with each base at this position
        tempdf['seq'] = df['seq'].str.slice(i,i+1)
        #positions = [letlist==inv_dict[z] for z in range(Lseq)]
        bincounts = tempdf.groupby('seq').sum()
        
        baseprob = bincounts.sum(axis = 1)/bincounts.sum().sum()
        entropy = bincounts.apply(nsb_for_pandas,axis=1)
        partialent = (entropy*baseprob).sum()
        MI[i] = nsb.S(bincounts.sum(axis=0),bincounts.sum().sum(),len(bincounts.sum())) - partialent
        partialvar = bincounts.apply(var_for_pandas,axis=1)
        MIstd[i] = np.sqrt((partialvar*baseprob).sum())
	
    output_df = pd.concat([pd.Series(range(start,start + seqL)),
        pd.DataFrame(MI),pd.Series(MIstd)],axis=1)
    output_df.columns = ['pos','val_info','std_info']  
    return output_df

# Define commandline wrapper
def wrapper(args):        
    # Run funciton
    start = args.start
    end = args.end
    dicttype = args.type

    if args.i:
        df = pd.io.parsers.read_csv(args.i,delim_whitespace=True)
    else:
        df = pd.io.parsers.read_csv(sys.stdin,delim_whitespace=True)

    output_df = main(df,start,end,dicttype)
    if args.out:
        outloc = open(args.out,'w')
    else:
        outloc = sys.stdout
    output_df.to_string(outloc, index=False,col_space=10,float_format=utils.format_string)

# Connects argparse to wrapper
def add_subparser(subparsers):
    p = subparsers.add_parser('profile_info_test')
    p.add_argument('-s','--start',type=int,default=0,help ='''Position to start 
        your analyzed region''')
    p.add_argument('-i','--i',default=None,help='''Input file, otherwise input
        through the standard input.''')
    p.add_argument('-e','--end',type=int,default = None, help='''Position to end 
        your analyzed region''')
    p.add_argument('-t', '--type', choices=['dna','rna','protein'], default='dna')
    p.add_argument('-o', '--out', default=None)
    p.set_defaults(func=wrapper)
