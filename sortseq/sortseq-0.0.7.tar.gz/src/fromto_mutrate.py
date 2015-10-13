#!/usr/bin/env python

'''Script with find the probabilities of any one base being mutated to any other.
    This could reveal biases in the mutation rate.'''
from __future__ import division
#Our standard Modules
import argparse
import numpy as np
import sys

import pandas as pd
import sortseq.utils as utils



def main(df,dicttype):
    
    seq_dict,inv_dict = utils.choose_dict(dicttype)
    L = len(seq_dict)
    column_headers = ['ct_' + inv_dict[i] for i in range(len(seq_dict))]
    counts_arr = np.array(df[column_headers])
    wtarr = np.argmax(counts_arr,axis=1)
    mutarr = np.zeros([L,L])
    
    wt_df = []
    obs_df = []
    for z in range(L):
        #find places with correct wt base
        correctseqs = (wtarr==z)
        correctarr = df[column_headers][correctseqs]        
        mutarr[z,:] = np.sum(correctarr,axis = 0)/correctarr.sum().sum()
    mut_df = pd.DataFrame(mutarr.ravel(order='F'))
    wt_series = [inv_dict[i] for i in range(len(seq_dict))]*len(seq_dict)
    obs_series = []
    for i in range(len(seq_dict)):
        obs_series = obs_series + [inv_dict[i] for z in range(len(seq_dict))]
    output_df = pd.concat([pd.Series(wt_series),pd.Series(obs_series),mut_df],axis=1)
    output_df.columns = ['wt','obs','mut']
    return output_df

# Define commandline wrapper
def wrapper(args):
    
       
    # Run funciton
    df = pd.io.parsers.read_csv(sys.stdin,delimiter='\t')
    output_df = main(df,args.type)
    
    

    if args.out:
        outloc = open(args.out,'w')
    else:
        outloc = sys.stdout
    pd.set_option('max_colwidth',int(1e8))
    output_df.to_string(outloc, index=False,col_space=10,float_format=utils.format_string)

# Connects argparse to wrapper
def add_subparser(subparsers):
    p = subparsers.add_parser('fromto_mutrate')
    p.add_argument('-t', '--type', choices=['dna','rna','protein'], default='dna')
    p.add_argument('-o', '--out', default=None)
    p.set_defaults(func=wrapper)
