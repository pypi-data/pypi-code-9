#!/usr/bin/env python

'''Simulate cell sorting based on expression'''
from __future__ import division
import argparse
import numpy as np
import scipy as sp
import pandas as pd
import sys
import sortseq.Models
import sortseq.utils

def main(df,noisetype,npar,nbins):
    #Apply noise to our measurements (which are already in our DF)
    if noisetype == 'LogNormal':
        NoiseModelSort = Models.LogNormalNoise(npar)
    elif noisetype == 'Normal':
        NoiseModelSort = Models.NormalNoise(npar)
    elif noisetype == 'None':
        NoiseModelSort = Models.NormalNoise([1e-16])
    else:
        NoiseModelSort = Models.CustomModel(noisetype,npar)
    noisyexp,listnoisyexp = NoiseModelSort.genlist(df)
    #Determine Expression Cutoffs for bins
    noisyexp.sort()
    cutoffs = list(
        noisyexp[np.linspace(0,len(noisyexp),nbins,endpoint=False,dtype=int)])
    cutoffs.append(np.inf)
    seqs_arr = np.zeros([len(listnoisyexp),nbins],dtype=int)
    for i,entry in enumerate(listnoisyexp):
        seqs_arr[i,:] = np.histogram(entry,bins=cutoffs)[0]
    col_labels = ['ct_' + str(i) for i in range(nbins)]
    output_df = pd.concat([df,pd.DataFrame(seqs_arr,columns=col_labels)],axis=1)      
    
    return output_df


# Define commandline wrapper
def wrapper(args):
    noisetype = args.noisemodel
    try:
        npar = args.noiseparam.strip('[').strip(']').split(',')
    except:
        npar = []
    nbins = args.nbins
    # Run funciton
    if args.i:
        df = pd.io.parsers.read_csv(
            args.i,delim_whitespace=True,
            dtype={'seqs':str,'batch':int,'val':float})
    else:
        df = pd.io.parsers.read_csv(
            sys.stdin,delim_whitespace=True,
            dtype={'seqs':str,'batch':int,'val':float})
    output_df = main(df,noisetype,npar,nbins)
    
    if args.out:
        outloc = open(args.out,'w')
    else:
        outloc = sys.stdout
    pd.set_option('max_colwidth',int(1e8))
    output_df.to_string(
        outloc, index=False,col_space=10,float_format=utils.format_string)

# Connects argparse to wrapper
def add_subparser(subparsers):
    p = subparsers.add_parser('simulate_sort')
    p.add_argument('-nm', '--noisemodel',
        choices=['LogNormal','Normal','None','Custom'],default='LogNormal',
        help='''Function module name that determines noisy expression from base 
        expression. For example if your function is contained 
        mynoisemodel.py enter mynoisemodel. The default noise model 
        adds a set autoflourescence value and log-normal noise. The 
        function name within the module should be gennoisyexp. 
        Its first input argument must be the list of expression values,
        and the second should be a vector containing all other 
        parameters as strings. If you would like no noise, enter None).''')
    p.add_argument(
        '-npar','--noiseparam',default = '[.2,.2]',help = '''
        Parameters for your noise model, as a list. The required parameters are
        LogNormal=[autoflouro,scale],Normal=[scale]. For custom models, enter a
        list of your parameters, with function name as the first entry.''')
    #Number of bins to Sort into
    p.add_argument(
        '-i','--i',default=False,help='''Read input from file instead 
        of stdin''')
    p.add_argument(
        '-n','--nbins',type=int,default=4,
        help='''Number of bins to sort into.''')
    p.add_argument('-o', '--out', default=None)
    p.set_defaults(func=wrapper)
