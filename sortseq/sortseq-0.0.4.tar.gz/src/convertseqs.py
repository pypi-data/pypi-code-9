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
from Bio import Seq



def main(df):
    df['prot_seq'] = df['seq'].apply(Seq.translate)
    return df

# Define commandline wrapper
def wrapper(args):    
    # Run funciton
    if args.i:
        df = pd.io.parsers.read_csv(args.i,delim_whitespace=True)
    else:
        df = pd.io.parsers.read_csv(sys.stdin,delim_whitespace=True)

    output_df = main(df)[['ct_0','ct_1','prot_seq']]
    if args.out:
        outloc = open(args.out,'w')
    else:
        outloc = sys.stdout

    if len(df['seq']) > 100000:
        output_df = output_df[:100000]
    pd.set_option('max_colwidth',int(1e8))
    
    output_df.to_string(
        outloc, index=False,col_space=10,float_format=utils.format_string)
# Connects argparse to wrapper
def add_subparser(subparsers):
    p = subparsers.add_parser('convertseqs')
    p.add_argument(
        '-i','--i',default=False,help='''Read input from file instead 
        of stdin''')
    p.add_argument('-o', '--out', default=None)
    p.set_defaults(func=wrapper)
