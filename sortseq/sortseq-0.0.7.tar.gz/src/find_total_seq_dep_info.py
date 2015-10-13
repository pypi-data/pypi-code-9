#!/usr/bin/env python

'''A script with generates Simulated Data for a Sort Seq Experiment with a given mutation rate and wild type sequence.''' 
from __future__ import division
import argparse
import numpy as np
import sys

import sortseq.utils as utils
import pandas as pd
import sortseq.Sublib as Sublib
import sortseq.nsbestimator as nsb

def main(df,mpra):
    pd.set_option('max_colwidth',int(1e8))
    nbins = 0    
    include = True
    while include:
        if 'ct_' + str(nbins) not in df.columns:
            break
        nbins = nbins + 1
    column_headers = ['ct_' + str(z) for z in range(nbins)]
    seqs_arr = np.array(df[column_headers])
    
    pbatch = np.sum(seqs_arr,axis=1)
    totalseqs = np.sum(pbatch)
    originalent = nsb.S(pbatch,np.sum(pbatch),len(pbatch))
    partialent = 0
    V = 0
    for z in range(4):
         #partialent = partialent + np.sum(seqs_arr[z,:])/totalseqs*nsb.S(seqs_arr[z,:],np.sum(seqs_arr[z,:]),nbins)
         partialent = partialent + np.sum(seqs_arr[:,z])/totalseqs*nsb.S(seqs_arr[:,z],np.sum(seqs_arr[:,z]),len(seqs_arr[:,z]))
         V = V + np.sum(seqs_arr[z,:])/totalseqs*nsb.dS(seqs_arr[z,:],np.sum(seqs_arr[z,:]),nbins)
    MI = float(originalent - partialent)
    V = np.sqrt(float(V))
    
    
    #Determine Expression Cutoffs for bins
     
    
    return MI,np.sqrt(V)

# Define commandline wrapper
def wrapper(args):
    mpra = args.ReporterArray
    # Run funciton
    df = pd.io.parsers.read_csv(sys.stdin,delimiter='\t')
    MI,V = main(df,mpra)
    output_df = pd.DataFrame(pd.Series(MI,name='MI'))
    output_df = pd.concat([output_df, pd.Series(V,name='Var')],axis=1)
    
    output_df.columns = ['MI','std']
    
    if args.out:
        outloc = open(args.out,'w')
    else:
        outloc = sys.stdout

    output_df.to_string(outloc, index=False,col_space=10,float_format=utils.format_string)

# Connects argparse to wrapper
def add_subparser(subparsers):
    p = subparsers.add_parser('find_total_seq_dep_info')
    p.add_argument('-mpra','--ReporterArray',default=False,help='''Is the
                experiment a massively parallel reporter assay? Default=False''')
    p.add_argument('-o', '--out', default=None)
    p.set_defaults(func=wrapper)
