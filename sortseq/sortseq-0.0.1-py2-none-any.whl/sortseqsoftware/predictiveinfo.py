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
import sortseq.Models as Models
import sortseq.simulate_evaluate as simulate_evaluate
from sklearn import linear_model
import sortseq.EstimateMutualInfoforMImax as EstimateMutualInfoforMImax


def main(data_df,model_df,dicttype='dna',exptype=None,modeltype='LinearEmat',start=0,end=None):
    data_df['seq'] = data_df['seq'].str.slice(start=start,stop=end)
    #Determine Exp Type is not given
    col_headers = utils.get_column_headers(data_df,exptype=exptype)
    if modeltype == 'LinearEmat':
        data_df['val'] = simulate_evaluate.main(data_df,[model_df],dicttype,modeltype=modeltype)
    else:
        raise ValueError('Cannot handle other model types at the moment. Sorry!')
    long_expression,batch = utils.expand_weights_array(data_df['val'],np.array(data_df[col_headers]))
    
    rankexpression,rankbatch = utils.shuffle_rank(long_expression,batch)
    MI = EstimateMutualInfoforMImax.alternate_calc_MI(rankexpression,rankbatch)

    return MI
     
def wrapper(args):
    
    data_df = pd.io.parsers.read_csv(args.dataset,delim_whitespace=True)    	    
    
    if args.i:
        model_df = pd.io.parsers.read_csv(args.i,delim_whitespace=True)
    else:
        model_df = pd.io.parsers.read_csv(sys.stdin,delim_whitespace=True)
    MI = main(data_df,model_df,dicttype='dna',exptype=args.exptype,start=args.start,end=args.end)
    output_df = pd.DataFrame([MI],columns=['info'])
  

    if args.out:
        outloc = open(args.out,'w')
    else:
        outloc = sys.stdout
    output_df.to_string(outloc, index=False,col_space=10,float_format=utils.format_string)

# Connects argparse to wrapper
def add_subparser(subparsers):
    p = subparsers.add_parser('predictiveinfo')
    p.add_argument('-ds','--dataset')
    p.add_argument('-expt','--exptype',default=None,choices=[None,'sortseq','selex','dms','mpra'])
    p.add_argument('-s','--start',type=int,default=0,help ='Position to start your analyzed region')
    p.add_argument('-e','--end',type=int,default = None, help='Position to end your analyzed region')
    p.add_argument('-m','--models',help='''File names containing models to evaluate.''')
    p.add_argument('-i', '--i', default=None,help='''Input file, otherwise input
        through the standard input.''')            
    p.add_argument('-o', '--out', default=None)
    p.set_defaults(func=wrapper)
