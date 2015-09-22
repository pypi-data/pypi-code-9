#!/usr/bin/env python

'''A script which tests if there is any mutual information between one base
    being mutated and another base begin mutated.'''
from __future__ import division
#Our standard Modules
import argparse
import numpy as np
import sys

import csv
#Our miscellaneous functions
import pandas as pd
import sortseq.utils as utils
from scipy import stats
import scipy as sp
import sortseq.profile_counts as profile_counts
import sortseq.nsbestimator as nsb
import sortseq.utils as utils

def entropy(entry):
    entry = np.array([entry,1 - entry])
    entropy = -np.sum(entry*np.log2(entry))
    return entropy

def mutated(seq):
    s = np.array(list(seq))
    mut = (s!= wt)
    return mut

def main(df,dicttype,start=0,end=None):
    pd.set_option('max_colwidth',int(1e8))
    df['seq'] = df['seq'].str.slice(start,end)
    print df
    seq_dict,inv_dict = utils.choose_dict(dicttype)
    col_headers = utils.get_column_headers(df)
    if 'ct' not in df.columns:
        df['ct'] = df[col_headers].sum(axis=1)
    wt = profile_counts.main(df,dicttype,return_wtseq=True)
    Lseq = len(wt)
   
    strings = df['seq']
    #Make array of bases
    mut_arr = np.zeros([len(strings),len(strings[0])])
    for z,s in enumerate(strings):
        mut_arr[z,:] = (np.array(list(s)) != wt)
    mut_df = pd.DataFrame(mut_arr)
    #calculate original entropies
    msummed = mut_df.sum(axis=0)
    original_ent_df = (msummed/len(strings)).apply(entropy)
    print original_ent_df
    MI = pd.DataFrame()
    for i in range(len(strings[0])):
        #calculate partial entropies
        grouped = mut_df.groupby(i)
        partial_mut = (grouped.sum()).divide(grouped.size(),axis=0)
        try:
            print partial_mut[[35,36]]
        except:
            pass
        partial_ent = partial_mut.applymap(entropy)
        #now multiply by occurance frequency and sum
        freq_partial_ent = (partial_ent.multiply(grouped.size(),axis=0))/len(strings)
        summed_partial_ent = freq_partial_ent.sum(axis=0)
        MI = pd.concat([MI,summed_partial_ent],axis=1)
    MI = -(MI.subtract(original_ent_df,axis=0))
    return MI

# Define commandline wrapper
def wrapper(args):    
    # Run funciton
    seqs_df = pd.io.parsers.read_csv(
                  sys.stdin,delim_whitespace=True)
    output_df = main(seqs_df,args.type,start=args.start,end=args.end)
    
    

    if args.out:
        outloc = open(args.out,'w')
    else:
        outloc = sys.stdout
    pd.set_option('max_colwidth',int(1e8))
    output_df.to_string(
        outloc, index=False,col_space=10,float_format=utils.format_string)

# Connects argparse to wrapper
def add_subparser(subparsers):
    p = subparsers.add_parser('pairwise_mutrate') 
    p.add_argument('-t', '--type', choices=['dna','rna','protein'], default='dna')
    p.add_argument('-s','--start',type=int,default=0)
    p.add_argument('-e','--end',type=int,default=None)
    p.add_argument('-w','--wtseq',default=None,help ='Wild Type Sequence')
    p.add_argument('-o', '--out', default=None)
    p.set_defaults(func=wrapper)
