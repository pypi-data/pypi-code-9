#!/usr/bin/python  
# -*- coding: utf-8 -*-

'''
Created on 2015-3-19

@author: Administrator
'''
import random 
import math
from collections import defaultdict
import sys,os,time
from optparse import OptionParser 
from tempfile import gettempdir
try:
    import numpy
except ImportError:
    print >>sys.stderr, "No numpy module"

#initial population
#case 1: generate initial population based on the input haplotype frequency
#initial frequency of haplotype from two selected loci ordered with 00,01,10,11 in background
def Population1(haplotype, hapfre,N):
    H={} #dict H storage the haplotype corresponding to the frequency
    for i in range(len(haplotype)):
        H[haplotype[i]]=hapfre[i]
    anpop={}  ##dict anpop storage individual ID corresponding to haplotype
    anpop["00"]=range(0,int(round(N*H["00"])))
    anpop["01"]=range(len(anpop["00"]),len(anpop["00"])+int(round(N*H["01"])))
    anpop["10"]=range(len(anpop["00"])+len(anpop["01"]),len(anpop["00"])+len(anpop["01"])+int(round(N*H["10"]))) 
    anpop["11"]=range(len(anpop["00"])+len(anpop["01"])+len(anpop["10"]),N)
    return H, anpop
#compute the fitness of individual with different haplotype
def Fitness11(Shap,S,haplotype):
    fitness={} #dict fitness storage the fitness of each haplotype
    for fele in haplotype:
        for mele in haplotype:
            if fele == Shap and mele == Shap:
                fitness.setdefault(fele,{})[mele]=(1+S)*(1+S)
            elif fele == Shap or mele == Shap:
                fitness.setdefault(fele,{})[mele]=1+S
            else:
                fitness.setdefault(fele,{})[mele]=1
    return fitness
"""
def Fitness12(Shap,S,haplotype):
    fitness={}
    for fele in haplotype:
        for mele in haplotype:
            recomhaplotype=[fele[0]+mele[1],mele[0]+fele[1]]
            if fele ==Shap and mele==Shap:
                fitness.setdefault(fele,{})[mele]=(1+S)*(1+S)
            elif fele == Shap or mele == Shap:
                if Shap in recomhaplotype:
                    fitness.setdefault(fele,{})[mele]=1+S
                else:
                    fitness.setdefault(fele,{})[mele]=1+S/(float(2))
            elif  Shap in recomhaplotype:
                fitness.setdefault(fele,{})[mele]=(1+S/(float(2)))
            else:
                fitness.setdefault(fele,{})[mele]=1
    return fitness
"""
def Fitness21(Shap,S,haplotype):
    fitness={}
    for fele in haplotype:
        for mele in haplotype:
            if fele == Shap or mele == Shap:
                fitness.setdefault(fele,{})[mele]=(1+S)
            else:
                fitness.setdefault(fele,{})[mele]=1
    return fitness
"""
def Fitness22(Shap,S,haplotype):
    fitness={}
    for fele in haplotype:
        for mele in haplotype:
            recomhaplotype=[fele[0]+mele[1],mele[0]+fele[1]]
            if fele ==Shap or mele==Shap:
                if Shap in recomhaplotype:
                    fitness.setdefault(fele,{})[mele]=(1+S)
                else:
                    fitness.setdefault(fele,{})[mele]=(1+S/float(2))
            elif  Shap in recomhaplotype:
                fitness.setdefault(fele,{})[mele]=(1+S/(float(2)))
            else:
                fitness.setdefault(fele,{})[mele]=1
    return fitness
"""
def Fitness3(Shap,S,haplotype):
    fitness={}
    for fele in haplotype:
        for mele in haplotype:
            locus1=[int(fele[0]),int(mele[0])]
            locus2=[int(fele[1]),int(mele[1])]
            if len(list(set(locus1))) == 2:
                if len(list(set(locus2)))==2:
                    if int(Shap[0]) in locus1 and int(Shap[1]) in locus2:
                        fitness.setdefault(fele,{})[mele]=(1+S[0])*(1+S[1])
                    elif int(Shap[0]) in locus1:
                        fitness.setdefault(fele,{})[mele]=1+S[0]
                    elif int(Shap[1]) in locus2:
                        fitness.setdefault(fele,{})[mele]=1+S[1]
                    else:
                        fitness.setdefault(fele,{})[mele]=1
                else:
                    if int(Shap[0]) in locus1 and int(Shap[1]) in locus2:
                        fitness.setdefault(fele,{})[mele]=(1+S[0])*(1+S[1])*(1+S[1])
                    elif int(Shap[0]) in locus1:
                        fitness.setdefault(fele,{})[mele]=1+S[0]
                    elif int(Shap[1]) in locus2:
                        fitness.setdefault(fele,{})[mele]=(1+S[1])*(1+S[1])
                    else:
                        fitness.setdefault(fele,{})[mele]=1
            else:
                if len(list(set(locus2)))==2:
                    if int(Shap[0]) in locus1 and int(Shap[1]) in locus2:
                        fitness.setdefault(fele,{})[mele]=(1+S[0])*(1+S[0])*(1+S[1])
                    elif int(Shap[0]) in locus1:
                        fitness.setdefault(fele,{})[mele]=(1+S[0])*(1+S[0])
                    elif int(Shap[1]) in locus2:
                        fitness.setdefault(fele,{})[mele]=1+S[1]
                    else:
                        fitness.setdefault(fele,{})[mele]=1
                else:
                    if int(Shap[0]) in locus1 and int(Shap[1]) in locus2:
                        fitness.setdefault(fele,{})[mele]=(1+S[0])*(1+S[0])*(1+S[1])*(1+S[1])
                    elif int(Shap[0]) in locus1:
                        fitness.setdefault(fele,{})[mele]=(1+S[0])*(1+S[0])
                    elif int(Shap[1]) in locus2:
                        fitness.setdefault(fele,{})[mele]=(1+S[1])*(1+S[1])
                    else:
                        fitness.setdefault(fele,{})[mele]=1
    return fitness
def Fitness4(Shap,S,haplotype):
    fitness={}
    for fele in haplotype:
        for mele in haplotype:
            locus1=[int(fele[0]),int(mele[0])]
            locus2=[int(fele[1]),int(mele[1])]
            if int(Shap[0]) in locus1 and int(Shap[1]) in locus2:
                fitness.setdefault(fele,{})[mele]=(1+S[0])*(1+S[1])
            elif int(Shap[0]) in locus1:
                fitness.setdefault(fele,{})[mele]=(1+S[0])
            elif int(Shap[1]) in locus2:
                fitness.setdefault(fele,{})[mele]=(1+S[1])
            else:
                fitness.setdefault(fele,{})[mele]=1
    return fitness
#compute the forward of haplotype frequency
def ForwardHapfre(fitness,theta,H,iterm,forward,Shap,haplotype,N,mu):
    T=1
    while T <= iterm:
        if H[Shap] < 1:
            H2={} # dict H2: haplotype frequency of next generation 
            D=H["00"]*H["11"]-H["01"]*H["10"] #compute the LD between two selected loci
            w1=H["00"]*fitness['00']['00']+H["01"]*fitness['00']['01']+H["10"]*fitness['00']['10']+H["11"]*fitness['00']['11']
            w2=H["00"]*fitness['01']['00']+H["01"]*fitness['01']['01']+H["10"]*fitness['01']['10']+H["11"]*fitness['01']['11']
            w3=H["00"]*fitness['10']['00']+H["01"]*fitness['10']['01']+H["10"]*fitness['10']['10']+H["11"]*fitness['10']['11']
            w4=H["00"]*fitness['11']['00']+H["01"]*fitness['11']['01']+H["10"]*fitness['11']['10']+H["11"]*fitness['11']['11']
            w=H["00"]*w1+H["01"]*w2+H["10"]*w3+H["11"]*w4
            H2["00"]=H["00"]*(w1/w)-theta*D*(fitness['00']['11']/w)
            H2["01"]=H["01"]*(w2/w)+theta*D*(fitness['00']['11']/w)
            H2["10"]=H["10"]*(w3/w)+theta*D*(fitness['00']['11']/w)
            H2["11"]=H["11"]*(w4/w)-theta*D*(fitness['00']['11']/w)
            v=mu/(len(H)-1)
            deltfre=[]
            Hmu={}
            for ele in sorted(H.keys(),reverse=False):
                mean=v-(mu+v)*H[ele]
                mukeys=Hmu.keys()
                psum=0
                newsum=0
                for key in Hmu.keys():
                    psum=psum+H[key]
                    newsum=newsum+Hmu[key]
                if psum >= 1 or len(mukeys) == 3:
                    Hmu[ele]=1-newsum
                else:
                    x=H[ele]/(1-psum)
                    if (1-x) >=0:
                        y=x+mean+random.normalvariate(0, 1)*math.sqrt(x*(1-x)/(N-psum*N))
                    else:
                        y=x+mean
                    Hmu[ele]=y*(1-psum)
            newH={}
            for ele in H:
                if H2[ele]+Hmu[ele]-H[ele] < 0:
                    newH[ele]=0
                else:
                    newH[ele]=H2[ele]+Hmu[ele]-H[ele]
            for ele in newH:
                forward.setdefault(T,{})[ele]=newH[ele]/sum(newH.values())
            H=forward[T]
        if H[Shap] >= 1:
            H[Shap]=1
            for ele in haplotype:
                if ele != Shap:
                    H[ele]=0
            forward[T]=H
        T=T+1
    return H,T-1,forward 
#forward recombination
def Frecombination(T,allpop,hapalle,theta,N,n):
    recomtype={} #dict storage the recombination haplotype as well as recombination probability
    popn=[len(allpop[T-1]["00"]),len(allpop[T-1]["01"]),len(allpop[T-1]["10"]),len(allpop[T-1]["11"])] # individual distribution in the previous generation 
    r00=[] # probability of recombination as 00
    r01=[] # probability of recombination as 01
    r10=[]# probability of recombination as 10
    r11=[]# probability of recombination as 11
    if hapalle == "00":
        r0000=n*theta*popn[0]*(popn[0]-1)/float(2)/float(2*N*(2*N-1))
        r0010=n*theta*popn[0]*popn[2]/float(2*N*(2*N-1))
        r0110=n*theta*popn[1]*popn[2]/float(2*N*(2*N-1))
        r0100=n*theta*popn[0]*popn[1]/float(2*N*(2*N-1))
        r00.append(r0000/(r0000+r0010+r0110+r0100))
        r00.append(r0010/(r0000+r0010+r0110+r0100))
        r00.append(r0110/(r0000+r0010+r0110+r0100))
        r00.append(r0100/(r0000+r0010+r0110+r0100))
        recomclass=list(numpy.random.multinomial(n,r00))
        recomtype.setdefault("00",{})["00"]=recomclass[0]
        recomtype.setdefault("00",{})["10"]=recomclass[1]
        recomtype.setdefault("01",{})["10"]=recomclass[2]
        recomtype.setdefault("01",{})["00"]=recomclass[3]
    elif hapalle == "01":
        r0101=n*theta*popn[1]*(popn[1]-1)/float(2)/float(2*N*(2*N-1))
        r0001=n*theta*popn[0]*popn[1]/float(2*N*(2*N-1))
        r0011=n*theta*popn[0]*popn[3]/float(2*N*(2*N-1))
        r0111=n*theta*popn[1]*popn[3]/float(2*N*(2*N-1))
        r01.append(r0101/(r0101+r0001+r0011+r0111))
        r01.append(r0001/(r0101+r0001+r0011+r0111))
        r01.append(r0011/(r0101+r0001+r0011+r0111))
        r01.append(r0111/(r0101+r0001+r0011+r0111))
        recomclass=list(numpy.random.multinomial(n,r01))
        recomtype.setdefault("01",{})["01"]=recomclass[0]
        recomtype.setdefault("00",{})["01"]=recomclass[1]
        recomtype.setdefault("00",{})["11"]=recomclass[2]
        recomtype.setdefault("01",{})["11"]=recomclass[3]
    elif hapalle == "10":
        r1010=n*theta*popn[2]*(popn[2]-1)/float(2)/float(2*N*(2*N-1))
        r0010=n*theta*popn[0]*popn[2]/float(2*N*(2*N-1))
        r0011=n*theta*popn[0]*popn[3]/float(2*N*(2*N-1))
        r1011=n*theta*popn[2]*popn[3]/float(2*N*(2*N-1))
        r10.append(r1010/(r1010+r0010+r0011+r1011))
        r10.append(r0010/(r1010+r0010+r0011+r1011))
        r10.append(r0011/(r1010+r0010+r0011+r1011))
        r10.append(r1011/(r1010+r0010+r0011+r1011))
        recomclass=list(numpy.random.multinomial(n,r10))
        recomtype.setdefault("10",{})["10"]=recomclass[0]
        recomtype.setdefault("00",{})["10"]=recomclass[1]
        recomtype.setdefault("00",{})["11"]=recomclass[2]
        recomtype.setdefault("10",{})["11"]=recomclass[3]
    else:
        r1111=n*theta*popn[3]*(popn[3]-1)/float(2)/float(2*N*(2*N-1))
        r0110=n*theta*popn[1]*popn[2]/float(2*N*(2*N-1))
        r0111=n*theta*popn[1]*popn[3]/float(2*N*(2*N-1))
        r1011=n*theta*popn[2]*popn[3]/float(2*N*(2*N-1))
        r11.append(r1111/(r1111+r0110+r0111+r1011))
        r11.append(r0110/(r1111+r0110+r0111+r1011))
        r11.append(r0111/(r1111+r0110+r0111+r1011))
        r11.append(r1011/(r1111+r0110+r0111+r1011))
        recomclass=list(numpy.random.multinomial(n,r11))
        recomtype.setdefault("11",{})["11"]=recomclass[0]
        recomtype.setdefault("01",{})["10"]=recomclass[1]
        recomtype.setdefault("01",{})["11"]=recomclass[2]
        recomtype.setdefault("10",{})["11"]=recomclass[3]
    return recomtype
        
#forward mutation
def C(n,k):
    combina=1
    for i in range(n-k+1,n+1):
        combina=combina*i
    combinb=1
    for j in range(2,k+1):
        combinb=combinb*j
    comnum=combina/combinb
    return comnum
def Fmutation(T,allpop,hapalle,mu,n):
    #mutation result in 01,10,11,because not allow for recurrent mutation
    mutationtype={} #storage the mutation type and probability
    popn=[len(allpop[T-1]["00"]),len(allpop[T-1]["01"]),len(allpop[T-1]["10"]),len(allpop[T-1]["11"])]
    if hapalle == "00":
        if popn[1]!=0:
            m0100=4*popn[1]*mu
        else:
            m0100=0
        if popn[2]!=0:
            m1000=4*popn[2]*mu
        else:
            m1000=0
        if popn[3]!=0:
            m1100=4*popn[3]*mu*mu
        else:
            m1100=0
        m=[m0100/(m0100+m1000+m1100),m1000/(m0100+m1000+m1100),m1100/(m0100+m1000+m1100)]
        mutaclass=list(numpy.random.multinomial(n,m))
        mutationtype.setdefault("00",{})["01"]=mutaclass[0]
        mutationtype.setdefault("00",{})["10"]=mutaclass[1]
        mutationtype.setdefault("00",{})["11"]=mutaclass[2]
    elif hapalle == "01":
        if popn[0]!=0:
            m0001=4*popn[0]*mu
        else:
            m0001=0
        if popn[2]!=0:
            m1001=4*popn[2]*mu*mu
        else:
            m1001=0
        if popn[3]!=0:
            m1101=4*popn[3]*mu
        else:
            m1101=0
        m=[m0001/(m0001+m1001+m1101),m1001/(m0001+m1001+m1101),m1101/(m0001+m1001+m1101)]
        mutaclass=list(numpy.random.multinomial(n,m))
        mutationtype.setdefault("01",{})["00"]=mutaclass[0]
        mutationtype.setdefault("01",{})["10"]=mutaclass[1]
        mutationtype.setdefault("01",{})["11"]=mutaclass[2]
    elif hapalle == "10":
        if popn[0]!=0:
            m0010=4*popn[0]*mu
        else:
            m0010=0
        if popn[1]!=0:
            m0110=4*popn[1]*mu*mu
        else:
            m0110=0
        if popn[3]!=0:
            m1110=4*popn[3]*mu
        else:
            m1110=0
        m=[m0010/(m0010+m0110+m1110),m0110/(m0010+m0110+m1110),m1110/(m0010+m0110+m1110)]
        mutaclass=list(numpy.random.multinomial(n,m))
        mutationtype.setdefault("10",{})["00"]=mutaclass[0]
        mutationtype.setdefault("10",{})["01"]=mutaclass[1]
        mutationtype.setdefault("10",{})["11"]=mutaclass[2]
    else:
        if popn[0] !=0:
            m0011=4*popn[0]*mu*mu
        else:
            m0011=0
        if popn[1] != 0:
            m0111=4*mu*popn[1]
        else:
            m0111 = 0
        if popn[2] !=0:
            m1011=4*mu*popn[2]
        else:
            m1011=0
        m=[m0011/(m0011+m0111+m1011),m0111/(m0011+m0111+m1011),m1011/(m0011+m0111+m1011)]
        mutaclass=list(numpy.random.multinomial(n,m))
        mutationtype.setdefault("11",{})["00"]=mutaclass[0]
        mutationtype.setdefault("11",{})["01"]=mutaclass[1]
        mutationtype.setdefault("11",{})["10"]=mutaclass[2]
    return mutationtype
#generate the relationship of parent-offsprings
def Forwardtrac(anpop,forward,iterm,r,mu,nsam,N,theta):
    ltrac={}
    rtrac={}
    allpop={}
    allpop[0]=anpop
    T=1
    while T < len(forward):
        frequence=forward[T]
        ancesfrequence=[int(round(forward[T-1]["00"]*N)),int(round(forward[T-1]["01"]*N)),int(round(forward[T-1]["10"]*N)),int(round(forward[T-1]["11"]*N))]
        allpop.setdefault(T,{})["00"]=range(0,int(round(N*frequence["00"])))
        allpop.setdefault(T,{})["01"]=range(len(allpop[T]["00"]),len(allpop[T]["00"])+int(round(N*frequence["01"])))
        allpop.setdefault(T,{})["10"]=range(len(allpop[T]["00"])+len(allpop[T]["01"]),len(allpop[T]["00"])+len(allpop[T]["01"])+int(round(N*frequence["10"]))) 
        allpop.setdefault(T,{})["11"]=range(len(allpop[T]["00"])+len(allpop[T]["01"])+len(allpop[T]["10"]),N)
        for ele in sorted(frequence.keys()):
            num=len(allpop[T][ele])
            if ele == "00":
                muta=4*(len(allpop[T-1]["11"]))*mu*mu+(4*len(allpop[T-1]["01"])+4*len(allpop[T-1]["10"]))*mu
                if ancesfrequence[0] >=1:
                    rec=theta*(ancesfrequence[0]*(ancesfrequence[0]-1)+ancesfrequence[0]*ancesfrequence[2]+ancesfrequence[1]*ancesfrequence[2]+ancesfrequence[0]*ancesfrequence[1])/float(2*N*(2*N-1))
                else:
                    rec=theta*(ancesfrequence[0]*ancesfrequence[2]+ancesfrequence[1]*ancesfrequence[2]+ancesfrequence[0]*ancesfrequence[1])/float(2*N*(2*N-1))
            elif ele == "01":
                muta=4*(len(allpop[T-1]["10"]))*mu*mu+(4*len(allpop[T-1]["00"])+4*len(allpop[T-1]["11"]))*mu
                if ancesfrequence[1] >= 1:
                    rec=theta*(ancesfrequence[1]*(ancesfrequence[1]-1)+ancesfrequence[0]*ancesfrequence[3]+ancesfrequence[1]*ancesfrequence[3]+ancesfrequence[0]*ancesfrequence[1])/float(2*N*(2*N-1))
                else:
                    rec=theta*(ancesfrequence[0]*ancesfrequence[3]+ancesfrequence[1]*ancesfrequence[3]+ancesfrequence[0]*ancesfrequence[1])/float(2*N*(2*N-1))
            elif ele == "10":
                muta=4*(len(allpop[T-1]["01"]))*mu*mu+(4*len(allpop[T-1]["00"])+4*len(allpop[T-1]["11"]))*mu
                if ancesfrequence[2] >=1:
                    rec=theta*(ancesfrequence[2]*(ancesfrequence[2]-1)+ancesfrequence[0]*ancesfrequence[2]+ancesfrequence[0]*ancesfrequence[3]+ancesfrequence[2]*ancesfrequence[3])/float(2*N*(2*N-1))
                else:
                    rec=theta*(ancesfrequence[0]*ancesfrequence[2]+ancesfrequence[0]*ancesfrequence[3]+ancesfrequence[2]*ancesfrequence[3])/float(2*N*(2*N-1))
            else:
                muta=4*(len(allpop[T-1]["00"]))*mu*mu+(4*len(allpop[T-1]["01"])+4*len(allpop[T-1]["10"]))*mu
                if ancesfrequence[3] >=1:
                    rec=theta*(ancesfrequence[3]*(ancesfrequence[3]-1)+ancesfrequence[1]*ancesfrequence[2]+ancesfrequence[1]*ancesfrequence[3]+ancesfrequence[2]*ancesfrequence[3])/float(2*N*(2*N-1))
                else:
                    rec=theta*(ancesfrequence[1]*ancesfrequence[2]+ancesfrequence[1]*ancesfrequence[3]+ancesfrequence[2]*ancesfrequence[3])/float(2*N*(2*N-1))
            gene=int(round(forward[T-1][ele]*N))/float(2*N)
            if gene+rec+muta != 0:
                sampleclass=list(numpy.random.multinomial(num,[gene/(gene+rec+muta),rec/(gene+rec+muta), muta/(gene+rec+muta)]))
                if sampleclass[0]!=0: 
                    genesample=list(numpy.random.choice(allpop[T-1][ele],sampleclass[0]))
                    for k in range(sampleclass[0]):
                        ltrac.setdefault(T,{})[allpop[T][ele][k]]=genesample[k]
                        rtrac.setdefault(T,{})[allpop[T][ele][k]]=genesample[k]    
                if sampleclass[1] !=0:
                    recomtype=Frecombination(T,allpop,ele,theta,N,sampleclass[1])
                    left=[]
                    right=[]
                    for lparent in recomtype.keys():
                        for rparent in recomtype[lparent].keys():
                            if recomtype[lparent][rparent] != 0:
                                left.extend(list(numpy.random.choice(allpop[T-1][lparent],recomtype[lparent][rparent])))
                                right.extend(list(numpy.random.choice(allpop[T-1][rparent],recomtype[lparent][rparent])))
                    for k in range(sampleclass[1]):
                        ltrac.setdefault(T,{})[allpop[T][ele][sampleclass[0]+k]]=left[k]
                        rtrac.setdefault(T,{})[allpop[T][ele][sampleclass[0]+k]]=right[k]
                if sampleclass[2] !=0:
                    mutationtype=Fmutation(T,allpop,ele,mu,sampleclass[2])
                    mutparent=[]
                    for parent in mutationtype[ele].keys():
                        if mutationtype[ele][parent] != 0:
                            mutparent.extend(list(numpy.random.choice(allpop[T-1][parent],mutationtype[ele][parent])))
                    for k in range(sampleclass[2]):
                        ltrac.setdefault(T,{})[allpop[T][ele][sampleclass[0]+sampleclass[1]+k]]=mutparent[k]
                        rtrac.setdefault(T,{})[allpop[T][ele][sampleclass[0]+sampleclass[1]+k]]=mutparent[k]
        T=T+1
    return allpop, ltrac, rtrac
#generate the DNA sequence of initial population
def Randomseq(anpop,position,two_locus):
    ancesent={} #dict ancesent storage the mutation sequence
    sampleclass=sorted(anpop.keys()) #haplotype class
    pvalue=[] #list pvalue storage the allele frequence of each segsite
    for ele in position:
        pvalue.append(random.uniform(0,1))
    for ele in sampleclass:
        allele=[]
        p1=position.index(two_locus[0])
        p2=position.index(two_locus[1])
        for i in range(len(position)):
            if i==p1:
                allele.append([int(ele[0])]*len(anpop[ele]))
            elif i == p2:
                allele.append([int(ele[1])]*len(anpop[ele]))
            else:
                allele.append(list(numpy.random.choice([0,1],len(anpop[ele]),replace=True,p=[pvalue[i],1-pvalue[i]])))
        for j in range(len(anpop[ele])):
            sallele=[]
            for k in range(len(position)):
                sallele.append(allele[k][j])
            ancesent[anpop[ele][j]]=sallele
    return ancesent

def Fsample(allpop,ltrac,rtrac,nsam,iterm,forward,mu,region,position,two_locus,anpop):
    offsample=[] #sample ID
    frequence=forward[iterm]
    left={} #sample corresponding to left ancestor ID
    right={} #sample corresponding to left ancestor ID
    samp=list(numpy.random.multinomial(nsam,[frequence["00"],frequence["01"],frequence["10"],frequence["11"]]))
    if samp[0] !=0:
        samp00=list(numpy.random.choice(allpop[iterm]["00"],samp[0],replace=False))## sampling of haplotype 00
    else:
        samp00=[]
    if samp[1] !=0:
        samp01=list(numpy.random.choice(allpop[iterm]["01"],samp[1],replace=False))
    else:
        samp01=[]
    if samp[2] !=0:
        samp10=list(numpy.random.choice(allpop[iterm]["10"],samp[2],replace=False))
    else:
        samp10=[]
    if samp[3] !=0:
        samp11=list(numpy.random.choice(allpop[iterm]["11"],samp[3],replace=False))
    else:
        samp11=[]
    for ele in samp00:
        left.setdefault("00",{})[ele]=ele
        right.setdefault("00",{})[ele]=ele
    for ele in samp01:
        left.setdefault("01",{})[ele]=ele
        right.setdefault("01",{})[ele]=ele
    for ele in samp10:
        left.setdefault("10",{})[ele]=ele
        right.setdefault("10",{})[ele]=ele
    for ele in samp11:
        left.setdefault("11",{})[ele]=ele
        right.setdefault("11",{})[ele]=ele
    leftkeys=left.keys()
    rightkeys=right.keys()
    T=iterm
    while T > 0:
        for ele in leftkeys:
            for individual in left[ele].keys():
                left.setdefault(ele,{})[individual]=ltrac[T][left.setdefault(ele,{})[individual]]
                right.setdefault(ele,{})[individual]=rtrac[T][right.setdefault(ele,{})[individual]]
        T=T-1
    ancesent=Randomseq(anpop,position,two_locus)
    p1=position.index(two_locus[0])
    p2=position.index(two_locus[1])
    cutoff=p1+int(round((p2-p1)/2))
    for ele in leftkeys:
        for individual in left[ele].keys():
            if left[ele][individual] == right[ele][individual]:
                offs=ancesent[left[ele][individual]]
            elif left[ele][individual] != right[ele][individual]:
                offs=ancesent[left[ele][individual]][0:cutoff]
                offs.extend(ancesent[right[ele][individual]][cutoff:len(ancesent[right[ele][individual]])])
            offs[p1]=int(ele[0])
            offs[p2]=int(ele[1])
            offsample.append(offs)
    return offsample

def Forwardsequence(position,offsample,res,two_locus):
    out="//"
    print >>res,out
    out="Segsites: "+str(len(position))
    print >> res,out
    out="Selected two_locus: "
    for ele in two_locus:
        out=out+str(ele)+' '
    print >> res, out
    out="Positions: "
    for ele in position:
        out=out+str(ele)+' '
    print >> res, out
    for sample in offsample:
        out=""
        for base in sample:
            out=out+str(base)
        print >> res,out


def main():
    usage = "usage: python %prog <-n sample_number> <-d replication_number> [...]"
    description = "two-SNPs locus evolution forward simulation of selection model. The order of haplotypes should follow 00,01,10 and 11. For example: python %prog -H 01, -s 0.01. If not input selected haplotype (-H) and selective coefficient (-s), neutral model was default."
    op = OptionParser(version="%prog 0.1",description=description,usage=usage,add_help_option=False)
    op.add_option("-h","--help",action="help",
                  help="Show this help message and exit.")
    op.add_option("-n","--sample number",dest="nsam",type="int",default="30",
                  help=" please input the number of simulated samples, default is 30 samples")
    op.add_option("-d","--duplication number",dest="nrep",type="int", default="1",
                  help=" please input the replication number of simulated samples, default is 1")
    op.add_option("-l","--region length",dest="region",type="int", default="10000",
                  help="please input the length of simulated region (bp), default is 10000")
    op.add_option("-g","--generation",dest="generation",type="int", default="30",
                  help="please input the number of simulated generation,default is 30")
    op.add_option("-t","--two locus",dest="two_locus",type="int", nargs=2,
                  help="please input the position of selected two_locus,seprated by space. It would be random selected in the region if not specified ")
    op.add_option("-p","--haplotype frequency",dest="hapf",type="float", nargs=4,
                  help="please input the frequency of haplotype of selected two_locus seprated by space. It followed the order 00, 01, 10 and 11 which 0 represented ancestor and 1 represented derived , the sum should be 1")
    op.add_option("-R","--recombination rate",dest="R",type="float", default="0.000000003",
                  help="please input the recombination rate per site r where in 4Nr,defaule is 3*10**(-8)")
    op.add_option("-u","--mutation rate", dest="mu",type="float",default="0.000000003",
                  help="please input the mutation rate per site u where in 4Nu,defaule is 3*10**(-8) ")
    op.add_option("-e","--segsites",dest="segsites",type="int",
                  help="please input the number of segsites in the region, it would be randomly generated according to the length of region if not input ")
    op.add_option("-M","--model",dest="model",type="str",default="M1",
                  help="please input the type of evolutional model from model1,model2,model3 and model4")
    op.add_option("-H","--selective advantage haplotype or selective allele", dest="H",type="str",
                  help="please specified the haplotype which was selected in evolution,for example 10; if evolution model was 3 or 4, the input was selective allele from two locus separate by comma, such as 1,0 ")
    op.add_option("-S","--selection coefficient",dest="s",type="str",
                  help="please input the select coefficient of haplotype which specified previous, default was 0 represent neutral model. If evolution model was 3 or 4, input two coefficient corresponding two locus separated by comma,such as 0.01,0.02")
    op.add_option("-o","--outfilename",dest="outfilename",type="str",default="forwardsimulation.out",
                  help="The file name of output file showing the simulation data including number of segsites, position of each segsite, positions of selected two-locus, allele of each sample")
    op.add_option("-f","--frequencyfilename",dest="frequencyfilename",type="str",default="Hapfre.trac",
                  help="The file name of haplotype frequency")

    (options,args) = op.parse_args()

    if not options.hapf:
        print "Please input the haplotype frequency according to 00, 01, 10 and 11 which 0 represented ancestral and 1 was derived."
        op.print_help()
        sys.exit(1)
    haplotype=["00","01","10","11"]
    hapfre=[]
    for ele in list(options.hapf):
        hapfre.append(float(ele))
    if float('%.4f'%sum(hapfre)) != 1:
        print "The sum of haplotype frequency is not equal 1!"
        sys.exit(1)
    model=options.model
    if not options.H and not options.s:
        print "You did not specify the selected haplotype!"
        Shap=haplotype[hapfre.index(max(hapfre))]
        S=0
    elif not options.H:
        print "Please input the haplotype corresponding to the selective coefficient, one from 00,01,10 and 11."
        sys.exit(1)
    elif not options.s:
        print "You did not input the selected coefficient of specificed haplotype."
        if model == "M3" or model == "M4":
            S=[0,0]
        else:
            S=0
    else:
        hap=options.H.split(",")
        if len(hap)==1:
            Shap=hap[0]
        else:
            Shap=hap[0]+hap[1]
        if Shap not in haplotype:
            print "The type of -H was error!"
            sys.exit(1)
        coefficient=options.s.split(",")
        if model =="M1" or model =="M2" :
            if len(coefficient) == 1:
                S=float(coefficient[0])
            else:
                print "The type of selective coefficient is inconsistent with evolutional model!"
                sys.exit(1)
        else:
            if len(coefficient) == 2:
                S=[float(coefficient[0]),float(coefficient[1])]
            else:
                print "The type of selective coefficient is inconsistent with evolutional model!"
                sys.exit(1)
    nsam = options.nsam
    nrep=options.nrep
    region=range(0,options.region)
    N=17469
    mu=options.mu
    r=options.R
    iterm=options.generation
    
    outputfilename=options.outfilename
    if os.path.exists(outputfilename):
        os.remove(outputfilename)
    if nsam >=N:
        N = nsam
    outputfilename=options.outfilename
    frequencyfilename=options.frequencyfilename
    if os.path.exists(outputfilename):
        os.remove(outputfilename)
    #------step 1: random generate initial population based on imput haplotype frequency-----------
    print "Generate the initial population"
    if model == "M1":
        fitness=Fitness11(Shap,S,haplotype)
    if model=="M2":
        fitness=Fitness21(Shap,S,haplotype)
    if model=="M3":
        fitness=Fitness3(Shap,S,haplotype)
    if model == "M4":
        fitness=Fitness4(Shap,S,haplotype)
    #-----------step 2: simulation offspring ----------------
    res=open(os.path.join(os.getcwd(),outputfilename),'wb')
    trac=open(os.path.join(os.getcwd(),frequencyfilename),'wb')
    for t in range(nrep):
        (H,anpop)=Population1(haplotype, hapfre,N)
        if not options.two_locus:
            two_locus=sorted(random.sample(region,2))
        else:
            two_locus=[]
            for ele in list(options.two_locus):
                two_locus.append(int(ele))
            two_locus=sorted(two_locus)
        theta=r*abs(two_locus[1]-two_locus[0])
        forward={}
        T=0
        forward[T]=H
        (H,T,forward)=ForwardHapfre(fitness,theta, H, iterm, forward,Shap,haplotype,N,mu)
        print "Print the track file of haplotype frequency"
        out="//"
        print >>trac,out
        out="T"+"\t"+"00"+"\t"+"01"+"\t"+"10"+"\t"+"11"
        print >> trac,out
        for ele in forward.keys():
            out=str(ele)+"\t"
            for key in sorted(forward[ele].keys()):
                out=out+str(forward[ele][key])+"\t"
            print >> trac,out
        (allpop,ltrac,rtrac)=Forwardtrac(anpop,forward,iterm,r,mu,nsam,N,theta)
        print "Simulation the offspring"
        print "simulation the "+str(t)+"th replication"
        
        if not options.segsites:
            segsites = numpy.random.poisson(len(region)/100, 1)[0]
        else:
            segsites = options.segsites
        if segsites == 2:
            position=two_locus
        else:
            position = random.sample(region,segsites)
        for ele in two_locus:
            if ele not in position:
                position.append(ele)
        position=sorted(position)
        offsample=Fsample(allpop,ltrac,rtrac,nsam,iterm,forward,mu,region,position,two_locus,anpop)
        Forwardsequence(position,offsample,res,two_locus)
        print " A region of "+str(options.region)+'bp include '+str(segsites)+" segsites were simulated for "+str(iterm)+' generations with sample size '+str(nsam)+' for '+str(t+1)+' replication.'
if __name__ == "__main__":
    
    try:
        main()
    except KeyboardInterrupt:
        sys.stderr.write("User interrupt me, see you!\n")
        sys.exit(0)    

            
                    
    

