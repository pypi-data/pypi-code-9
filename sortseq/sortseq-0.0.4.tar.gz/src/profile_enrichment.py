#!/usr/bin/env python

'''A script which calculates .'''
from __future__ import division
#Our standard Modules
import argparse
import numpy as np
import sys

import csv
import sortseq.nsbestimator as nsb
import sortseq.logratio as logratio
#Our miscellaneous functions
import pandas as pd
import sortseq.utils as utils



def main(df,dicttype,wtseq=None,start=0,end=None,pseudo=1):
    pd.set_option('max_colwidth',int(1e8))
    seq_dict,inv_dict = utils.choose_dict(dicttype)
    #Check that we have the right dictionary
    '''
    if not utils.is_seq_valid(df['seq'][0],seq_dict):
        sys.exit('Incorrect Sequence Dictionary')
    '''
    #add pseudocounts
    df['ct_0'] = df['ct_0'] + pseudo
    df['ct_1'] = df['ct_1'] + pseudo

    Ldict = len(seq_dict)
    df['seq'] = df['seq'].str.slice(start,end)
    seqL = len(df['seq'][0])
    temp_df = df.copy()
    wtseqtest = [] 
    enrich_ratio = np.zeros([seqL,Ldict])
    for i in range(seqL):
        #Find entries with each base at this position
        temp_df = df.copy()
        letlist = df['seq'].str.slice(i,i+1)
        temp_df['seq'] = letlist
        
        
        
        grouped = temp_df.groupby('seq')
        df_for_ratio = grouped.sum().reset_index()
        if not wtseq:
            wtseqtest.append(temp_df['seq'].mode()[0])
            print logratio.main(df_for_ratio,dicttype,wtseqtest[i])                
            enrich_ratio[i,:] = logratio.main(
                df_for_ratio,dicttype,wtseqtest[i])['lr']
        else:
            enrich_ratio[i,:] = logratio.main(
                df_for_ratio,dicttype,wtseq[i])['lr']
    column_headers = ['le_' + inv_dict[z] for z in range(Ldict)]
    output_df = pd.DataFrame(enrich_ratio,columns=column_headers)
    output_df['pos'] = range(start,start + seqL)
    if wtseq:
        output_df['wt'] = list(wtseq)
    else:
        output_df['wt'] = list(wtseqtest)
    output_df = output_df.replace([np.inf, -np.inf], np.nan)
    output_df = output_df[['pos','wt'] + column_headers]
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
    
    output_df = main(df,dicttype,wtseq=wtseq,start=start,end=end,pseudo=pseudo)
    if args.out:
        outloc = open(args.out,'w')
    else:
        outloc = sys.stdout
    output_df.to_string(
        outloc, index=False,col_space=10,float_format=utils.format_string)

# Connects argparse to wrapper
def add_subparser(subparsers):
    p = subparsers.add_parser('profile_enrichment')
    p.add_argument(
        '-s','--start',type=int,default=0,help ='''Position to start 
        your analyzed region''')
    p.add_argument(
        '-e','--end',type=int,default = None, help='''Position to end 
        your analyzed region''')
    p.add_argument('-w','--wtseq',help='Wild type sequence')
    p.add_argument('--pseudo',default=1,help='Pseudo counts to add')
    p.add_argument('-t', '--type', choices=['dna','rna','protein'], default='dna')
    p.add_argument(
        '-i', '--i', default=None,help='''Input file, otherwise input
        through the standard input.''')
    p.add_argument('-o', '--out', default=None)
    p.set_defaults(func=wrapper)
