from __future__ import division
import sys

import csv
import numpy as np
import scipy as sp
from collections import Counter
import scipy.ndimage
import os
import pandas as pd
#from scripts import EstimateMutualInfo

#Read data from our standard txt or csv files, if there is no data, throw an error

def sample(weights,T_counts):
    '''Sample our library according to their energies'''
    emean = T_counts*weights/np.sum(weights)
    resampled_lib = np.random.poisson(lam=emean)
    return resampled_lib
    
def choose_dict(dicttype):
    '''Get numbering dictionary for either dna,rna, or proteins'''
    if dicttype == 'dna':
        seq_dict = {'A':0,'C':1,'G':2,'T':3}
        inv_dict = {0:'A',1:'C',2:'G',3:'T'}
    if dicttype == 'rna':
        seq_dict = {'A':0,'C':1,'G':2,'U':3}
        inv_dict = {0:'A',1:'C',2:'G',3:'U'}
    if dicttype == 'protein':
        seq_dict = {'*':0,'A':1,'C':2,'D':3,'E':4,'F':5,'G':6,'H':7,'I':8,'K':9,'L':10,'M':11,
            'N':12,'P':13,'Q':14,'R':15,'S':16,'T':17,'V':18,'W':19,'Y':20}
        inv_dict = {v:k for k,v in seq_dict.items()}
    return seq_dict,inv_dict

def get_column_headers(df,exptype=None):
    if exptype == 'sortseq':
        #will not include library bin
        nbins = 0    
        include = True
        while include:
            if 'ct_' + str(nbins+1) not in df.columns:
                break
            nbins = nbins + 1
        col_headers = ['ct_' + str(i+1) for i in range(nbins)] 
    elif (exptype == 'selex' or exptype == 'mpra' or exptype == 'dms'):
        col_headers = ['ct_0','ct_1'] #for these experiments only need library and expression bins
    elif exptype == None:
        #Detect experiment type
        nbins = 0    
        include = True
        while include:
            if 'ct_' + str(nbins+1) not in df.columns:
                break
            nbins = nbins + 1
        col_headers = ['ct_' + str(i+1) for i in range(nbins)] 
        if nbins == 1: #then exptype is not sort-seq
            col_headers = ['ct_0','ct_1']
            sys.stderr.write('''Experiment type assumed not to be SortSeq. Only bins 0
                 and 1 will be used in analysis.\n''')
        else:
            sys.stderr.write('Experiment type assumed to be SortSeq.\n')
    
    return col_headers

def collapse(df):
    '''Takes a list of sequences and batch numbers and returns seq, ct, ct_0...ct_K'''
    # index them starting at 1
    df['batch'] = df['batch']-df['batch'].min() + 1
    output_df = pd.DataFrame()
    for i in range(df['batch'].max() + 1):
        thisbatch = df['seq'][df['batch']==i]
        output_df = pd.concat([output_df,pd.Series(thisbatch.value_counts(),name='ct_'+str(i))],axis=1)
    batches = ['ct_' + str(i) for i in range(df['batch'].max()+1)]
    output_df['ct'] = np.sum(output_df[batches],axis=1)
    output_df = output_df.reset_index()
    output_df = output_df.rename(columns = {'index':'seq'})
    output_df = output_df.fillna(0)
    return output_df

def collapse_further(df):
    '''take clipped df and then collapse it further'''
    output_df = df.groupby('seq').sum()
    output_df = output_df.reset_index()
    try:
        output_df = output_df.drop('val',axis=1)
    except:
        pass   
    return output_df
        
# Checks validity of a sequence
def is_seq_valid(seq,seq_dict):
    return set(seq).issubset(set(seq_dict.keys()))

def seq2matsparse(seq,par_seq_dict):
    #Parameterize each sequence and put into a sparse matrix
    seqlist = np.zeros(len(par_seq_dict)*len(seq))
    for i,bp in enumerate(seq):
        try:
            seqlist[i*(len(par_seq_dict)) + par_seq_dict[bp]] = 1
        except:
            pass
    return seqlist

def seq2mat2(seq): # returns which parameters are true for the sequence, where each parameter is a possible pairing
    pair_dict = {'AA':0,'AC':1, 'AG':2,'AT':3,'CA':4,'CC':5,'CG':6,'CT':7,'GA':8,'GC':9,'GG':10,'GT':11,'TA':12,'TC':13,'TG':14}
    pairlist = []
    lseq = len(seq)
    index = 0
    for i,bp in enumerate(seq):
        for z in range(i+1,lseq):
            if bp + seq[z] == 'TT':
                continue
            pairlist.append(index*15 + pair_dict[bp + seq[z]])
            index = index +1
    return pairlist

def seq2mat3(seq): #Returns a parameterized matrix for 3 base pair interactions
    pair_dict = {'A':0,'C':1, 'G':2,'T':3}
    trilist = []
    lseq = len(seq)
    index = 0
    for i,bp in enumerate(seq):
        for z in range(i+1,lseq-1):
            for q in range(z+1,lseq):
                if bp + seq[z] + seq[q] == 'TTT':
                    continue
                trilist.append(index*63 + pair_dict[bp]*16 + pair_dict[seq[z]]*4 + pair_dict[seq[q]])
                index = index +1
    return trilist  
  
def compute_MI_linear(s,b,value,q1type,q2type):
    dot = emat[:,:,sp.newaxis]*seqs
    energies = dot.sum(0).sum(0)
    MI,V = EstimateMutualInfo.EstimateMI(b,value,q1type,q2type)
    return MI
    
def shuffle_rank(expression,y):
    #Rank Order everything
    index_shuf = range(len(y))
    sp.random.shuffle(index_shuf)
    batchtemp = y[index_shuf]
    expressiontemp = expression[index_shuf]
    temp = expressiontemp.argsort()
    rankexpression = np.empty(len(y))
    rankexpression[temp] = np.arange(len(expressiontemp))/len(y)       
    return rankexpression,batchtemp

def genlassomat(df,modeltype,seq_dict): 
    '''generates a paramaterized form of the sequence in a csr matrix. This is for
        use in learn_model for lasso mat'''
    
    n_seqs = int(np.sum(df['ct']))
    batch = np.zeros(n_seqs,dtype=int)
    mut_region_length = len(df['seq'][0])
    #Find bin number    
    nbins = 0    
    include = True
    while include:
        if 'ct_' + str(nbins + 1) not in df.columns:
            break
        nbins = nbins + 1
    binheaders = ['ct_' + str(i + 1) for i in range(nbins)]
    #convert count columns to int
    df[binheaders] = df[binheaders].astype(int)
    if modeltype == '1Point':
            lasso_mat = sp.sparse.lil_matrix((n_seqs,len(seq_dict)*mut_region_length))
            counter=0
            for i,s in enumerate(df['seq']):
                seqlist = seq2matsparse(s,seq_dict)
                for bnum, bh in enumerate(binheaders):
                    for c in range(df[bh][i]):
                        lasso_mat[counter,:] = seqlist
                        batch[counter] = bnum
                        counter = counter + 1
    '''
    #This section is for expanding the analysis to allow 2 and 3 point interactions
    elif modeltype == '2Point':
            lasso_mat = sp.sparse.lil_matrix((n_seqs,round(sp.misc.comb(mut_region_length,2))*15))
            for i,s in enumerate(seqs):
                lasso_mat[i,seq2mat2(s)] = 1
    elif modeltype == '3Point':
            lasso_mat = sp.sparse.lil_matrix((n_seqs,round(sp.misc.comb(mut_region_length,3))*63))
            for i,s in enumerate(seqs):
                lasso_mat[i,seq2mat3(s)] = 1
    '''
    return sp.sparse.csr_matrix(lasso_mat),batch

def expand_weights_array(expression,weights_arr):
    t_exp = np.zeros(np.sum(weights_arr))
    batch = np.zeros_like(t_exp)
    n_seqs,n_bins = weights_arr.shape
    counter = 0
    for i in range(n_seqs):
        for z in range(n_bins):
            t_exp[counter:counter+weights_arr[i,z]] = expression[i]
            batch[counter:counter+weights_arr[i,z]] = z
            counter = counter + weights_arr[i,z]
    return t_exp,batch

def expand_sw(expression,y,sample_weight):
    t_exp = np.zeros(np.sum(sample_weight))
    batch = np.zeros_like(t_exp,dtype=int)
    counter=0
    for i, sw in enumerate(sample_weight):
        t_exp[counter:counter+sample_weight[i]] = expression[i]
        batch[counter:counter+sample_weight[i]] = y[i]
        counter = counter+sample_weight[i]
    expression = t_exp
    y = batch
    return expression,y

def format_string(x):
    return '%10.6f' %x

def genweightandmat(df,seq_dict):
    '''For use with learn_model, linear regressions'''
    n_seqs = len(df['seq'])    
    mut_region_length = len(df['seq'][0])
    binheaders = get_column_headers(df)
    nbins=len(binheaders)
    #convert count columns to int
    df[binheaders] = df[binheaders].astype(int)
    lasso_mat = sp.sparse.lil_matrix((n_seqs,len(seq_dict)*mut_region_length))
    counter = 0
    sample_weights = np.zeros(n_seqs)
    batch = np.zeros(n_seqs)
    for i,s in enumerate(df['seq']):       
             lasso_mat[i,:] = seq2matsparse(s,seq_dict)             
             batch[i] = np.sum([df[binheaders[z]][i]*z for z in range(nbins)]/df['ct'][i])
             sample_weights[i] = df['ct'][i]
    return sp.sparse.csr_matrix(lasso_mat),batch,sample_weights
'''
def arrayweightandmat(df,seq_dict):
    n_seqs = len(df['seq'])    
    mut_region_length = len(df['seq'][0])
    #Find bin number    
    nbins = 0    
    include = True
    while include:
        if 'ct_' + str(nbins) not in df.columns:
            break
        nbins = nbins + 1
    binheaders = ['ct_' + str(i) for i in range(nbins)]
    #convert count columns to int
    df[binheaders] = df[binheaders].astype(int)
    counter = 0
    sample_weights = np.zeros(n_seqs)
    batch = np.zeros(n_seqs)
    seq_mat = np.zeros([len(seq_dict),mut_region_length,n_seqs])
    for i,s in enumerate(df['seq']):       
             seq_mat[:,:,counter] = seq2mat(s,seq_dict)
             batch[i] = np.sum([df[binheaders[z]][i]*z for z in range(nbins)]/df['ct'][i])
             sample_weights[i] = df['ct'][i]
    return seq_mat,batch,sample_weights
'''

def array_seqs_weights(df,seq_dict):
    n_seqs = len(df['seq'])    
    mut_region_length = len(df['seq'][0])
    #Find bin number    
    binheaders = get_column_headers(df)
    nbins = len(binheaders)
    #convert count columns to int
    df[binheaders] = df[binheaders].astype(int)
    nentries = (df[binheaders]).sum().sum()
    #nentries = (df[binheaders] != 0).sum().sum()
    seq_mat = np.zeros([len(seq_dict),mut_region_length,nentries])
    counter = 0
    
    batch = np.zeros(nentries,dtype=int)
    for i,s in enumerate(df['seq']):
        for z in range(nbins):
             for q in range(df[binheaders[z]][i]):
                 seq_mat[:,:,counter] = seq2mat(s,seq_dict)
                 batch[counter] = z
                 counter = counter+1
    return seq_mat,batch

def get_PSSM_from_weight_matrix(emat,factor):
    """get position specific scoring matrix from weight matrix. There
    is an undetermined scale factor, which JBK suggests manually
    adjusting until getting a reasonable information content (say 1
    bit per bp).

    Assumes that negative energies -> better binding.
    """
    
    # need to reverse sign for PSSM
    emat = -emat
    # set lowest element to zero
    emat = emat - emat.min(axis=0)
    # exponentiate
    p = sp.exp(factor*emat)
    p = p/p.sum(axis=0)
    return p

def compute_PSSM_self_information(p):
    """Compute self information of a PSSM. See the wikipedia page on
    PSSMs, for instance."""
    return -sp.sum(p*sp.log(p))

def kernal_smoothing_MI(seqs,batches,model):
    '''Smooths bin edges, and then calculates MI using naive entropy estimation'''  
    # preliminaries
    n_seqs = len(batches)
    n_batches = batches.max() + 1 # assumes zero indexed batches
    n_bins = 1000

    #energies = sp.zeros(n_seqs)
    f = sp.zeros((n_batches,n_seqs))

    # compute energies
    energies = model.genexp(seqs)


    # sort energies
    inds = sp.argsort(energies)
    for i,ind in enumerate(inds):
        f[batches[ind],i] = 1.0/n_seqs # batches aren't zero indexed


    # bin and convolve with Gaussian
    f_binned = sp.zeros((n_batches,n_bins))

    for i in range(n_batches):
        f_binned[i,:] = sp.histogram(f[i,:].nonzero()[0],bins=n_bins,range=(0,n_seqs))[0]
    #f_binned = f_binned/f_binned.sum()
    f_reg = scipy.ndimage.gaussian_filter1d(f_binned,0.04*n_bins,axis=1)
    f_reg = f_reg/f_reg.sum()

    # compute marginal probabilities
    p_b = sp.sum(f_reg,axis=1)
    p_s = sp.sum(f_reg,axis=0)

    # finally sum to compute the MI
    MI = 0
    for i in range(n_batches):
        for j in range(n_bins):
            if f_reg[i,j] != 0:
                MI = MI + f_reg[i,j]*sp.log2(f_reg[i,j]/(p_b[i]*p_s[j]))
    return MI,f_reg


def kernal_smoothing_MI_linear(energies,batches):
    '''This function is exactly the same as the previous function,
    but it removes the use of the model class, to fit with pymc syntax'''
    # preliminaries
    n_seqs = len(batches)
    n_batches = batches.max() + 1 # assumes zero indexed batches
    n_bins = 1000

    #energies = sp.zeros(n_seqs)
    f = sp.zeros((n_batches,n_seqs))


    # sort energies
    inds = sp.argsort(energies)
    for i,ind in enumerate(inds):
        f[batches[ind],i] = 1.0/n_seqs # batches aren't zero indexed


    # bin and convolve with Gaussian
    f_binned = sp.zeros((n_batches,n_bins))

    for i in range(n_batches):
        f_binned[i,:] = sp.histogram(f[i,:].nonzero()[0],bins=n_bins,range=(0,n_seqs))[0]
    #f_binned = f_binned/f_binned.sum()
    f_reg = scipy.ndimage.gaussian_filter1d(f_binned,0.04*n_bins,axis=1)
    f_reg = f_reg/f_reg.sum()

    # compute marginal probabilities
    p_b = sp.sum(f_reg,axis=1)
    p_s = sp.sum(f_reg,axis=0)

    # finally sum to compute the MI
    MI = 0
    for i in range(n_batches):
        for j in range(n_bins):
            if f_reg[i,j] != 0:
                MI = MI + f_reg[i,j]*sp.log2(f_reg[i,j]/(p_b[i]*p_s[j]))
    
    return MI,f_reg

def seq2mat(seq,seq_dict):
    '''Turn a sequence into a linear sequence matrix. This is for use with our linear energy matrices.'''
    mat = sp.zeros((len(seq_dict),len(seq)),dtype=int)
    for i,bp in enumerate(seq):
        mat[seq_dict[bp],i] = 1
    return mat

def parameterize_seq(seq,seq_dict):
    ('''Turn a sequence into parameterized matrix. We will use this for least squares regression. The energy matrix value for all T entries is
        set to zero.''')
    
    mat = sp.zeros((len(seq_dict)-1,len(seq)),dtype=int)
    for i,bp in enumerate(seq):
        try:
            mat[seq_dict[bp],i] = 1
        except:
            pass
    return mat

def emat_typical_parameterization(emat,Ldict):
    '''Takes a parameterized emat (3xL_seq), and returns a 'typical' energy matrix(4xL), with unit norm and average energy 0'''
    L = len(emat)/(Ldict-1)
    emat = emat.reshape([(Ldict-1),L],order='F')
    zmat = np.zeros(L)
    emat = np.vstack([emat,zmat])
    emat = fix_matrix_gauge(emat)
    return emat

def parameterize_emat(emat,Ldict):
    '''Turns 4xL typical Emat to a 3xL emat where all T values are set to zero''' 
    ematp = np.zeros([(Ldict-1),len(emat[0,:])])
    emat = emat - emat[(Ldict-1),:]
    ematp = emat[:(Ldict-1),:]
    return ematp

#Return raveled 
#def seq2matpair(seq):

def fix_matrix_gauge(emat):
    """Fix gauge of an energy matrix such that the average value
    of each column is zero (columns correspond to positions), and
    overall matrix norm is equal to 1."""
    # fix mean
    for j in range(emat.shape[1]):
        emat[:,j] = emat[:,j] -sp.mean(emat[:,j])
    # fix inner product
    emat = emat/sp.sqrt(sp.sum(emat*emat))
    return emat


def RandEmat(L,Ldict):
    '''Makes 4xL random emat'''
    emat_0 = fix_matrix_gauge(sp.randn(Ldict,L))
    return emat_0

def compute_MI(seqs,batches,matrixcoefs,n_bins):
    '''Compute the predictive information of a model onto sequence data'''
    # preliminaries
    n_seqs = len(batches)
    n_batches = int(batches.max()) + 1 # assumes zero indexed batches
    
    
    f = sp.zeros((n_batches,n_seqs))
    
    #If modeltype is an energy matrix for repression or activation, this will calculate the binding energy of a sequence, which will be monotonically correlated with expression.
    dot = matrixcoefs[:,:,sp.newaxis]*seqs
    expression = dot.sum(0).sum(0)
    

        
    


    # sort expressions
    inds = sp.argsort(expression)
    for i,ind in enumerate(inds):
        f[batches[ind],i] = 1.0/n_seqs # batches aren't zero indexed
        

    # bin and convolve with Gaussian
    f_binned = sp.zeros((n_batches,n_bins))
    MI = 0
    for i in range(n_batches):
        f_binned[i,:] = sp.histogram(f[i,:].nonzero()[0],bins=n_bins,range=(0,n_seqs))[0]
    
    p_b = sp.sum(f_binned,axis=1)
    originalent = nsb.S(p_b,n_seqs,n_batches)
    p_b = p_b/n_seqs
    p_s = sp.sum(f_binned,axis=0)/n_seqs
    H_nsb = [nsb.S(f_binned[:,i],f_binned[:,i].sum(),len(f_binned[:,i])) for i in range(0,n_bins)]
    H_var = [nsb.dS(f_binned[:,i],f_binned[:,i].sum(),len(f_binned[:,i])) for i in range(0,n_bins)]
    V = np.sqrt(np.sum(np.array(H_var)**2))
    H_mean = (p_s*H_nsb).sum()
    MI = originalent - H_mean

def analyze_pymc(M):
    '''Analyze the MCMC run to test for MI convergence, if not, throw up a flag'''
    burn_in = 1000
    emat_trace = M.trace('emat')[burn_in:]
    emat_mean = np.mean(emat_trace[:],axis=0)

    
