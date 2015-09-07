#!/usr/bin/env python

from __future__ import division
import numpy as np
import argparse
import statsmodels.api as sm
import sys
from subprocess import Popen, PIPE
import sortseq.nsbestimator as nsb
from sklearn.grid_search import GridSearchCV
if __name__== '__main__':
    import sortseq.utils
from collections import Counter
from cStringIO import StringIO
import pandas as pd
import scipy as sp
import scipy.ndimage


''' This script estimates MI by implementing a Density Estimation through 
    convolution with a kernel. Other methods are available for other variable 
    types. Currently it appears the 'alternate_calc_MI' is the most reliable.
'''

class KernDE():

    '''Class for kernel density estimation that has a fit and predict method for use in scikit learn GridCV'''

    def __init__(self,bandwidth='scott'): 
        self.bandwidth=bandwidth       

    def fit(self,data):
        self.kde = sm.nonparametric.KDEUnivariate(data)
        self.kde.fit(bw=self.bandwidth,cut=0)

    def score(self,evaldata):
        '''Evaluate log prob of model using the density grid. This method is
           more computationally efficient than using the evaluate method'''
        logprobdens = np.log2(self.kde.density[:-1])
        evalhist,bins = np.histogram(evaldata,bins=self.kde.support)
        logprob = np.sum(logprobdens*evalhist)
        return logprob

    def get_params(self,deep=False):
        param = {'bandwidth':self.bandwidth}
        return param
 
    def set_params(self,**param):
        self.bandwidth=param['bandwidth']   
    
    
def EstimateMI(df):       
        '''Estimate original entropy, this is the only function from this script
            we use for parallel tempering'''   
        
        thekde = KernDE()        
        originalent = 0 #always zero because rank order is flat.
        partialent = 0
        MIvar = 0
        #Find partial entropy for each bin value
        for val in set(df.index):
            tempdf = df.loc[val][0] #separate out all entries of certain bin                           
            thekde.fit(tempdf) #convolve with kernal
            #do reimann sum to find entropy.
            pdens = thekde.kde.density
            dsupport = np.sum(thekde.kde.support.max()-thekde.kde.support.min())/len(thekde.kde.support)
            tent = -np.sum(pdens*np.log2(pdens + 1e-15))*dsupport
            partialent = partialent + len(tempdf)/len(df[0])*tent
            
        MI = originalent - partialent
        V = None #don't know how to calculate this.
        
        
        return MI,V

def alternate_calc_MI(rankexpression,batches):
    
    n_bins = 1000
    n_seqs = len(batches)
    batches = batches - batches.min()
    n_batches = int(batches.max()+1)
    f = sp.zeros((n_batches,n_seqs))
    inds = sp.argsort(rankexpression)
    for i,ind in enumerate(inds):
        f[batches[ind],i] = 1.0/n_seqs # batches are zero indexed

    
    # bin and convolve with Gaussian
    f_binned = sp.zeros((n_batches,n_bins))

    for i in range(n_batches):
        f_binned[i,:] = sp.histogram(f[i,:].nonzero()[0],bins=n_bins,range=(0,n_seqs))[0]
    
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
    return MI
    
def main():
    parser = argparse.ArgumentParser(
        description='''Estimate mutual information between two variables''')
    parser.add_argument(
        '-q1','--q1type',choices=['Continuous','Discrete'],default='Discrete',
        help='Data type for first quantity.')
    parser.add_argument(
        '-q2','--q2type',choices=['Continuous','Discrete'],default='Discrete',
        help='Data type for first quantity.')
    parser.add_argument(
        '-k','--kneig',default='6',help='''If you are estimating Continuous
        vs Continuous, you can overwrite default arguments for the Kraskov 
        estimator here. This argument is number of nearest neighbors 
        to use, with 6 as the default.''')
    parser.add_argument(
        '-td','--timedelay',default='1',help='''Kraskov Time Delay, default=1''')
    parser.add_argument(
        '-cv','--crossvalidate',default=False,choices=[True,False],help=
        '''Cross validate Kernel Density Estimate. Default=False''')
    parser.add_argument(
        '-o','--out',default=False,help='''Output location/type, by 
        default it writes to standard output, if a file name is supplied 
        it will write to a text file''')
    args = parser.parse_args()
    
    
    MI,V = EstimateMI(
        quant1,quant2,args.q1type,args.q2type,timedelay = args.timedelay,
        embedding = args.embedding,kneig = args.kneig,cv=args.crossvalidate)
    if args.out:
                outloc = open(args.out,'w')
    else:
                outloc = sys.stdout
    outloc.write('Mutual Info \n')
    outloc.write('%.5s' %MI)
    if (args.q1type == args.q2type and args.q1type == 'Discrete'):
        outloc.write( ' +/- %.5s' %np.sqrt(V))
    outloc.write('\n')
         
if __name__ == '__main__':
    main()          

            
                
            
    
    


