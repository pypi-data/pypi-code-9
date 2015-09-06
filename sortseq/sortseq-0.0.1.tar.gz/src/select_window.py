#!/usr/bin/env python

'''A script which clips the sequences in your dataframe'''
import argparse
import sys
import pandas as pd
import sortseq.utils as utils


def main(df,start=None,end=None):
    '''selects only the target part of each sequence.'''
    df['seq'] = df['seq'].str.slice(start=start,stop=end)
    return utils.collapse_further(df)

# Define commandline wrapper
def wrapper(args):

    
    
    if args.i:
        df = pd.io.parsers.read_csv(args.i,delim_whitespace=True)
    else:
        df = pd.io.parsers.read_csv(sys.stdin,delim_whitespace=True)
    
    output_df = main(df,start=args.start,end=args.end)
    if args.out:
        outloc = open(args.out,'w')
    else:
        outloc = sys.stdout
    pd.set_option('max_colwidth',int(1e8))
    output_df.to_string(
        outloc, index=False,col_space=10,float_format=utils.format_string)

# Connects argparse to wrapper
def add_subparser(subparsers):
    p = subparsers.add_parser('select_window')
    p.add_argument('-e', '--end', type=int,default=None,
        help = 'Last base in window, (with python indexing scheme)')
    p.add_argument('-s', '--start', type=int, default=None, 
        help='First base in window.')  
    p.add_argument(
        '-i', '--i', default=None,help='''Input file, otherwise input
        through the standard input.''')
    p.add_argument('-o', '--out', default=None)
    p.set_defaults(func=wrapper)
