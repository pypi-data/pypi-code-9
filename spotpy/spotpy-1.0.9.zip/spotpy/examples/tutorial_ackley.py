# -*- coding: utf-8 -*-
'''
Copyright 2015 by Tobias Houska
This file is part of Statistical Parameter Estimation Tool (SPOTPY).

:author: Tobias Houska

This class holds the example code from the ackley tutorial web-documention.
'''

import spotpy
from spot_setup_ackley import spot_setup
from spotpy import analyser

def calc_like(results,evaluation):
    likes=[]
    sim=spotpy.analyser.get_modelruns(results)
    for s in sim:
        likes.append(spotpy.likelihoods.rmse(list(s),evaluation))
        #likes.append(likelihoods.agreementindex(list(s),evaluation))
    return likes
    
#Create samplers for every algorithm:

rep=15000
dims=[2]
fig=plt.figure(figsize=(16,15))

for i in range(len(dims)):
    results=[]
    setup=spot_setup(dims[i])

    sampler=spotpy.algorithms.mc(setup,    dbname='ackleyMC',    dbformat='csv')
    sampler.sample(rep)
    results.append(sampler.getdata())
    #
    sampler=spotpy.algorithms.lhs(setup,   dbname='ackleyLHS',   dbformat='csv')
    sampler.sample(rep)
    results.append(sampler.getdata())
    
    sampler=spotpy.algorithms.mle(setup,   dbname='ackleyMLE',   dbformat='csv')
    sampler.sample(rep)
    results.append(sampler.getdata())
    
    sampler=spotpy.algorithms.mcmc(setup,  dbname='ackleyMCMC',  dbformat='csv')
    sampler.sample(rep)
    results.append(sampler.getdata())
    
#    sampler=spotpy.algorithms.sceua(setup, dbname='ackleySCEUA', dbformat='csv')
#    sampler.sample(rep,ngs=2)
#    results.append(sampler.getdata())
#    
#    sampler=spotpy.algorithms.sa(setup,    dbname='ackleySA',    dbformat='csv')
#    sampler.sample(rep,Tini=50,Ntemp=20,alpha=0.99)
#    results.append(sampler.getdata())
#    
#    sampler=spotpy.algorithms.demcz(setup, dbname='ackleyDEMCz', dbformat='csv')
#    sampler.sample(rep,nChains=30)
#    results.append(sampler.getdata())
#
#    sampler=spotpy.algorithms.rope(setup,  dbname='ackleyROPE',  dbformat='csv')
#    sampler.sample(rep)
#    results.append(sampler.getdata())
#    
    algorithms=['MC','LHS','MLE','MCMC','SCEUA','SA','DEMCz','ROPE']
    evaluation = setup.evaluation()
    #spotpy.analyser.plot_likelihoodtraces(results,evaluation,algorithms,filename=str(dims[i])+'pars')

    font = {'family' : 'calibri',
        'weight' : 'normal',
        'size'   : 20}
    plt.rc('font', **font)   
    xticks=[0,5000,10000]
    
    for j in range(len(results)):
        ax  = plt.subplot(len(dims),len(results),(j+1)+i*len(results))
        likes=spotpy.analyser.calc_like(results[j],evaluation)  
        ax.plot(likes,'b-')
        ax.set_ylim(0,25)
        ax.set_xlim(0,len(results[0]))
        if i==len(dims)-1:        
            ax.set_xlabel(algorithms[j])
        ax.xaxis.set_ticks(xticks)
        if j==0:
            ax.set_ylabel('RMSE dims='+str(dims[i]))
            ax.yaxis.set_ticks([0,10,20])   
        else:
            ax.yaxis.set_ticks([])        
        
    #plt.tight_layout()
fig.savefig('test.png')




#results=[]
#for algorithm in algorithms:
#    results.append(spotpy.analyser.load_csv_results('ackley'+algorithm))







