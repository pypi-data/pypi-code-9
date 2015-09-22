#!/usr/bin/env python

from __future__ import division
import numpy as np
import csv
import os
import argparse
import statsmodels.api as sm
import sys
from subprocess import Popen, PIPE
import sortseq.nsbestimator as nsb
from sklearn.grid_search import GridSearchCV
if __name__== '__main__':
    import sortseq.utils as utils
from collections import Counter
from cStringIO import StringIO
import timeit


''' This script estimates MI by implementing the NSB estimator 
(For 2 Discrete Variables), Density Estimation through convolution with
 a kernel (Discrete-Continuous), or the Kraskov Estimator 
(Continuous-Continuous).
'''

class KernDE():
    '''Class that has a fit and predict method for use in scikit learn GridCV'''

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
    
                  



    

def EstimateMI(
        quant1,quant2,q1type,q2type,timedelay = '1',embedding = '1',
        kneig = '6',cv=False):   
    #If both variables are Discrete use NSB
    if (q1type == q2type and q1type == 'Discrete'): 

        '''We want to split into the fewest possible groupings to do our
        estimation, and we split based on quant2. We will check to see if 
        it is better to split based on quant1, if so, we will switch them.
        '''
        if len(set(quant1)) < len(set(quant2)):
            quant1, quant2 = quant2, quant1

        #get entropy of quantity 1
        counts = []
        q1counter = Counter(quant1)
        for key in q1counter.keys():
            counts.append(q1counter[key])
                     
        originalent = nsb.S(np.array(counts),np.sum(counts),len(counts))
        #Now split out based on quantity 2 and estimate entropies.
        partialent = 0
        MIvar = 0
        for val in set(quant2):
            #for each discrete quantity2, find the values of quantity 1
            q1list = [quant1[i] for i in range(len(quant2)) if quant2[i] == val] 
            q1counter = Counter(q1list)
            #Get counts of each value in quant1
            counts = []
            for key in set(quant1):
                counts.append(q1counter[key])
            #Calculate each entropy
            ent = nsb.S(np.array(counts),np.sum(counts),len(counts))
            dent = nsb.dS(np.array(counts),np.sum(counts),len(counts))
            #add partial entropy times prob of q2 value
            partialent = partialent + (len(q1list)/len(quant1))*ent
            #add to the variance
            MIvar = MIvar + (len(q1list)/len(quant1))*dent
        #now subtract in order to find MI
        MI = originalent - partialent
        return MI,np.sqrt(MIvar)
    #If one variable is continuous and one is discrete use kernel density est.
    if (q1type != q2type):
        if q1type == 'Discrete':
            quant1, quant2 = quant2, quant1
        #Estimate original entropy
        
        
        thekde = KernDE()
        if cv:
            '''use crossvalidation to determine proper gaussian bandwidth'''
            grid = GridSearchCV(
                KernDE(),{'bandwidth': np.logspace(-3, .16, 30)},refit=False)
            grid.fit(quant1)
        
            thekde.set_params(**grid.best_params_)
            
        thekde.fit(quant1)
        

        support = thekde.kde.support
        dsupport = np.sum(support.max()-support.min())/len(support)
        dens = thekde.kde.density
        #Integrate using riemann sum
        originalent = -np.sum(dens*np.log2(dens + 1e-15))*dsupport
        
        partialent = 0
        MIvar = 0
        for val in set(quant2):
            
            q1list = [quant1[i] for i in range(len(quant1)) if quant2[i] == val]
            
            if cv: 
                grid.fit(q1list)
                thekde.set_params(**grid.best_params_)
                
            thekde.fit(q1list)
            pdens = thekde.kde.density
            support = thekde.kde.support
            dsupport = np.sum(support.max()-support.min())/len(support)
            tent = -np.sum(pdens*np.log2(pdens + 1e-15))*dsupport
            partialent = partialent + len(q1list)/len(quant1)*tent
            
        MI = originalent - partialent
        V = None
        
        
        return MI,V

    #If both variables are continuous use Kraskov nearest neighbor estimator
    if (q1type == q2type and q1type == 'Continuous'):
        #The Kraskov Estimator requires the data be in a txt file.
        temp_file = open('kraskov_temp_file.txt','w')
        writer = csv.writer(temp_file,delimiter = '\t')
        writer.writerows(zip(*[quant1,quant2]))
        temp_file.close()
        '''Call the Kraskov estimator, it outputs automatically to stdout
        which we re-direct if the --out flag is used'''

        
        p = Popen(['./../src/MIhigherdim','kraskov_temp_file.txt','2',
                embedding,timedelay,str(len(quant1)),kneig],stdin=PIPE,
                stdout=PIPE,stderr=PIPE)
        MI = p.communicate()
        
        os.system('rm kraskov_temp_file.txt')
        V = None
        return MI,V
    else:
        sys.exit('Please input correct variable types')

def main():
    parser = argparse.ArgumentParser(description='''Estimate mutual 
                                        information between two variables''')
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
        '-cv','--crossvalidate',default=False,choices=[True,False], help=
        '''Cross validate Kernel Density Estimate. Default=False''')
    parser.add_argument(
        '-ed','--embedding',default='1',help='''Kraskov embedding dimension.
        Default=1''')
    parser.add_argument('-o','--out',default=False,help='''Output location/type, 
        by default it writes to standard output,if a file name is supplied 
        it will write to a text file''')
    args = parser.parse_args()
    
    header,inputarr = utils.read_stdin()
    quant1 = inputarr[0]
    quant2 = inputarr[1]
    MI,V = EstimateMI(quant1,quant2,args.q1type,args.q2type,timedelay = args.timedelay,
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

            
                
            
    
    


