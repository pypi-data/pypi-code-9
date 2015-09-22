#!/usr/bin/env python
import sortseq.simulate_RNAseq_lib as simulate_RNAseq_lib
import numpy as np
import scipy as sp
import sortseq.learn_model as learn_model
import sortseq.utils as utils
import pandas as pd

seq_dict,inv_dict = utils.choose_dict('dna')
headers = ['val_' + str(inv_dict[i]) for i in range(len(seq_dict))]
'''
#test ratio of rna counts and lib counts. Also test effect of total lib size
mRNAcounts = 500000
ratio = np.linspace(.1,.9,20)
numlibraryseqs = np.logspace(4,6,50)
emat = np.zeros([50,20,4,10])

for i,lc in enumerate(numlibraryseqs):
    for z, rat in enumerate(ratio):
         df = simulate_RNAseq_lib.main(wtseq='ACAGGGTACC',mutrate=.01,numseq=lc,libcounts=mRNAcounts*rat,mRNAcounts=mRNAcounts*(1-rat))
         ematdf = learn_model.main(df,'dna','least_squares',exptype='mpra')
         emat[i,z,:,:] = np.transpose(np.array(ematdf[headers]))
         print 'hi'
         

np.save('rnaemat',emat)
'''

'''
MI_10 = np.zeros(100)
for i  in range(100):
    MI = simulate_RNAseq_lib.compute_MI(dffull,emat[i,10,:])
    MI_10[i] = float(MI[0][0].split('\n')[0])
'''    

   
def test_pair(): 
    emat = np.zeros([30,4,10])   
    for i,z in enumerate(np.linspace(.8,.9,30)):       
             df = simulate_RNAseq_lib.main(wtseq='ACAGGGTACC',mutrate=.1,numseq=50000,libcounts=50000,mRNAcounts=50000,include_pair=z)
             if i == 1:
                 pd.set_option('max_colwidth',int(1e8))
                 df.to_string(open('/home/bill/RNAseq/dftest','w'), index=False,col_space=10,float_format=utils.format_string)               
             ematdf = learn_model.main(df,'dna','least_squares',exptype='mpra')
             emat[i,:,:] = np.transpose(np.array(ematdf[headers]))
         
             print 'hi'
    np.save('/home/bill/RNAseq/testpairemats',emat)

#test effect of total number of sequencing counts
def test_mrnacounts():
    mRNAcounts = np.logspace(3.5,5.5,100)
    rat = .5
    lc = 5e4
    emat = np.zeros([100,4,10])
    for z,mrna in enumerate(mRNAcounts):
         try:
             df = simulate_RNAseq_lib.main(wtseq='ACAGGGTACC',mutrate=.01,numseq=lc,libcounts=mrna*rat,mRNAcounts=mrna*(1-rat))
             if np.mod(z,5) == 0:
                 print df
             ematdf = learn_model.main(df,'dna','least_squares',exptype='mpra')
             emat[z,:,:] = np.transpose(np.array(ematdf[headers]))
         except:
             emat[z,:,:] = np.zeros([4,10])
             print 'hi'
    np.save('/home/bill/RNAseq/rnacounts_test_emats_v3_lc50000',emat)


#test_mrnacounts()

'''
#test miMax
rat = .5
mrna = 50000
df = simulate_RNAseq_lib.main(wtseq='ACAGGGTACC',mutrate=.01,numseq=1e5,libcounts=mrna*rat,mRNAcounts=mrna*(1-rat))
df.to_string(open('/home/bill/RNAseq/testdf.txt','w'), index=False,col_space=10,float_format=utils.format_string)
'''

#for testing just lib counts


def test_lib_counts():
    libcounts = np.logspace(3,8,100)
    mrna = 1e5
    emat = np.zeros([100,4,10])
    totaldata = np.zeros(100)
    rat = .5
    for z,lc in enumerate(libcounts):
        try:
             df = simulate_RNAseq_lib.main(wtseq='ACAGGGTACC',mutrate=.01,numseq=lc,libcounts=mrna*rat,mRNAcounts=mrna*(1-rat))
             if np.mod(z,5) == 0:
                 print df
             ematdf = learn_model.main(df,'dna','least_squares',exptype='mpra')
             emat[z,:,:] = np.transpose(np.array(ematdf[headers]))
             totaldata[z] = df[['ct_0','ct_1']].sum().sum()
        except:
             emat[z,:,:] = np.zeros([4,10])
             print 'hi'
    np.save('/home/bill/RNAseq/libcounts_test_emats_v1',emat)
    np.save('/home/bill/RNAseq/libcounts_test_totaldata_v1',totaldata)

#test_lib_counts()
test_pair()
