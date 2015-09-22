#!/usr/bin/env python

'''A script with generates Simulated Data for a Sort Seq Experiment with a given mutation rate and wild type sequence.''' 
from __future__ import division
import argparse
import numpy as np
import scipy as sp
import pandas as pd
import sys
sys.path.append('../')
import sortseq.utils as utils
import sortseq.simulate_evaluate as simulate_evaluate
import sortseq.learn_model as learn_model
import sortseq.EstimateMutualInfo as EstimateMutualInfo
import sortseq.Models as Models
import re


# Converts a sequence to a numerical array
# [CHANGE SO TAKES MULTIPLE ALIGNED SEQUENCES AT ONCE]

def seq2arr(seq,seq_dict):
    '''Change base pairs to numbers'''
    return np.array([seq_dict[let] for let in seq])

# Converts a numerical array to a sequence
# [CHANGE SO TAKES A MATRIX WITH MULTIPLE ROWS]
def arr2seq(arr,inv_dict):
    '''Change numbers back into base pairs.'''
    return ''.join([inv_dict[num] for num in arr])

# main function for simulating library
def generate_seqs(wtseq=None, mutrate=0.10, numseq=10000,dicttype='dna',probarr=None):
    seq_dict,inv_dict = utils.choose_dict(dicttype)    
                
    if isinstance(probarr,np.ndarray):
        L = probarr.shape[1]
        #Generate bases according to probability matrix
        letarr = np.zeros([numseq,L])
        for z in range(L):
            letarr[:,z] = np.random.choice(range(len(seq_dict)),numseq,p=probarr[:,z]) 
    else:
        parr = []
        wtseq = wtseq.upper()
        L = len(wtseq)
        letarr = np.zeros([numseq,L])
        #Check to make sure the wtseq uses the correct bases.
        if not utils.is_seq_valid(wtseq,seq_dict):
            sys.exit('Please use only bases contained in ' + str(seq_dict.keys()))        
        #find wtseq array 
        wtarr = seq2arr(wtseq,seq_dict)
        mrate = mutrate/(len(seq_dict)-1) #The probability of any non-wild type base pair appearing
        #Generate sequences by mutating away from wildtype
        #probabilities away from wildtype (0 = stays the same, a 3 for example means a C becomes an A, a 1 means C-> G)
        parr = np.array([1-(len(seq_dict)-1)*mrate] + [mrate for i in range(len(seq_dict)-1)])  
        #Generate random movements from wtseq
        letarr = np.random.choice(range(len(seq_dict)),[numseq,len(wtseq)],p=parr) 

        #Find sequences
        letarr = np.mod(letarr + wtarr,len(seq_dict))

    seqs= []
    #Convert Back to letters
    for i in range(numseq):
        seqs.append(arr2seq(letarr[i,:],inv_dict))

    seqs_df = pd.DataFrame(seqs, columns=['seq'])
    
    
    return seqs_df

seq_dict,inv_dict = utils.choose_dict('dna')

def create_mut_c(seq,z=0,wtseq=None):
    
    mut = [m.start() for m in re.finditer('GT', seq)]
    seq = list(seq)
    choices = np.random.choice([0,1],len(mut),p=[1-z,z])
    
    #mut = np.roll((seq != wtseq),1)
    for num,mutpos in enumerate(mut):
        if choices[num] == 1:   
            seq[mutpos:mutpos+2] = 'AC'
    seq = ''.join(seq)
    ''' 
    seq = np.array([seq_dict[s] for s in seq])
    shifts = np.random.choice(range(4),len(wtseq),p=[z,(1-z)/3,(1-z)/3, (1-z)/3])
    shifts = shifts*mut
    seq = np.mod(seq + shifts,4)
    seq = ''.join([inv_dict[s] for s in seq])
    '''
    return seq

def main(wtseq=None, mutrate=0.10, numseq=10000,dicttype='dna',probarr=None,mRNAcounts=int(1e6),libcounts=int(1e5),include_pair=None):
    #generate sequencing lib
    numseq = int(numseq)
    mRNAcounts = int(mRNAcounts)
    libcounts = int(libcounts)
    df = generate_seqs(wtseq=wtseq,mutrate=mutrate,numseq=int(numseq),dicttype='dna')
    

    df.columns = ['seq']
    if include_pair:
        df['seq'] = df['seq'].apply(create_mut_c,z=include_pair,wtseq=wtseq)
    df['tag'] = generate_seqs(wtseq=wtseq,mutrate=.75,numseq=int(numseq))
    df['val'] = simulate_evaluate.main(df,['/home/bill/sortbackup/scripts/testemat10.txt'],'dna',modeltype='LinearEmat')
    df['ct'] = 1
    df['ct_0'] = utils.sample(df['ct'],int(libcounts))
    df['ct_1'] = utils.sample(df['ct']*np.exp(-df['val']),int(mRNAcounts))
    df.replace(0,np.NaN,inplace=True)
    df.dropna(how='any',subset=['ct_0','ct_1'],inplace=True)
    df.reset_index(inplace=True)
    df.replace(np.NaN,0,inplace=True)
    #grouped = df.groupby('seq')
    #dfsum = grouped.sum().reset_index()
    #ratio = np.array(dfsum['ct_1'])/np.array(dfsum['ct_0'])
    #normalization = ratio[dfsum['seq']==wtseq]
    #logratio = np.log(ratio/normalization)
    #dfsum['lr'] = logratio
    return df

def compute_matrix(df):
    mut_region_length = 10
    seq_dict,inv_dict = utils.choose_dict('dna')
    par_seq_dict = {v:k for v,k in seq_dict.items() if k != (len(seq_dict)-1)}
    lasso_mat = sp.sparse.lil_matrix((len(df['seq']),3*mut_region_length))

    for i,s in enumerate(df['seq']):       
             lasso_mat[i,:] = utils.seq2matsparse(s,par_seq_dict)
    em2 = learn_model.Compute_Least_Squares(lasso_mat,df['lr'],df['ct'])
    return utils.emat_typical_parameterization(em2,4)

def compute_MI(df,em):
   seq_dict,inv_dict = utils.choose_dict('dna')
   myModel = Models.LinearModel(em,seq_dict)
   val = myModel.genexp(df['seq'])
   return EstimateMutualInfo.EstimateMI(val,df['lr'],'Continuous','Continuous')

             
# Define commandline wrapper
def wrapper(args):
    if args.baseprob:
        probarr = np.genfromtxt(args.baseprob)
    else:
        probarr = None
    # Run funciton
    seqs_df = main(wtseq=args.wtseq, mutrate=args.mutrate, 
        numseq=args.numseqs,dicttype=args.type,probarr=probarr)
    
    if args.out:
        outloc = open(args.out,'w')
    else:
        outloc = sys.stdout

    seqs_df.to_csv(outloc, index=False, columns=['seq','ct'], sep='\t')

# Connects argparse to wrapper
def add_subparser(subparsers):
    p = subparsers.add_parser('simulate_library')
    p.add_argument('-w', '--wtseq', type=str, \
        help ='Wild Type Sequence')
    p.add_argument('-m', '--mutrate', type=float, default=0.09, \
        help='Mutation Rate, given fractionally. For example enter .1, not 10 percent')
    p.add_argument('-n', '--numseqs', type=int, default=100000, \
        help='Number of Sequences')
    p.add_argument('-bp','--baseprob',default=None,help=''' If you would like to 
        use custom base probabilities, this is the filename of a probability array.''')
    p.add_argument('-t', '--type', choices=['dna','rna','protein'], default='dna')
    p.add_argument('-o', '--out', default=None)
    p.set_defaults(func=wrapper)
