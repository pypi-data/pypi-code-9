#!/usr/bin/env python

'''A script which accepts a library through standard input and outputs mutation rate across each position.'''
from __future__ import division
#Our standard Modules
import argparse
import numpy as np
import scipy as sp
import sys

#Our miscellaneous functions
#This module will allow us to easily tally the letter counts at a particular position
import pandas as pd
import sortseq.utils as utils

import sortseq.predictiveinfo as predictiveinfo


class score_MI():
    def __call__(self,estimator,X,y,sample_weight=None):
        mymodel = Models.RaveledModel(estimator.coef_)
        expression = mymodel.genexp(X)
        if isinstance(sample_weight,(list,np.ndarray)):
            expression,y = utils.expand_sw(expression,y,sample_weight)            
        rankexpression,batch = utils.shuffle_rank(expression,y)
        
        MI,V = EstimateMutualInfo.EstimateMI(rankexpression,batch,'Continuous','Discrete')
        return MI

def calculate_predictive(model,df):
    nbins = 0    
    include = True
    while include:
        if 'ct_' + str(nbins + 1) not in df.columns:
            break
        nbins = nbins + 1
    column_headers = ['ct_' + str(z+1) for z in range(nbins)]
    expression = model.genexp(df['seq'])
    long_expression,batch = utils.expand_weights_array(expression,np.array(df[column_headers]))
    rankexpression,rankbatch = utils.shuffle_rank(long_expression,batch)
    MI,V = EstimateMutualInfo.EstimateMI(rankexpression,rankbatch,'Continuous','Discrete')
    return MI,V



def main(data_dfs,model_dfs,dataname,dicttype,exptype=None):
    pd.set_option('max_colwidth',int(1e8))
    seq_dict,inv_dict = utils.choose_dict(dicttype)

    model_column_headers = ['val_' + inv_dict[i] for i in range(len(seq_dict))]
    nummodels = len(mymodels)
    #Check that models describe proper location  
    lengths = [len(mymodels[z]['pos']) for z in range(nummodels)]
    lengths = lengths + [len(dfs[z]['seq'][0]) for z in range(nummodels)]
    
    if len(set(lengths)) > 1:
        raise ValueError('Sequences and Models have varying lengths!')

    MI = np.zeros([nummodels,nummodels])
    #Training sets = rows, test sets = columns
    for z, model_df in enumerate(model_dfs):
        for q, data_df in enumerate(data_dfs):            
            MI[z,q],V = calculate_predictive(data_df,model_df,dicttype=dicttype,exptype=exptype,modeltype='LinearEmat',start=0,end=None)

    output_df = pd.DataFrame(MI)
    output_df.columns = dataname
    output_df = pd.concat([pd.Series(dataname,name='Training/Test'),output_df],axis=1)    
    return output_df

# Define commandline wrapper
def wrapper(args):
    ds = pd.io.parsers.read_csv(args.datasets,delim_whitespace=True)
    models = pd.io.parsers.read_csv(args.models,delim_whitespace=True)
    if len(ds.exp) != len(models.exp):
        raise NameError('Wrong number of input models')

    dicttype = args.type
        	    
    dataname = ds.exp
    dfs = []
    mymodels = []
    for z,f in ds.iterrows():
        
        tempdf = pd.io.parsers.read_csv(f[1],delim_whitespace=True)
        tempdf['seq'] = tempdf['seq'].str.slice(args.start,args.end)
        dfs.append(utils.collapse_further(tempdf))

    for z,m in models.iterrows():
        
        mymodels.append(pd.io.parsers.read_csv(m[1],delim_whitespace=True))
    
    output_df = main(dfs,mymodels,dataname,dicttype,exptype=args.exptype)
    
  

    if args.out:
        outloc = open(args.out,'w')
    else:
        outloc = sys.stdout
    output_df.to_string(outloc, index=False,col_space=10,float_format=utils.format_string)

# Connects argparse to wrapper
def add_subparser(subparsers):
    p = subparsers.add_parser('compare_predictive_information')
    p.add_argument('-ds','--datasets',help='''White space delimited file, where the columns are name and file of data sets.''')
    p.add_argument('-s','--start',type=int,default=0,help ='Position to start your analyzed region')
    p.add_argument('-e','--end',type=int,default = None, help='Position to end your analyzed region')
    p.add_argument('-expt','--exptype',default=None,choices=[None,'sortseq','selex','dms','mpra'])
    p.add_argument('-m','--models',help='''File names containing models to evaluate.''')
    p.add_argument('-t', '--type', choices=['dna','rna','protein'], default='dna')            
    p.add_argument('-o', '--out', default=None)
    p.set_defaults(func=wrapper)
