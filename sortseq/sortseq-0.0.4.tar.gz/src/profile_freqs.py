#!/usr/bin/env python

'''A script which calculates the frequency of each base at each position.'''
from __future__ import division
#Our standard Modules
import argparse
import numpy as np
import sys

import pandas as pd
import sortseq.utils as utils



def main(df,wtseq,dicttype):
    seq_dict,inv_dict = utils.choose_dict(dicttype)
    strings = df['seq']
    try:
        ct = df['ct']
    except:
        df['ct'] = 1
        ct = df['ct']
    seqL = len(strings[0])
    mutfreq = np.zeros([seqL,len(seq_dict)])
    #Dictionary with number corresponding to each base
    wttest = []
    for i in range(seqL):
        #at this position make list of each base
        letlist = strings.str.slice(i,i+1)
        #tally the number of each
        counts = [np.sum(ct[letlist==inv_dict[q]]) for q in range(len(seq_dict))]
        wtlet = np.argmax(counts)
        wttest.append(inv_dict[wtlet])
        mutfreq[i,:] = counts
    
    if wtseq:
        assert(wtseq==wttest)
    if not utils.is_seq_valid(wttest,seq_dict):
        sys.exit('Wild type seq is invalid')
    cols = ['freq_' + str(inv_dict[q]) for q in range(len(seq_dict))]
    mf = pd.DataFrame(mutfreq,columns=cols)
    #now go from cts to frequency ratio
    mf = mf.div(mf.sum(axis=1),axis='rows')
    pos = pd.Series(range(seqL),name='pos')
    output_df = pd.concat([pos,mf],axis=1)
    
    return output_df

# Define commandline wrapper
def wrapper(args):
    
    wtseq = args.wtseq
    
    
    # Run funciton
    if args.i:
        df = pd.io.parsers.read_csv(args.i,delim_whitespace=True)
    else:
        df = pd.io.parsers.read_csv(sys.stdin,delim_whitespace=True)
    output_df = main(df,wtseq,args.type)
    
    

    if args.out:
        outloc = open(args.out,'w')
    else:
        outloc = sys.stdout
    pd.set_option('max_colwidth',int(1e8))
    output_df.to_string(
        outloc, index=False,col_space=10,float_format=utils.format_string)

# Connects argparse to wrapper
def add_subparser(subparsers):
    p = subparsers.add_parser('profile_freqs')
    p.add_argument(
        '-b','--bin',default=None,help='''Bin where mutation rate will
        be measured. If left blank, total mutation rate will be measured.''')
    p.add_argument(
        '-i', '--i', default=None,help='''Input file, otherwise input
        through the standard input.''')
    p.add_argument('-w','--wtseq',default=None,help ='Wild Type Sequence')
    p.add_argument(
        '-t', '--type', choices=['dna','rna','protein'], default='dna')
    p.add_argument('-o', '--out', default=None)
    p.set_defaults(func=wrapper)
