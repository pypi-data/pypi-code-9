#!/usr/bin/env python

'''This script accepts input data frames of data sets and corresponding models
    and then computes predictive information of each model on each test dataset
    .'''
from __future__ import division
#Our standard Modules
import argparse
import numpy as np
import scipy as sp
import sys
#Our miscellaneous functions
import pandas as pd
import sortseq.utils as utils
import sortseq.predictiveinfo as predictiveinfo

def main(data_dfs,model_dfs,dataname,dicttype,exptype=None,start=0,end=None):
    
    seq_dict,inv_dict = utils.choose_dict(dicttype)
    col_headers = utils.get_column_headers(data_dfs[0])
    
    nummodels = len(model_dfs)
    #Check that models are the same length  
    lengths = [len(model_dfs[z]['pos']) for z in range(nummodels)] 
    if len(set(lengths)) > 1:
        raise ValueError('Models have varying lengths!')
    
    MI = np.zeros([nummodels,len(data_dfs)])
    #Training sets = rows, test sets = columns
    for z, model_df in enumerate(model_dfs):
        for q, data_df in enumerate(data_dfs):
            
            data_df2 = data_df.copy()         
            MI[z,q] = predictiveinfo.main(
                data_df2,model_df,dicttype=dicttype,exptype=exptype,
                modeltype='LinearEmat',start=start,end=end)
            print MI[z,q]

    output_df = pd.DataFrame(MI)
    output_df.columns = dataname
    output_df = pd.concat(
        [pd.Series(dataname,name='Training/Test'),output_df],axis=1)    
    return output_df

# Define commandline wrapper
def wrapper(args):
    ds = pd.io.parsers.read_csv(args.datasets,delim_whitespace=True)
    models = pd.io.parsers.read_csv(args.models,delim_whitespace=True)
    dfs = []
    mymodels = []
    #Create lists of test data sets and corresponding models
    for z,f in ds.iterrows():
        tempdf = pd.io.parsers.read_csv(f[1],delim_whitespace=True)
        dfs.append(utils.collapse_further(tempdf))
    
    for z,m in models.iterrows():        
        mymodels.append(pd.io.parsers.read_csv(m[1],delim_whitespace=True))
    dataname = ds.exp
    output_df = main(
        dfs,mymodels,dataname,args.type,exptype=args.exptype,
        start=args.start,end=args.end)
    
  

    if args.out:
        outloc = open(args.out,'w')
    else:
        outloc = sys.stdout
    pd.set_option('max_colwidth',int(1e8)) # Makes sure columns are not truncated
    output_df.to_string(
        outloc, index=False,col_space=10,float_format=utils.format_string)

# Connects argparse to wrapper
def add_subparser(subparsers):
    p = subparsers.add_parser('compare_predictive_information')
    p.add_argument(
        '-ds','--datasets',help='''White space delimited file, where the 
         columns are name and file of data sets.''')
    p.add_argument('-s','--start',type=int,default=0,help ='''
         Position to start your analyzed region''')
    p.add_argument('-e','--end',type=int,default = None, help='''
         Position to end your analyzed region''')
    p.add_argument('-expt','--exptype',default=None,choices=[None,'sortseq',
        'selex','dms','mpra'])
    p.add_argument('-m','--models',help='''File names containing models to
        evaluate.''')
    p.add_argument('-t', '--type', choices=['dna','rna','protein'],
        default='dna')            
    p.add_argument('-o', '--out', default=None)
    p.set_defaults(func=wrapper)
