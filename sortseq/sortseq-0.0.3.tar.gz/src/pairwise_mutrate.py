#!/usr/bin/env python

'''A script which tests if there is any mutual information between one base
    being mutated and another base begin mutated.'''
from __future__ import division
#Our standard Modules
import argparse
import numpy as np
import sys

import csv
#Our miscellaneous functions
import pandas as pd
import sortseq.utils as utils
from scipy import stats
import scipy as sp
import sortseq.nsbestimator as nsb




def main(df,dicttype):
    pd.set_option('max_colwidth',int(1e8))
    seq_dict,inv_dict = utils.choose_dict(dicttype)
    strings = df['seq']
    #Make array of bases
    seq_arr = np.zeros([len(strings),len(strings[0])])
    for i in range(len(strings)):
        for z,b in enumerate(strings[i]):
            seq_arr[i,z] = seq_dict[b]
    wtarr = np.zeros(len(strings[i]))
    for z in range(len(strings[i])):
        wtarr[z] = np.argmax(
            np.histogram(seq_arr[:,z],bins=range(len(seq_dict)+1),
            weights=df['ct'])[0])
    seqL = len(strings[0])
    #Determine which bases are mutant
    mutarr = pd.DataFrame(seq_arr == wtarr)
    #See if there is any mutual information between mutation positions
    
    MI = np.zeros(sp.misc.comb(len(strings[0]),2) + len(strings[0]))
    pos_0 = np.zeros_like(MI,dtype=int)
    pos_1 = np.zeros_like(MI,dtype=int)
    counter = 0
    for i in range(len(strings[0])):
        #Get list [non-mut number,mut-number] at pos i
        mutcounts = [np.sum(df['ct'][mutarr[i]==q]) for q in range(2)]
        originalent = nsb.S(np.array(mutcounts),np.sum(mutcounts),2)
        for z in range(i,len(strings[0])):
            partialent = 0
            #split into 2 parts based on position z
            for q in range(2):
                partialmut = mutarr[i][mutarr[z]==q]
                partialcounts = df['ct'][mutarr[z]==q]
                mutcounts = [np.sum(partialcounts[partialmut==q]) for q in range(2)]
                partialent = (
                    partialent + len(partialmut)/len(strings)*
                    nsb.S(np.array(mutcounts),np.sum(mutcounts),len(mutcounts)))
            
            MI[counter] = originalent - partialent
            pos_0[counter] = i
            pos_1[counter] = z
            counter = counter + 1
    
    pos_0 = pd.Series(pos_0)
    pos_1 = pd.Series(pos_1)
    output_df = pd.concat([pos_0,pos_1,pd.DataFrame(MI)],axis=1)
    output_df.columns = ['pos_0','pos_1','MI']
    return output_df

# Define commandline wrapper
def wrapper(args):    
    # Run funciton
    seqs_df = pd.io.parsers.read_csv(
                  sys.stdin,delim_whitespace=True,usecols=['seq','ct'])
    output_df = main(seqs_df,args.type)
    
    

    if args.out:
        outloc = open(args.out,'w')
    else:
        outloc = sys.stdout

    output_df.to_csv(outloc, index=False, sep='\t')

# Connects argparse to wrapper
def add_subparser(subparsers):
    p = subparsers.add_parser('pairwise_mutrate') 
    p.add_argument('-t', '--type', choices=['dna','rna','protein'], default='dna')
    p.add_argument('-w','--wtseq',default=None,help ='Wild Type Sequence')
    p.add_argument('-o', '--out', default=None)
    p.set_defaults(func=wrapper)
