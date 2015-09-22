#!/usr/bin/env python

'''A script which adds a calculated energy column to your dataframe.''' 
from __future__ import division
import argparse
import numpy as np
import scipy as sp
import pandas as pd
import sys

import sortseq.Models as Models
import sortseq.utils as utils

def main(df,mp,dicttype,modeltype='LinearEmat'):
    
    if modeltype == 'LinearEmat':
        mymodel = Models.LinearModel(mp[0],dicttype)
    elif modeltype == 'RandomLinear':
        emat_0 = utils.RandEmat(len(seqs[0]),len(seq_dict))
        mymodel = Models.LinearModel(emat_0,dicttype)
    else:
        mymodel = Models.CustomModel(mp)
    df['val'] = mymodel.genexp(df['seq'])
    return df['val']


# Define commandline wrapper
def wrapper(args):
    modeltype = args.modeltype
    dicttype = args.type
    try:
        mp = args.modelparam.strip('[').strip(']').split(',')
    except:
        mp = []
    # Run funciton
    if args.i:
        df = pd.io.parsers.read_csv(args.i,delim_whitespace=True)
    else:
        df = pd.io.parsers.read_csv(sys.stdin,delim_whitespace=True)
    df['val'] = main(df,mp,dicttype,modeltype=modeltype)
    
    
    

    if args.out:
        outloc = open(args.out,'w')
    else:
        outloc = sys.stdout
    pd.set_option('max_colwidth',int(1e8))
    df.to_string(
        outloc, index=False,col_space=10,float_format=utils.format_string)

# Connects argparse to wrapper
def add_subparser(subparsers):
    p = subparsers.add_parser('simulate_evaluate')
    p.add_argument(
        '-m', '--modeltype', type=str,choices=['RandomLinear','LinearEmat',
        'Custom'],help ='Type of Model to use')
    p.add_argument('-mp', '--modelparam', default=None,
        help='''Parameters should be entered as a list, with 
        RandomLinear=[LengthofSeq],LinearEmat=[FileName]. If you are using a 
        custom model enter a list of parameters with the first parameter
        being the python function name (for mymodel.py enter mymodel) ''')
    p.add_argument(
        '-t', '--type', choices=['dna','rna','protein'], default='dna')
    p.add_argument(
        '-i','--i',default=False,help='''Read input from file instead 
        of stdin''')
    p.add_argument('-o', '--out', default=None)
    p.set_defaults(func=wrapper)
