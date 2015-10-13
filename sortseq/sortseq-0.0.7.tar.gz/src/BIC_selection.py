#!/usr/bin/env python

'''Simulates expression from an mpra, selex, or protein selection experiment''' 
from __future__ import division
import argparse
import numpy as np
import scipy as sp
import pandas as pd
import sys
import sortseq.Models as Models
import sortseq.utils as utils
import sortseq.predictiveinfo as predictiveinfo

def BIC(df_test,df_model,N,start=0,end=None):
    info = predictiveinfo.main(df_test,df_model,start=start,end=end)
    return -2*N*info + len(df_test['seq'][0])*np.log(N)

def main(df_train,df_test,df_model,start=0,end=None):
    N = len(df_train['seq'])
    if not end:
        end = start + len(df_model.index)
    #Now loop through model sizes until we find optimal size
    optimal_BIC = 0
    optimal_start = start
    optimal_end = end
    for test_start in range(start,end):
        for test_end in range(test_start,end):
            test_model_start = test_start - start
            test_model_end = len(df_model.index) + test_end - end
            test_BIC = BIC(
                df_test.copy(),df_model.copy()[test_model_start:test_model_end]
                ,N,start=test_start,end=test_end)
            if (test_BIC < optimal_BIC):
                optimal_BIC = test_BIC
                optimal_start = test_start
                optimal_end = test_end
    #adjust starts and ends to reflect model
    optimal_model_end = len(df_model.index) + optimal_end - end
    optimal_model_start = optimal_start - start
    optimal_model = df_model[optimal_model_start:optimal_model_end]
    return optimal_model


# Define commandline wrapper
def wrapper(args):
    df_train = pd.io.parsers.read_csv(args.df_train,delim_whitespace=True)
    df_test = pd.io.parsers.read_csv(args.df_test,delim_whitespace=True)
    df_model = pd.io.parsers.read_csv(args.df_model,delim_whitespace=True)
    optimal_model = main(df_train,df_test,df_model,start=args.start,end=args.end)
    if args.out:
        outloc = open(args.out,'w')
    else:
        outloc = sys.stdout
    pd.set_option('max_colwidth',int(1e8))
    optimal_model.to_string(
        outloc, index=False,col_space=10,float_format=utils.format_string)

# Connects argparse to wrapper
def add_subparser(subparsers):
    p = subparsers.add_parser('BIC_selection')
    p.add_argument(
        '--df_train', help ='''training data set.''')
    p.add_argument(
        '--df_test', help='''Testing data set.''')
    p.add_argument(
        '--df_model', help='''Model to optimize.''')
    p.add_argument('-s','--start',type=int,default=0)
    p.add_argument('-e','--end',type=int,default=None,help='''End of model region''')
    p.add_argument('-o', '--out', default=None)
    p.set_defaults(func=wrapper)
