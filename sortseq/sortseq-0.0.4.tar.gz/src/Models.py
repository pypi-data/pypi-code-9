#!/usr/bin/env python
#Class container for Model Handling
import importlib
import sys
import numpy as np
import sortseq.utils as utils	
import scipy as sp
import pandas as pd


class ExpModel:
    #All exp models return log expression
    pass


class LinearModel(ExpModel):
    ''' This model generates energies of binding 
        through a linear energy matrix model'''


    def __init__(self,param,dicttype):
        seq_dict,inv_dict = utils.choose_dict(dicttype)
        #if input is a text file
        if isinstance(param,str):
            self.matrix = np.genfromtxt(param,skip_header=1)
        #if input is a matrix
        elif isinstance(param,np.ndarray):
            self.matrix = param
        #if input is data frame
        elif isinstance(param,pd.DataFrame):
            headers = ['val_' + inv_dict[i] for i in range(len(seq_dict))]
            self.matrix = np.transpose(np.array(param[headers]))
        else:
            raise ValueError(
                '''Linear Model Input is not of correct type. 
                Enter File name of matrix (with header) or a matrix.''')
        self.seq_dict = seq_dict
        self.inv_dict = inv_dict

    def genexp(self,seqs):
        if len(seqs[0]) != self.matrix.shape[1]:
            raise ValueError('Energy Matrix Length does not equal Sequence Length')
        '''If modeltype is an energy matrix for repression or activation, this
             will calculate the binding energy of a sequence, which will be 
             monotonically correlated with expression.'''
        energies = np.zeros(len(seqs))
        if self.matrix.shape[0] == len(self.seq_dict)-1:
            for i,s in enumerate(seqs):
                 energies[i] = np.sum(
                     self.matrix*utils.parameterize_seq(s,self.seq_dict))
        elif self.matrix.shape[0] == len(self.seq_dict):
            for i,s in enumerate(seqs):
                energies[i] = np.sum(self.matrix*utils.seq2mat(s,self.seq_dict))
        else:
            raise ValueError('Input model has an incorrect number of rows') 
        return energies 

class RaveledModel(ExpModel):
    '''This model type generates an energy matrix model, 
        but accepts flattened matrices (for sklearn based fitting). It will not
        generate models from files or dataframes.'''

    def __init__(self,param):
          self.matrix = param
     
    def genexp(self,sparse_seqs_mat,sample_weight=None):
        if sp.sparse.issparse(sparse_seqs_mat):
            '''If modeltype is an energy matrix for repression or activation,
                this will calculate the binding energy of a sequence, which will 
                be monotonically correlated with expression.'''
            n_seqs = sparse_seqs_mat.shape[0]
            #energies = sp.zeros(n_seqs) 
            energies = np.zeros(n_seqs)
            energiestemp = sparse_seqs_mat.multiply(self.matrix).sum(axis=1)
            for i in range(0,n_seqs):
                 energies[i] = energiestemp[i]
        else:
            raise ValueError('Enter sparse sequence matrix.')
        if sample_weight:
            t_exp = np.zeros(np.sum(sample_weights))
            counter=0
            for i, sw in enumerate(sample_weight):
                t_exp[counter:counter+sample_weight[i]] = -energies[i]
                counter = counter + sample_weight[i]
            return t_exp
        else:
            return energies

class CustomModel(ExpModel):
    '''This is a class holder for user defined models'''

    def __init__(self,mp=''):
        self.mp = mp
        self.modeltype = modeltype
        try:
            self.model = importlib.import_module(mp[0])
        except:
            raise ValueError('''Input Custom Model does not exist. 
                Make sure it is a python function of the name you listed''')

    def genexp(self,seqs):
        return self.model.genexp(seqs,self.mp[1:])

class NoiseModel():

    def gennoisyexp(self,logexp):
        '''If no particular noise function is declared, then just assume no
            noise'''
        return logexp

    def genlist(self,df):
        nlist = []
        T_counts = np.sum(df['ct'])
        nexp = np.zeros(T_counts)
        counter = 0 
        for i,seq in enumerate(df['seq']):
            exp = df['val'][i]
            counts = df['ct'][i]
            explist = [exp for z in range(counts)]
            noisyexp = self.gennoisyexp(explist)
            nlist.append(noisyexp)
            nexp[counter:counter+counts]=noisyexp
            counter = counter + counts
        return nexp,nlist
    
        

class LogNormalNoise(NoiseModel):
    '''Noise model that adds autoflourescence and then draws the noisy 
        measurement from a log normal distribution with this mean'''
    def __init__(self,npar):
        self.auto = float(npar[0])
        self.scale = float(npar[1])

    def gennoisyexp(self,logexp):
        exp = np.exp(logexp) + self.auto
        nexp = np.random.lognormal(np.log(exp),self.scale)
        return np.log(nexp)

class NormalNoise(NoiseModel):
    '''Add Gaussian Noise'''
    def __init__(self,npar):
        self.scale = float(npar[0])

    def gennoisyexp(self,logexp):
        nexp = logexp + np.random.normal(
            scale=(np.abs(logexp).mean())*self.scale,size=len(logexp))
        return nexp

class PoissonNoise(NoiseModel):
    '''Add Noise for mpra experiment Expression Measurements'''
    def gennoisyexp(self,df,T_LibCounts,T_mRNACounts):
        exp = np.exp(df['val'])
        libcounts = df['ct']
        weights = exp*libcounts
        meanexp = T_mRNACounts*weights/np.sum(weights)
        meanlibcounts = libcounts/np.sum(libcounts)*T_LibCounts
        noisyexp = np.random.poisson(lam=meanexp)
        noisylibcounts = np.random.poisson(lam=meanlibcounts)
        return noisylibcounts,noisyexp

        

        

class CustomNoiseModel(NoiseModel):
    def __init__(self,modeltype,npar):
        self.npar = npar
        self.modeltype = modeltype
        try:
            self.model = importlib.import_module(modeltype) #import the modeltype function
        except:
            raise ValueError(
                '''Input Custom Model does not exist. Make sure 
                it is a python function of the name you listed''')
    def gennoisyexp(self,logexp):
        return self.model.genNoisyExp(logexp,self.npar)

