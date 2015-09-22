#!/usr/bin/env python
from __future__ import division
#Our standard Modules
import argparse
import numpy as np
import sys
import sortseq.nsbestimator as nsb
#Our miscellaneous functions
#This module will allow us to easily tally the letter counts at a particular position
import pandas as pd
import sortseq.utils as utils
import sortseq.simulate_RNAseq_lib as simulate_RNAseq_lib
import sortseq.simulate_evaluate as simulate_evaluate
import sortseq.learn_model as learn_model

import sortseq.EstimateMutualInfoforMImax as EstimateMutualInfoforMImax
'''
#for testing ratio and library
emats = np.load('rnacounts_test_emats.npy')
MI = np.zeros([50,20])
df = simulate_RNAseq_lib.main(wtseq='ACAGGGTACC',mutrate=.1,numseq=1e5,libcounts=1e5,mRNAcounts=1e5)
col_headers = ['ct_0','ct_1']
for z in range(50):
    for i in range(20):
        df['val'] = -1*simulate_evaluate.main(df,[emats[z,i,:,:]],'dna',modeltype='LinearEmat')
        long_expression,batch = utils.expand_weights_array(df['val'],np.array(df[col_headers]))
        rankexpression,rankbatch = utils.shuffle_rank(long_expression,batch)
        MI[z,i] = EstimateMutualInfoforMImax.alternate_calc_MI(rankexpression,rankbatch)
        print MI[z,i]
np.save('MIRNA_test_mrnacounts',MI)
'''
#for testing mrna counts
emats = np.load('/home/bill/RNAseq/testpairemats.npy')
MI = np.zeros([30])
df = simulate_RNAseq_lib.main(wtseq='ACAGGGTACC',mutrate=.1,numseq=1e5,libcounts=5e5,mRNAcounts=5e5)
print df
emat10 = np.genfromtxt('/home/bill/sortbackup/scripts/testemat10.txt')

col_headers = ['ct_0','ct_1']

df['val'] = -1*simulate_evaluate.main(df,[emat10],'dna',modeltype='LinearEmat')
long_expression,batch = utils.expand_weights_array(df['val'],np.array(df[col_headers]))
rankexpression,rankbatch = utils.shuffle_rank(long_expression,batch)
mimax = EstimateMutualInfoforMImax.alternate_calc_MI(rankexpression,rankbatch)


for z in range(30):
        df['val'] = -1*simulate_evaluate.main(df,[emats[z,:,:]],'dna',modeltype='LinearEmat')
        long_expression,batch = utils.expand_weights_array(df['val'],np.array(df[col_headers]))
        rankexpression,rankbatch = utils.shuffle_rank(long_expression,batch)
        MI[z] = EstimateMutualInfoforMImax.alternate_calc_MI(rankexpression,rankbatch)
        print MI[z]
np.save('/home/bill/RNAseq/MIRNA_test_pair',MI)
#mi_max = 0.0111412574747
print 'mi_max = ' + str(mimax)

'''
#test mi of mimax
etest = np.load('/home/bill/RNAseq/emeantest2.npy')
emat10 = np.genfromtxt('/home/bill/sortbackup/scripts/testemat10.txt')
df = pd.io.parsers.read_csv('/home/bill/RNAseq/testdf.txt',delim_whitespace=True)
col_headers = ['ct_0','ct_1']
df['val'] = -1*simulate_evaluate.main(df,[emat10],'dna',modeltype='LinearEmat')
long_expression,batch = utils.expand_weights_array(df['val'],np.array(df[col_headers]))
rankexpression,rankbatch = utils.shuffle_rank(long_expression,batch)
mimax = EstimateMutualInfoforMImax.alternate_calc_MI(rankexpression,rankbatch)

print mimax

df['val'] = -1*simulate_evaluate.main(df,[etest],'dna',modeltype='LinearEmat')
long_expression,batch = utils.expand_weights_array(df['val'],np.array(df[col_headers]))
rankexpression,rankbatch = utils.shuffle_rank(long_expression,batch)
mi = EstimateMutualInfoforMImax.alternate_calc_MI(rankexpression,rankbatch)

print mi

ematdf = learn_model.main(df,'dna','least_squares',exptype='mpra')
headers = ['val_A','val_C','val_G','val_T']
emat = np.transpose(np.array(ematdf[headers]))

print emat
df['val'] = -1*simulate_evaluate.main(df,[emat],'dna',modeltype='LinearEmat')
long_expression,batch = utils.expand_weights_array(df['val'],np.array(df[col_headers]))
rankexpression,rankbatch = utils.shuffle_rank(long_expression,batch)
mi = EstimateMutualInfoforMImax.alternate_calc_MI(rankexpression,rankbatch)

print mi
'''




