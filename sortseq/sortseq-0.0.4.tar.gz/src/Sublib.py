#!/usr/bin/env python
#Class container for Sublibrary Handling
from __future__ import division
import numpy as np
import scipy as sp
import sys

import scipy.ndimage
import sortseq.nsbestimator as nsb
from collections import Counter
import mpmath
import sortseq.EstimateMutualInfo as EstimateMutualInfo
import statsmodels.api as sm

def shannon_entropy(x):
    """compute shannon entropy of pmf x"""
    return sum([-p*sp.log2(p) for p in x if p > 0])


class Sublib:

    def __init__(self,seqs,batch):
        '''This method creates a list of batch numbers for each sequence'''
        '''
        useqs = list(set(seqs)) #unique sequences
        seqs_arr = [] #initialize seqs list
        #Find which sequences correspond to which batch
        inds = [np.nonzero(batch == i)[0] for i in range(0,batch.max()+1)]
        seqs_sorted = [[seqs[z] for z in inds[i]] for i in range(0,batch.max() + 1)]
        #Count them up
        counterarr = [Counter(seqs_sorted[i]) for i in range(0,batch.max() + 1)]
        #Put all the data into an array where each row has sequence, and then distribution over batches.
        for seq in useqs:
            seqs_arr.append([seq] + [counterarr[i][seq] for i in range(batch.max() + 1)])
        seqs_sorted = sorted(seqs_list,key=lambda seq: sum(seq[1:]),reverse=True)[:300]
        '''
        self.seqs_arr = None
        self.seqs = seqs
        self.batch = batch
        
    def compute_Seq_Dependent_Info(self,ReporterAssay):
        '''This method computes Total Sequence Dependent Info'''
        if ReporterAssay:
            MI,V = EstimateMutualInfo.EstimateMI(self.seqs,self.batch,'Discrete','Continuous')
        else:
            MI,V = EstimateMutualInfo.EstimateMI(self.seqs,self.batch,'Discrete','Discrete')
          
        self.seq_dependent_info = MI
        self.seq_dependent_info_std = V
        return MI,V

    def compute_Predictive_Info(self,mymodel,n_bins=100,estimationtype='KernalSmoothing'):
        '''This method computes the MI between a models energy predictions and the batch outcomes.
        This is a Discrete-Continuous comparision, so convolution with a kernal is the proper
        estimation method.'''
        seqs_arr = self.seqs_arr
        n_batches = len(seqs_arr[0][1:]) # assumes zero indexed batches
        

        rank_max = len(seqs_arr)
        # first, compute the shannon entropy of the batch distribution across
        # all sequences
        p_b = sp.zeros(len(seqs_arr[0][1:]))
        n_seqs = 0
        for i in range(rank_max):
            p_b = p_b + seqs_arr[i][1:]
            n_seqs = n_seqs + sum(seqs_arr[i][1:])
    
        f = sp.zeros((n_batches,rank_max))
        
        '''If modeltype is an energy matrix for repression or activation,
        this will calculate the binding energy of a sequence, which will be 
        monotonically correlated with expression.
        '''

        '''Calculate the expression for every sequence, 
        the list comprehension yeilds a list of seqs.'''
        expression = mymodel.genexp([seqs_arr[i][0] for i in range(rank_max)])      
        
        '''Sort expressions and fill array f with the number of sequences
        in each bin, where each column of f represents rising predicted energy.
        '''
        inds = sp.argsort(expression)
        
        for i,ind in enumerate(inds):
            f[:,i] = seqs_arr[ind][1:] 
        
        '''bin and convolve with Gaussian, you need to select n_bins 
        such that the number of data points in each bin is greater than 30.
        '''

        f_binned = sp.zeros((n_batches,n_bins)) 
        MI = 0
                        
        
        #First figure out bin edges
        edges = np.linspace(0,rank_max,num=n_bins+1)
        
        for i in range(n_batches): 
            #Add up all entries in f for each bin
            for q in range(n_bins):
                f_binned[i,q] = np.sum(f[i,edges[q]:edges[q+1]])
        
        if estimationtype == 'NSB':        
            p_b = sp.sum(f_binned,axis=1)
            originalent = nsb.S(p_b,n_seqs,n_batches)
            p_b = p_b/n_seqs
            p_s = sp.sum(f_binned,axis=0)/n_seqs
        
            H_nsb = [nsb.S(f_binned[:,i],f_binned[:,i].sum(),
                            len(f_binned[:,i])) for i in range(0,n_bins)]
            H_var = [nsb.dS(f_binned[:,i],f_binned[:,i].sum(),
                            len(f_binned[:,i])) for i in range(0,n_bins)]
            V = np.sqrt(np.sum(np.array(p_s*H_var)**2))
            H_mean = (p_s*H_nsb).sum()
        
            MI = originalent - H_mean

        if estimationtype == 'KernalSmoothing':
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
            V = 0
        
        return MI,V
    def separate_discrete_seqs(self):
        '''Removes all overrepresented seqs which will mess up our kernel density
                   estimates'''
        discrete_seqs = [self.seqs_arr[i][0] for i in range(len(self.seqs_arr)) 
                        if np.sum(self.seqs_arr[i][1:]) > .1*len(self.batch)]
        self.discrete_arr = [self.seqs_arr[i][:] for i in range(len(self.seqs_arr)) 
                        if self.seqs_arr[i][0] in discrete_seqs]
        self.cont_seqs = [self.seqs[i] for i in range(len(self.seqs)) 
                        if self.seqs[i] not in discrete_seqs]
        self.cont_batch = [self.batch[i] for i in range(len(self.seqs)) 
                        if self.seqs[i] not in discrete_seqs]
              
        
    def compute_Predictive_Infov2(self,mymodel,ReporterArray,cv=False):
        '''This will compute mutual info between the model and batch number.'''
        if ReporterArray:
            MI,V = EstimateMutualInfo.EstimateMI(rankexpression,batchtemp,'Continuous','Continuous')
                    
            
        
        else:
            '''Use formula MI = H[batch] - sum over(p(discrete seq)*H[batch|discrete seq])
                                - sum over(p(continuous seq)H_continuous seq'''
            '''First Separate discrete seqs'''
            '''
            self.separate_discrete_seqs()
            
            batchdist = Counter(self.batch).values()
            BatchEnt = nsb.S(np.array(batchdist),np.sum(batchdist),len(batchdist))
            #Discrete Entropy times respective sequence probabilities
            DiscEnt = 0
            for s in self.discrete_arr:
                DiscEnt = DiscEnt + np.sum(s[1:])/len(self.batch)*nsb.S(np.array(s[1:]),np.sum(s[1:]),len(s[1:]))
            #Continuous Entropy
            ContEnt = 0
            cont_exp = mymodel.genexp(self.cont_seqs)
            for val in set(self.batch):
                q1list = [cont_exp[i] for i in range(len(self.cont_batch)) if self.cont_batch[i] == val]
                if not q1list:
                    continue
                partialkde = sm.nonparametric.KDEUnivariate(q1list)
                partialkde.fit()
                dsupport = np.sum(partialkde.support.max()-partialkde.support.min())/len(partialkde.support)
                tent = -np.sum(partialkde.density*np.log2(partialkde.density + 1e-15))*dsupport
                ContEnt = ContEnt + len(q1list)/len(self.batch)*tent
            MI = BatchEnt - DiscEnt - ContEnt
            V = None
            '''
            expression = mymodel.genexp(self.seqs)
            #Shuffle the variables
            index_shuf = range(len(self.batch))
            sp.random.shuffle(index_shuf)
            batchtemp = self.batch[index_shuf]
            expressiontemp = expression[index_shuf]
            temp = expressiontemp.argsort()
            rankexpression = np.empty(len(self.batch))
            rankexpression[temp] = np.arange(len(expressiontemp))/len(self.batch)
            MI,V = EstimateMutualInfo.EstimateMI(rankexpression,batchtemp,'Continuous','Discrete',cv=cv)
            '''
            '''
        return MI,V
    
        







        
