#!/usr/bin/python  
# -*- coding: utf-8 -*-

'''
Created on 2015-5-12

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

def Hapftrac(hapfre,Shap,haplotype,deltfre,N):
    trac={}
    trac.setdefault(0,{})["00"]=hapfre[0]
    trac.setdefault(0,{})["01"]=hapfre[1]
    trac.setdefault(0,{})["10"]=hapfre[2]
    trac.setdefault(0,{})["11"]=hapfre[3]
    T=1
    k=haplotype.index(Shap)
    frequency=hapfre
    temphap=[]
    for ele in haplotype:
        if ele != Shap:
            temphap.append(ele)
    while 1:
        trac.setdefault(T,{})[Shap]=frequency[k]-deltfre[k]+random.normalvariate(0, 1)*math.sqrt(frequency[k]*(1-frequency[k])/N)
        i=2
        while i >= 0:
            if i==2:
                if 1-frequency[k] == 0:
                    y=deltfre[haplotype.index(temphap[i])]
                else:
                    x=frequency[haplotype.index(temphap[i])]/(1-frequency[k])
                    if int(N-frequency[k]*N) == 0 or x >= 1:
                        y=x+deltfre[haplotype.index(temphap[i])]
                    else:
                        y=x+deltfre[haplotype.index(temphap[i])]+random.normalvariate(0, 1)*math.sqrt(x*(1-x)/int(N-frequency[k]*N))
                trac.setdefault(T,{})[temphap[i]]=y*(1-frequency[k])
            elif i ==1:
                allp=1-frequency[k]-frequency[haplotype.index(temphap[2])]
                if allp == 0:
                    y=deltfre[haplotype.index(temphap[i])]
                else:
                    num=int(N-frequency[k]*N-frequency[haplotype.index(temphap[2])]*N)
                    x=frequency[haplotype.index(temphap[i])]/allp
                    if num == 0 or x >= 1:
                        y=x+deltfre[haplotype.index(temphap[i])]
                    else:
                        y=x+deltfre[haplotype.index(temphap[i])]+random.normalvariate(0, 1)*math.sqrt(x*(1-x)/num)
                trac.setdefault(T,{})[temphap[i]]=y*allp
            else:
                fre=1
                for key in trac[T].keys():
                    fre=fre-trac[T][key]
                trac.setdefault(T,{})[temphap[i]]=fre
            i=i-1
        if trac[T][Shap] <= 1/float(N):
            trac[T][Shap]=0
            valuesum=sum(trac[T].values())
            for ele in trac[T].keys():
                if trac[T][ele] == max(trac[T].values()):
                    trac[T][ele]= trac[T][ele]-valuesum+1
            break
        elif min(trac[T].values()) < 0:
            for ele in trac[T].keys():
                if trac[T][ele] < 0:
                    trac[T][ele] = 0
            valuesum=sum(trac[T].values())
            for ele in trac[T].keys():
                trac[T][ele]=trac[T][ele]/float(valuesum)
            frequency=[trac[T]["00"],trac[T]["01"],trac[T]["10"],trac[T]["11"]]
        elif max(trac[T].values()) == 1:
            break
        else:
            frequency=[trac[T]["00"],trac[T]["01"],trac[T]["10"],trac[T]["11"]]
        T=T+1
    return trac
##coalescent probability
def Pca(n,N):
    Coa_pro=(n*(n-1))/float(4*N)
    return Coa_pro
## selective model: Two Locus Coalescent with selective 
##coalescent probability

def Hapcoalescet(n,N,deltt,T,Haptrac,theta,haplotype,Shap,r,region):
    #colascent in 00,01,10,11
    #n=[int(nsam*Haptrac[t]["00"]),int(nsam*Haptrac[t]["01"]),int(nsam*Haptrac[t]["10"]),int(nsam*Haptrac[t]["11"])]
    if n[haplotype.index(Shap)]==0:
        fre=[]
        for ele in n:
            if ele !=0:
                fre.append(ele/float(sum(n)))
            else:
                fre.append(float(0))
    else:
        fre=[Haptrac[deltt+T]["00"],Haptrac[deltt+T]["01"],Haptrac[deltt+T]["10"],Haptrac[deltt+T]["11"]]
    hapcoa=[]
    i=0
    for i in range(len(n)):
        if n[i] > 1:
            hapcoa.append((1-r*len(region))*n[i]*(n[i]-1)/float(4*N*fre[i]))
        else:
            hapcoa.append(0)
    return hapcoa

def Haprecombiantion(n,N,deltt,T,Haptrac,theta,haplotype,Shap):
    #recombination result in 00,01,10,11
    #n=[int(nsam*Haptrac[t]["00"]),int(nsam*Haptrac[t]["01"]),int(nsam*Haptrac[t]["10"]),int(nsam*Haptrac[t]["11"])]
    if n[haplotype.index(Shap)]==0:
        fre=[]
        for ele in n:
            if ele !=0:
                fre.append(ele/float(sum(n)))
            else:
                fre.append(float(0))
        Num=[int(round(N*fre[0])),int(round(N*fre[1])),int(round(N*fre[2])),int(round(N*fre[3]))]
    else:
        fre=[Haptrac[deltt+T]["00"],Haptrac[deltt+T]["01"],Haptrac[deltt+T]["10"],Haptrac[deltt+T]["11"]]
        Num=[int(round(N*Haptrac[deltt+T]["00"])),int(round(N*Haptrac[deltt+T]["01"])),int(round(N*Haptrac[deltt+T]["10"])),int(round(N*Haptrac[deltt+T]["11"]))]
    r0000=n[0]*theta*(Num[0]-n[0])*(Num[0]-n[0]-1)/float(2)/float(2*N*(2*N-1))
    r0001=n[0]*theta*(Num[0]-n[0])*(Num[1]-n[1])/float(2*N*(2*N-1))
    r0010=n[0]*theta*(Num[0]-n[0])*(Num[2]-n[2])/float(2*N*(2*N-1))
    r0110=n[0]*theta*(Num[1]-n[1])*(Num[2]-n[2])/float(2*N*(2*N-1))
    r00=[r0000,r0001,r0010,r0110]
    r0101=n[1]*theta*(Num[1]-n[1])*(Num[1]-n[1]-1)/float(2)/float(2*N*(2*N-1))
    r0001=n[1]*theta*(Num[0]-n[0])*(Num[1]-n[1])/float(2*N*(2*N-1))
    r0011=n[1]*theta*(Num[0]-n[0])*(Num[3]-n[3])/float(2*N*(2*N-1))
    r0111=n[1]*theta*(Num[1]-n[1])*(Num[3]-n[3])/float(2*N*(2*N-1))
    r01=[r0101,r0001,r0011,r0111]
    r1010=n[2]*theta*(Num[2]-n[2])*(Num[2]-n[2]-1)/float(2)/float(2*N*(2*N-1))
    r0010=n[2]*theta*(Num[0]-n[0])*(Num[2]-n[2])/float(2*N*(2*N-1))
    r0011=n[2]*theta*(Num[0]-n[0])*(Num[3]-n[3])/float(2*N*(2*N-1))
    r1011=n[2]*theta*(Num[2]-n[2])*(Num[3]-n[3])/float(2*N*(2*N-1))
    r10=[r1010,r0010,r0011,r1011]
    r1111=n[3]*theta*(Num[3]-n[3])*(Num[3]-n[3]-1)/float(2)/float(2*N*(2*N-1))
    r0110=n[3]*theta*(Num[1]-n[1])*(Num[2]-n[2])/float(2*N*(2*N-1))
    r0111=n[3]*theta*(Num[1]-n[1])*(Num[3]-n[3])/float(2*N*(2*N-1))
    r1011=n[3]*theta*(Num[2]-n[2])*(Num[3]-n[3])/float(2*N*(2*N-1))
    r11=[r1111,r0110,r0111,r1011]
    hapreco=[sum(r00),sum(r01),sum(r10),sum(r11)]
    return hapreco,r00,r01,r10,r11

def Hapmutation(n,Haptrac,mu,deltt,T,haplotype,Shap,N):
    #mutation result in 01,10,11
    #n=[int(nsam*Haptrac[t]["00"]),int(nsam*Haptrac[t]["01"]),int(nsam*Haptrac[t]["10"]),int(nsam*Haptrac[t]["11"])]
    if n[haplotype.index(Shap)]==0:
        fre=[]
        for ele in n:
            if ele !=0:
                fre.append(ele/float(sum(n)))
            else:
                fre.append(float(0))
        Num=[int(round(N*fre[0])),int(round(N*fre[1])),int(round(N*fre[2])),int(round(N*fre[3]))]
    else:
        Num=[int(round(N*Haptrac[deltt+T]["00"])),int(round(N*Haptrac[deltt+T]["01"])),int(round(N*Haptrac[deltt+T]["10"])),int(round(N*Haptrac[deltt+T]["11"]))]
    hapmut=[]
    if Num[0] > 0:
        m0100=mu*Num[1]*n[0]/float(Num[0])
        m1000=mu*Num[2]*n[0]/float(Num[0])
        m1100=mu*mu*Num[3]*n[0]/float(Num[0])
    else:
        m0100=0
        m1000=0
        m1100=0
    m00=[m0100,m1000,m1100]
    if Num[1] > 0:
        m0001=mu*n[1]*Num[0]/float(Num[1])
        m1001=mu*mu*n[1]*Num[2]/float(Num[1])
        m1101=mu*n[1]*Num[3]/float(Num[1])
    else:
        m0001=0
        m1001=0
        m1101=0
    m01=[m0001,m1001,m1101]
    if Num[2] > 0:
        m0010=mu*n[2]*Num[0]/float(Num[2])
        m0110=mu*mu*n[2]*Num[1]/float(Num[2])
        m1110=mu*n[2]*Num[3]/float(Num[2])
    else:
        m0010=0
        m0110=0
        m1110=0
    m10=[m0010,m0110,m1110]
    if Num[3] > 0:
        m0011=mu**2*Num[0]*n[3]/float(Num[3])
        m0111=mu*Num[1]*n[3]/float(Num[3])
        m1011=mu*Num[2]*n[3]/float(Num[3])
    else:
        m0011=0
        m0111=0
        m1011=0
    m11=[m0011,m0111,m1011]
    hapmut=[m0100,m1000,m1100,m0001,m1001,m1101,m0010,m0110,m1110,m0011,m0111,m1011]
    return hapmut,m00,m01,m10,m11

def Hapbackward(nsam,N,mu,Haptrac,theta,hapfre,Shap,locus1,locus2,haplotype,region,Shapfrequency,r,logout):
    sample={}
    n=[int(round(nsam*hapfre[0])),int(round(nsam*hapfre[1])),int(round(nsam*hapfre[2])),int(round(nsam*hapfre[3]))]    
    if sum(n) > nsam:
        n[n.index(max(n))]=n[n.index(max(n))]-1
    active00=range(1,n[0]+1)
    for ele in active00:
        sample[ele]="00"
    active01=range(n[0]+1,sum(n[0:2])+1)
    for ele in active01:
        sample[ele]="01"
    active10=range(sum(n[0:2])+1,sum(n[0:3])+1)
    for ele in active10:
        sample[ele]="10"
    active11=range(sum(n[0:3])+1,sum(n)+1)
    for ele in active11:
        sample[ele]="11"
    shapfre=n[haplotype.index(Shap)]/float(sum(n))
    T=0
    time=0
    #the right hand locus
    rightlengths={}
    rightoffsprings={}
    rightparent={}
    #the left hand locus
    leftlengths={}
    leftoffsprings={}
    leftparent={}
    for i in range(1,sum(n)+1):
        rightlengths[i]=0
        rightoffsprings[i]=1
        rightparent[i]=0
        leftlengths[i]=0
        leftoffsprings[i]=1
        leftparent[i]=0
    #offspring nodes for each node
    activePairs=range(1,sum(n)+1)
    activeLeft=[] 
    activeRight=[]
    nextNode=sum(n)+1
    recon=[0,0,0,0]
    n=[0,0,0,0]
    for ele in activePairs:
        if sample[ele] == "00":
            recon[0]=recon[0]+1
            n[0]=n[0]+1
        elif sample[ele] == "01":
            recon[1] = recon[1]+1
            n[1]=n[1]+1
        elif sample[ele] == "10":
            recon[2] = recon[2]+1
            n[2]=n[2]+1
        else:
            recon[3] = recon[3]+1
            n[3]=n[3]+1
    for ele in activeLeft:
        if sample[ele] == "00":
            n[0]=n[0]+1
        elif sample[ele] == "01":
            n[1]=n[1]+1
        elif sample[ele] == "10":
            n[2]=n[2]+1
        else:
            n[3]=n[3]+1
    for ele in activeRight:
        if sample[ele] == "00":
            n[0]=n[0]+1
        elif sample[ele] == "01":
            n[1]=n[1]+1
        elif sample[ele] == "10":
            n[2]=n[2]+1
        else:
            n[3]=n[3]+1
    while len(activePairs)+max(len(activeLeft),len(activeRight)) > 1:
        # compute the probability of recombination
        activen=len(activePairs)+len(activeLeft)+len(activeRight)
        if T == max(Haptrac.keys()):
            deltt = 0
        else :
            deltt = 1    
        (hapreco,r00,r01,r10,r11)=Haprecombiantion(recon,N,deltt,T,Haptrac,theta,haplotype,Shap)
        recombination=sum(hapreco)*len(activePairs)
        # compute the probability of coalescent
        hapcoa=Hapcoalescet(n,N,deltt,T,Haptrac,theta,haplotype,Shap,r,region)
        coalescent=sum(hapcoa)
        # probability of mutation
        (hapmut,m00,m01,m10,m11)=Hapmutation(n,Haptrac,mu,deltt,T,haplotype,Shap,N)
        mutation=sum(hapmut)*activen
        prob=recombination+coalescent+mutation
        t=random.expovariate(prob)
        timet=1
        time=time+timet
        log=str(len(activePairs))+' '+str(len(activeLeft))+' '+str(len(activeRight))+" After "+str(t)+" times:"
        print >>logout,log 
        #update times for all nodes
        indexRight=[]
        if len(activeRight) > 0:
            indexRight.extend(activeRight)
        if len(activePairs) > 0:
            indexRight.extend(activePairs)
        for ele in indexRight:
            rightlengths[ele]=rightlengths[ele]+timet
        indexLeft=[]
        if len(activeLeft) > 0:
            indexLeft.extend(activeLeft)
        if len(activePairs) > 0:
            indexLeft.extend(activePairs)
        for ele in indexLeft:
            leftlengths[ele]=leftlengths[ele]+timet
        #determine the events was coalescent or recombination event?
        event=list(numpy.random.multinomial(1,[recombination/prob,coalescent/prob,mutation/prob]))
        #coalescent event
        if event.index(1)==1:
            active00=[]
            active01=[]
            active10=[]
            active11=[]
            for ele in activePairs:
                if sample[ele]=="00":
                    active00.append(ele)
                elif sample[ele]=="01":
                    active01.append(ele)
                elif sample[ele]=="10":
                    active10.append(ele)
                else:
                    active11.append(ele)
            for ele in activeRight:
                if sample[ele]=="00":
                    active00.append(ele)
                elif sample[ele]=="01":
                    active01.append(ele)
                elif sample[ele]=="10":
                    active10.append(ele)
                else:
                    active11.append(ele)
            for ele in activeLeft:
                if sample[ele]=="00":
                    active00.append(ele)
                elif sample[ele]=="01":
                    active01.append(ele)
                elif sample[ele]=="10":
                    active10.append(ele)
                else:
                    active11.append(ele)
            #pick two nodes at random coalescent
            #active=[]
            #if len(activeLeft) > 0:
            #    active.extend(activeLeft)
            #if len(activeRight) > 0:
            #    active.extend(activeRight)
            #if len(activePairs) > 0:
            #    active.extend(activePairs)
            coaprob=[hapcoa[0]/sum(hapcoa),hapcoa[1]/sum(hapcoa),hapcoa[2]/sum(hapcoa),hapcoa[3]/sum(hapcoa)]
            coalescenttype=list(numpy.random.multinomial(1,coaprob))
            if coalescenttype.index(1)==0:
                coasample=random.sample(active00,2)
                sample[nextNode]="00"
#                n[0]=n[0]+1
                for ele in coasample:
                    if ele in active00:
                        active00.remove(ele)
#                        n[0]=n[0]-1
            elif coalescenttype.index(1)==1:
                coasample=random.sample(active01,2)
                sample[nextNode]="01"
#                n[1]=n[1]+1
                for ele in coasample:
                    if ele in active01:
                        active01.remove(ele)
 #                       n[1]=n[1]-1
            elif coalescenttype.index(1)==2:
                coasample=random.sample(active10,2)
                sample[nextNode]="10"
#              n[2]=n[2]+1
                for ele in coasample:
                    if ele in active10:
                        active10.remove(ele)
#                        n[2]=n[2]-1
            else:
                coasample=random.sample(active11,2)
                sample[nextNode]="11"
#                n[3]=n[3]+1
                for ele in coasample:
                    if ele in active11:
                        active11.remove(ele)
#                        n[3]=n[3]-1
            log="Nodes "+str(coasample[0])+" and "+str(coasample[1])+' coalescent into '+str(nextNode)
            print >>logout,log
            #assign parent node
            for ele in coasample:
                rightparent[ele]=nextNode
                leftparent[ele]=nextNode
            #creat ancestor node
            rightparent[nextNode]=0
            leftparent[nextNode]=0
            rightlengths[nextNode]=0
            leftlengths[nextNode]=0
            rightoffsprings[nextNode]=0
            leftoffsprings[nextNode]=0
            for ele in coasample:
                rightoffsprings[nextNode]=rightoffsprings[nextNode]+rightoffsprings[ele]
                leftoffsprings[nextNode]=leftoffsprings[nextNode]+leftoffsprings[ele]
                
            #delete coalescent node in list
            activePairs=list(set(activePairs).difference(set(coasample)))
            activeLeft=list(set(activeLeft).difference(set(coasample)))
            activeRight=list(set(activeRight).difference(set(coasample)))
            #add new ancestor node to list
            if rightoffsprings[nextNode]==0:
                activeLeft.append(nextNode)
            elif leftoffsprings[nextNode]==0:
                activeRight.append(nextNode)
            else:
                activePairs.append(nextNode)
            ##check for special situation where one locus finishes coalescent     
            nextNode=nextNode+1
        #recombination event
        elif event.index(1)==0:
            #pick one node at random to recombine
            active00=[]
            active01=[]
            active10=[]
            active11=[]
            for ele in activePairs:
                if sample[ele]=="00":
                    active00.append(ele)
                elif sample[ele]=="01":
                    active01.append(ele)
                elif sample[ele]=="10":
                    active10.append(ele)
                else:
                    active11.append(ele)
            recprob=[hapreco[0]/sum(hapreco),hapreco[1]/sum(hapreco),hapreco[2]/sum(hapreco),hapreco[3]/sum(hapreco)]
            recomtype=list(numpy.random.multinomial(1,recprob))
            if recomtype.index(1)==2:
                recomsample=random.sample(active10,1)[0]
                recomparent=list(numpy.random.multinomial(1,[r10[0]/sum(r10),r10[1]/sum(r10),r10[2]/sum(r10),r10[3]/sum(r10)]))
                active10.remove(recomsample)
#                n[2]=n[2]-1
                if recomparent.index(1)==0:
                    sample[nextNode]="10"
                    sample[nextNode+1]="10"
#                    n[2]=n[2]+2
                elif recomparent.index(1)==1:
                    sample[nextNode]="00"
                    sample[nextNode+1]="10"
#                    n[2]=n[2]+1
#                    n[0]=n[0]+1
                elif recomparent.index(1)==2:
                    sample[nextNode]="00"
                    sample[nextNode+1]="11"
#                    n[0]=n[0]+1
#                    n[3]=n[3]+1
                else:
                    sample[nextNode]="10"
                    sample[nextNode+1]="11"
#                    n[2]=n[2]+1
#                    n[3]=n[3]+1
            elif recomtype.index(1)==0:
                recomsample=random.sample(active00,1)[0]
                recomparent=list(numpy.random.multinomial(1,[r00[0]/sum(r00),r00[1]/sum(r00),r00[2]/sum(r00),r00[3]/(sum(r00))]))
                active00.remove(recomsample)
#                n[0]=n[0]-1
                if recomparent.index(1)==0:
                    sample[nextNode]="00"
                    sample[nextNode+1]="00"
#                    n[0]=n[0]+2
                elif recomparent.index(1)==1:
                    sample[nextNode]="00"
                    sample[nextNode+1]="01"
#                    n[0]=n[0]+1
#                    n[1]=n[1]+1
                elif recomparent.index(1)==2:
                    sample[nextNode]="00"
                    sample[nextNode+1]="10"
#                    n[0]=n[0]+1
#                    n[2]=n[2]+1
                else:
                    sample[nextNode]="01"
                    sample[nextNode+1]="10"
#                    n[1]=n[1]+1
#                    n[2]=n[2]+1
            elif recomtype.index(1)==1:
                recomsample=random.sample(active01,1)[0]
                recomparent=list(numpy.random.multinomial(1,[r01[0]/sum(r01),r01[1]/sum(r01),r01[2]/sum(r01),r01[3]/(sum(r01))]))
                active01.remove(recomsample)
#                n[1]=n[1]-1
                if recomparent.index(1)==0:
                    sample[nextNode]="01"
                    sample[nextNode+1]="01"
#                    n[1]=n[1]+2
                elif recomparent.index(1)==1:
                    sample[nextNode]="00"
                    sample[nextNode+1]="01"
#                    n[0]=n[0]+1
#                    n[1]=n[1]+1
                elif recomparent.index(1)==2:
                    sample[nextNode]="00"
                    sample[nextNode+1]="11"
#                    n[0]=n[0]+1
#                    n[3]=n[3]+1
                else:
                    sample[nextNode]="01"
                    sample[nextNode+1]="11"
#                    n[1]=n[1]+1
#                    n[3]=n[3]+1
            else:
                recomsample=random.sample(active11,1)[0]
                recomparent=list(numpy.random.multinomial(1,[r11[0]/sum(r11),r11[1]/sum(r11),r11[2]/sum(r11),r11[3]/(sum(r11))]))
                active11.remove(recomsample)
#                n[3]=n[3]-1
                if recomparent.index(1)==0:
                    sample[nextNode]="11"
                    sample[nextNode+1]="11"
#                    n[3]=n[3]+2
                elif recomparent.index(1)==1:
                    sample[nextNode]="01"
                    sample[nextNode+1]="10"
#                    n[1]=n[1]+1
#                    n[2]=n[2]+1
                elif recomparent.index(1)==2:
                    sample[nextNode]="01"
                    sample[nextNode+1]="11"
#                    n[1]=n[1]+1
#                    n[3]=n[3]+1
                else:
                    sample[nextNode]="10"
                    sample[nextNode+1]="11"
#                    n[2]=n[2]+1
#                    n[3]=n[3]+1
            log="Node "+str(recomsample)+' splits into '+str(nextNode)+" and "+str(nextNode+1)
            print >>logout, log
            #assign different ancestor to recombinant
            rightparent[recomsample]=nextNode
            leftparent[recomsample]=nextNode+1
            activeRight.append(nextNode)
            activeLeft.append(nextNode+1)
            #create ancestor for right portion
            rightparent[nextNode]=0
            leftparent[nextNode]=0
            rightlengths[nextNode]=0
            leftlengths[nextNode]=0
            rightoffsprings[nextNode]=rightoffsprings[recomsample]
            leftoffsprings[nextNode]=0
            nextNode=nextNode+1
            #create ancestor for left portion
            rightparent[nextNode]=0
            leftparent[nextNode]=0
            rightlengths[nextNode]=0
            leftlengths[nextNode]=0
            rightoffsprings[nextNode]=0
            leftoffsprings[nextNode]=leftoffsprings[recomsample]
            nextNode=nextNode+1
            #remove recombinant node from active list
            activePairs.remove(recomsample)
        ##mutation event
        else:
            active00=[]
            active01=[]
            active10=[]
            active11=[]
            for ele in activePairs:
                if sample[ele]=="00":
                    active00.append(ele)
                elif sample[ele]=="01":
                    active01.append(ele)
                elif sample[ele]=="10":
                    active10.append(ele)
                else:
                    active11.append(ele)
            for ele in activeRight:
                if sample[ele]=="00":
                    active00.append(ele)
                elif sample[ele]=="01":
                    active01.append(ele)
                elif sample[ele]=="10":
                    active10.append(ele)
                else:
                    active11.append(ele)
            for ele in activeLeft:
                if sample[ele]=="00":
                    active00.append(ele)
                elif sample[ele]=="01":
                    active01.append(ele)
                elif sample[ele]=="10":
                    active10.append(ele)
                else:
                    active11.append(ele)
            mutprob=[sum(m00)/sum(hapmut),sum(m01)/sum(hapmut),sum(m10)/sum(hapmut),sum(m11)/sum(hapmut)]
            muttype=list(numpy.random.multinomial(1,mutprob))
            if muttype.index(1)==0:
                mprob=[m00[0]/sum(m00),m00[1]/sum(m00),m00[2]/sum(m00)]
                type=list(numpy.random.multinomial(1,mprob))
                mutsample=random.sample(active00,1)[0]
                active00.remove(mutsample)
                if type.index(1) == 0:
                    active01.append(nextNode)
                    sample[nextNode]="01"
                elif type.index(1) == 1:
                    active10.append(nextNode)
                    sample[nextNode]="10"
                else:
                    active11.append(nextNode)
                    sample[nextNode]="11"
#                n[0]=n[0]+1
#                n[1]=n[1]-1
            elif muttype.index(1)==1:
                mprob=[m01[0]/sum(m01),m01[1]/sum(m01),m01[2]/sum(m01)]
                type=list(numpy.random.multinomial(1,mprob))
                mutsample=random.sample(active01,1)[0]
                active01.remove(mutsample)
                if type.index(1) == 0:
                    active00.append(nextNode)
                    sample[nextNode]="00"
                elif type.index(1) == 1:
                    active10.append(nextNode)
                    sample[nextNode]="10"
                else:
                    active11.append(nextNode)
                    sample[nextNode]="11"
#                n[0]=n[0]+1
#                n[2]=n[2]-1
            elif muttype.index(1)==2:
                mprob=[m10[0]/sum(m10),m10[1]/sum(m10),m10[2]/sum(m10)]
                type=list(numpy.random.multinomial(1,mprob))
                mutsample=random.sample(active10,1)[0]
                active10.remove(mutsample)
                if type.index(1) == 0:
                    active00.append(nextNode)
                    sample[nextNode]="00"
                elif type.index(1) == 1:
                    active01.append(nextNode)
                    sample[nextNode]="01"
                else:
                    active11.append(nextNode)
                    sample[nextNode]="11"
#                n[0]=n[0]+1
#                n[3]=n[3]-1
            else:
                mprob=[m11[0]/sum(m11),m11[1]/sum(m11),m11[2]/sum(m11)]
                type=list(numpy.random.multinomial(1,mprob))
                mutsample=random.sample(active11,1)[0]
                active11.remove(mutsample)
                if type.index(1) == 0:
                    active00.append(nextNode)
                    sample[nextNode]="00"
                elif type.index(1) == 1:
                    active01.append(nextNode)
                    sample[nextNode]="01"
                else:
                    active10.append(nextNode)
                    sample[nextNode]="10"
#                n[2]=n[2]+1
#                n[3]=n[3]-1
            log="Node "+str(mutsample)+'  was mutated by '+str(nextNode)
            print >> logout, log
            rightparent[mutsample]=nextNode
            leftparent[mutsample]=nextNode
            #creat ancestor node
            rightparent[nextNode]=0
            leftparent[nextNode]=0
            rightlengths[nextNode]=0
            leftlengths[nextNode]=0
            rightoffsprings[nextNode]=0
            rightoffsprings[nextNode]=rightoffsprings[nextNode]+rightoffsprings[mutsample]
            leftoffsprings[nextNode]=0
            leftoffsprings[nextNode]=leftoffsprings[nextNode]+leftoffsprings[mutsample]
            #delete mutation node
            activePairs=list(set(activePairs).difference(set([mutsample])))
            activeLeft=list(set(activeLeft).difference(set([mutsample])))
            activeRight=list(set(activeRight).difference(set([mutsample])))
            #add new ancestor node to list
            if rightoffsprings[nextNode]==0:
                activeLeft.append(nextNode)
            elif leftoffsprings[nextNode]==0:
                activeRight.append(nextNode)
            else:
                activePairs.append(nextNode)
            nextNode=nextNode+1
        if len(activePairs)==0:
                if len(activeRight)==1:
                    activeRight=[]
                if len(activeLeft)==1:
                    activeLeft=[]
        if len(activePairs)==1:
                if len(activeRight) !=0:
                    activeRight.extend(activePairs)
                    activePairs=[]
                if len(activeLeft)!=0:
                    activeLeft.extend(activePairs)
                    activePairs=[]
        activen=len(activePairs)+len(activeLeft)+len(activeRight)
        if activen > 0:
            recon=[0,0,0,0]
            n=[0,0,0,0]
            for ele in activePairs:
                if sample[ele] == "00":
                    recon[0]=recon[0]+1
                    n[0]=n[0]+1
                elif sample[ele] == "01":
                    recon[1] = recon[1]+1
                    n[1]=n[1]+1
                elif sample[ele] == "10":
                    recon[2] = recon[2]+1
                    n[2]=n[2]+1
                else:
                    recon[3] = recon[3]+1
                    n[3]=n[3]+1
            for ele in activeLeft:
                if sample[ele] == "00":
                    n[0]=n[0]+1
                elif sample[ele] == "01":
                    n[1]=n[1]+1
                elif sample[ele] == "10":
                    n[2]=n[2]+1
                else:
                    n[3]=n[3]+1
            for ele in activeRight:
                if sample[ele] == "00":
                    n[0]=n[0]+1
                elif sample[ele] == "01":
                    n[1]=n[1]+1
                elif sample[ele] == "10":
                    n[2]=n[2]+1
                else:
                    n[3]=n[3]+1
            shapfre=n[haplotype.index(Shap)]/float(sum(n))
            diff=[]
            for ele in Shapfrequency:
                diff.append(abs(ele-shapfre))
            value=min(diff)
            T=diff.index(value)
    return leftparent,leftlengths,rightparent,rightlengths,sample,time
def Twolocusneutral(nsam,N,r,mu,region,hapfre,logout):
    sample={}
    n=[int(round(nsam*hapfre[0])),int(round(nsam*hapfre[1])),int(round(nsam*hapfre[2])),int(round(nsam*hapfre[3]))]    
    if sum(n) > nsam:
        n[n.index(max(n))]=n[n.index(max(n))]-1
    active00=range(1,n[0]+1)
    for ele in active00:
        sample[ele]="00"
    active01=range(n[0]+1,sum(n[0:2])+1)
    for ele in active01:
        sample[ele]="01"
    active10=range(sum(n[0:2])+1,sum(n[0:3])+1)
    for ele in active10:
        sample[ele]="10"
    active11=range(sum(n[0:3])+1,sum(n)+1)
    for ele in active11:
        sample[ele]="11"
    #the right hand locus
    time=0
    rightlengths={}
    rightoffsprings={}
    rightparent={}
    #the left hand locus
    leftlengths={}
    leftoffsprings={}
    leftparent={}
    for i in range(1,nsam+1):
        rightlengths[i]=0
        rightoffsprings[i]=1
        rightparent[i]=0
        leftlengths[i]=0
        leftoffsprings[i]=1
        leftparent[i]=0
    #offspring nodes for each node
    activePairs=range(1,nsam+1)
    activeLeft=[] 
    
    activeRight=[]
    nextNode=nsam+1
    while len(activePairs)+max(len(activeLeft),len(activeRight)) > 1:
        # compute the probability of recombination
        activen=len(activePairs)+len(activeLeft)+len(activeRight)
        Rec_pro=r*len(region)*len(activePairs)
        mut_pro=mu*len(region)*activen
        # compute the probability of coalescent
        pca=Pca(activen,N)
        # calculate the time to next event (recombination or coalescent)
        prob=Rec_pro+pca+mut_pro
        t=random.expovariate(prob)
        timet=1
        time=time+timet
        log=str(len(activePairs))+' '+str(len(activeLeft))+' '+str(len(activeRight))+" After "+str(t)+" generations:"
        print >>logout,log
        #update times for all nodes
        indexRight=[]
        if len(activeRight) > 0:
            indexRight.extend(activeRight)
        if len(activePairs) > 0:
            indexRight.extend(activePairs)
        for ele in indexRight:
            rightlengths[ele]=rightlengths[ele]+timet
        indexLeft=[]
        if len(activeLeft) > 0:
            indexLeft.extend(activeLeft)
        if len(activePairs) > 0:
            indexLeft.extend(activePairs)
        for ele in indexLeft:
            leftlengths[ele]=leftlengths[ele]+timet
        #determine the events was coalescent or recombination event?
        event=list(numpy.random.multinomial(1,[Rec_pro/prob,pca/prob,mut_pro/prob]))
        if event.index(1)==1:
            #coalescent event
            #pick two nodes at random coalescent
            active=[]
            if len(activeLeft) > 0:
                active.extend(activeLeft)
            if len(activeRight) > 0:
                active.extend(activeRight)
            if len(activePairs) > 0:
                active.extend(activePairs)
            coalescent=random.sample(active,2)
            log="Nodes "+str(coalescent[0])+" and "+str(coalescent[1])+' coalescent into '+str(nextNode)
            print >>logout,log
            #assign parent node
            overlapRight=list(set(coalescent).intersection(set(indexRight)))
            for ele in overlapRight:
                rightparent[ele]=nextNode
            overlapLeft=list(set(coalescent).intersection(set(indexLeft)))
            for ele in overlapLeft:
                leftparent[ele]=nextNode
            #creat ancestor node
            rightparent[nextNode]=0
            leftparent[nextNode]=0
            rightlengths[nextNode]=0
            leftlengths[nextNode]=0
            rightoffsprings[nextNode]=0
            for ele in overlapRight:
                rightoffsprings[nextNode]=rightoffsprings[nextNode]+rightoffsprings[ele]
            leftoffsprings[nextNode]=0
            for ele in overlapLeft:
                leftoffsprings[nextNode]=leftoffsprings[nextNode]+leftoffsprings[ele]
            #delete coalescent node in list
            activePairs=list(set(activePairs).difference(set(coalescent)))
            activeLeft=list(set(activeLeft).difference(set(coalescent)))
            activeRight=list(set(activeRight).difference(set(coalescent)))
            #add new ancestor node to list
            if rightoffsprings[nextNode]==0:
                activeLeft.append(nextNode)
            elif leftoffsprings[nextNode]==0:
                activeRight.append(nextNode)
            else:
                activePairs.append(nextNode)
            nextNode=nextNode+1
        elif event.index(1) == 0:
            #recombination event
            #pick one node at random to recombine
            if len(activePairs)==1:
                recombinant=activePairs[0]
            else:
                recombinant=random.sample(activePairs,1)[0]
            log="Node "+str(recombinant)+' splits into '+str(nextNode)+" and "+str(nextNode+1)
            print >>logout,log
            #assign different ancestor to recombinant
            rightparent[recombinant]=nextNode
            leftparent[recombinant]=nextNode+1
            activeRight.append(nextNode)
            activeLeft.append(nextNode+1)
            #create ancestor for right portion
            rightparent[nextNode]=0
            leftparent[nextNode]=0
            rightlengths[nextNode]=0
            leftlengths[nextNode]=0
            rightoffsprings[nextNode]=rightoffsprings[recombinant]
            leftoffsprings[nextNode]=0
            nextNode=nextNode+1
            #create ancestor for left portion
            rightparent[nextNode]=0
            leftparent[nextNode]=0
            rightlengths[nextNode]=0
            leftlengths[nextNode]=0
            rightoffsprings[nextNode]=0
            leftoffsprings[nextNode]=leftoffsprings[recombinant]
            nextNode=nextNode+1
            #remove recombinant node from active list
            activePairs.remove(recombinant)
        else:
            active=[]
            if len(activeLeft) > 0:
                active.extend(activeLeft)
            if len(activeRight) > 0:
                active.extend(activeRight)
            if len(activePairs) > 0:
                active.extend(activePairs)
            mutationsample=random.sample(active,1)[0]
            log="Nodes "+str(mutationsample)+' mutated by '+str(nextNode)
            print >>logout,log
            #assign parent node
            rightparent[mutationsample]=nextNode
            leftparent[mutationsample]=nextNode
            #creat ancestor node
            rightparent[nextNode]=0
            leftparent[nextNode]=0
            rightlengths[nextNode]=0
            leftlengths[nextNode]=0
            rightoffsprings[nextNode]=0
            rightoffsprings[nextNode]=rightoffsprings[nextNode]+rightoffsprings[mutationsample]
            leftoffsprings[nextNode]=0
            leftoffsprings[nextNode]=leftoffsprings[nextNode]+leftoffsprings[mutationsample]
            #delete coalescent node in list
            activePairs=list(set(activePairs).difference(set([mutationsample])))
            activeLeft=list(set(activeLeft).difference(set([mutationsample])))
            activeRight=list(set(activeRight).difference(set([mutationsample])))
            activePairs.append(nextNode)
            nextNode=nextNode+1
        ##check for special situation where one locus finishes coalescent
        if len(activePairs)==0:
                if len(activeRight)==1:
                    activeRight=[]
                if len(activeLeft)==1:
                    activeLeft=[]
        if len(activePairs)==1:
                if len(activeRight) !=0:
                    activeRight.extend(activePairs)
                    activePairs=[]
                if len(activeLeft)!=0:
                    activeLeft.extend(activePairs)
                    activePairs=[] 
    return leftparent,leftlengths,rightparent,rightlengths,sample,time
def Tree(lengths,parent,nsam):
    #determine parent nodes
    Tree={}
    Nodes=sorted(parent.keys(),reverse=True)
    parentNodes=range(Nodes[0],nsam-1,-1)
    for ele in parentNodes:
        #determin sun nodes and length of each parent node
        for key, value in parent.iteritems():
            if value == ele:
                Tree.setdefault(ele,{})[key]=lengths[key]
    return Tree
def SepMutation(time,position,leftTree,rightTree,locus1,locus2):
    left=sorted(leftTree.keys(),reverse=True)
    right=sorted(rightTree.keys(),reverse=True)
    parent=sorted(list(set(left).union(set(right))),reverse=True)
    cutoff=locus1+abs(locus1-locus2)/float(2)
    i=0
    offspring={}
    while i < len(parent):
        Start=parent[i]
        if Start in left:
            activeLeft=sorted(leftTree[Start].keys(),reverse=True)
        else:
            activeLeft=[]
        if Start in right:
            activeRight=sorted(rightTree[Start].keys(),reverse=True)
        else:
            activeRight=[]
        if activeLeft == activeRight:
            for ele in activeLeft:
                delttime=max(leftTree[Start][ele],rightTree[Start][ele])
                nseg=numpy.random.binomial(len(position),delttime/float(time))
                position1 = random.sample(position,nseg)
                if offspring.has_key(Start):
                    for key in offspring[Start].keys():
                        offspring.setdefault(ele,{})[key]=offspring[Start][key]
                for pos in position1:
                    if offspring.has_key(Start):
                        if pos in offspring[Start].keys():
                            offspring.setdefault(ele,{})[pos]=offspring[ele][pos]+1
                        else:
                            offspring.setdefault(ele,{})[pos]=1
                    else:
                        offspring.setdefault(ele,{})[pos]=1
        else:
            for ele in activeLeft:
                delttime=leftTree[Start][ele]
                nseg=numpy.random.binomial(len(position),delttime/float(time))
                position1 = random.sample(position,nseg)
                position2=[]
                if offspring.has_key(Start):
                    for pos in offspring[Start].keys():
                        if pos < cutoff:
                            offspring.setdefault(ele,{})[pos]=offspring[Start][pos]       
                for pos in position1:
                    if ele < cutoff:
                        position2.append(pos)
                for pos in position2:
                    if offspring.has_key(Start):
                        if pos in offspring[Start].keys():
                            offspring.setdefault(ele,{})[pos]=offspring[Start][pos]+1
                        else:
                            offspring.setdefault(ele,{})[pos]=1
                    else:
                        offspring.setdefault(ele,{})[pos]=1
            for ele in activeRight:
                delttime=rightTree[Start][ele]
                nseg=numpy.random.binomial(len(position),delttime/float(time))
                position1 = random.sample(position,nseg)
                position2=[]
                if offspring.has_key(Start):
                    for pos in offspring[Start].keys():
                        if pos > cutoff:
                            offspring.setdefault(ele,{})[pos]=offspring[Start][pos]    
                for pos in position1:
                    if ele > cutoff:
                        position2.append(pos)
                for pos in position2:
                    if offspring.has_key(Start):
                        if pos in offspring[Start].keys():
                            offspring.setdefault(ele,{})[pos]=offspring[Start][pos]+1
                        else:
                            offspring.setdefault(ele,{})[pos]=1
                    else:
                        offspring.setdefault(ele,{})[pos]=1
        i=i+1
    return offspring
def hapSequence(position,offmutation,nsam,locus1,locus2,sample,res):
    sampleId=range(1,nsam+1)
    out="//"
    print >> res,out
    out="Segsites: "+str(len(position))
    print >>res,out
    out="Positions: "
    for ele in position:
        out=out+str(ele)+' '
    print >>res, out
    for ID in sampleId:
        out=""
        #output sequence 0: ancestor, 1:derived
        for segsite in position:
            if segsite in offmutation[ID].keys():
                if segsite == locus1:
                    if sample[ID] == "00" or sample[ID] == "01" or offmutation[ID][segsite]%2 == 0:
                        out=out+str(0)
                    else:
                        out=out+str(1)
                elif segsite == locus2:
                    if sample[ID] == "00" or sample[ID] == "10" or offmutation[ID][segsite]%2 == 0:
                        out=out+str(0)
                    else:
                        out=out+str(1)
                else:
                    if offmutation[ID][segsite]%2 == 0:
                        out=out+str(0)
                    else:
                        out=out+str(1)    
            else:
                if segsite == locus1:
                    if sample[ID] == "10" or sample[ID] == "11" :
                        out=out+str(1)
                    else:
                        out=out+str(0)
                elif segsite == locus2:
                    if sample[ID] == "01" or sample[ID] == "11" :
                        out=out+str(1)
                    else:
                        out=out+str(0)
                else:
                        out=out+str(0)
        print >>res, out


    
def main():
    usage = "usage: python %prog <-n sample_number> <-r replication_number> [...]"
    description = "two-SNPs locus evolution backward simulation of selection model. The order of haplotypes should follow 00,01,10 and 11. For example: python %prog -H 01, -s 0.01. If not input selected haplotype (-H) and selective coefficient (-s), neutral model was default."
    op = OptionParser(version="%prog 0.1",description=description,usage=usage,add_help_option=False)
    op.add_option("-h","--help",action="help",
                  help="Show this help message and exit.")
    op.add_option("-n","--sample number",dest="nsam",type="int",default="30",
                  help=" please input the number of simulated samples, default is 30 samples")
    op.add_option("-d","--duplication number",dest="nrep",type="int", default="1",
                  help=" please input the replication number of simulated samples, default is 1")
    op.add_option("-l","--region length",dest="region",type="int", default="10000",
                  help="please input the length of simulated region (bp), default is 10000")
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
    op.add_option("-H","--selective advantage haplotype" , dest="H",type="str",
                  help="please specified the haplotype which was selected in evolution,for example 10;")
    op.add_option("-S","--selection coefficient",dest="s",type="float",
                  help="please input the select coefficient of haplotype which specified previous, default was 0 represent neutral model. ")
    op.add_option("-o","--outfilename",dest="outfilename",type="str",default="simulation.out",
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
    if not options.H and not options.s:
        print "You did not specify the selected haplotype!"
        Shap=haplotype[hapfre.index(max(hapfre))]
        S=0
    elif not options.H:
        print "Please input the haplotype corresponding to the selective coefficient, one from 00,01,10 and 11."
        sys.exit(1)
    elif not options.s:
        print "You did not input the selected coefficient of specificed haplotype."
        S=0
    else:
        Shap=options.H
        S=options.s
        if Shap not in haplotype:
            print "The type of -H was error!"
            sys.exit(1)
    nsam = options.nsam
    nrep=options.nrep
    region=range(0,options.region)
    N=17469
    mu=options.mu
    r=options.R
    outputfilename=options.outfilename
    if os.path.exists(outputfilename):
        os.remove(outputfilename)
    if nsam >=N:
        N = nsam
    outputfilename=options.outfilename
    if os.path.exists(outputfilename):
        os.remove(outputfilename)
    #------step 1: Backward tracjory of haplotype frequency in time-----------
    res=open(os.path.join(os.getcwd(),outputfilename),'wb')
    frequencyfilename=options.frequencyfilename
    trac=open(os.path.join(os.getcwd(),frequencyfilename),'wb')
    logout=open(os.path.join(os.getcwd(),"log.out"),'wb')
    for t in range(nrep):
        if not options.two_locus:
            two_locus=sorted(random.sample(region,2))
        else:
            two_locus=[]
            for ele in list(options.two_locus):
                two_locus.append(int(ele))
            two_locus=sorted(two_locus)
        theta=r*abs(two_locus[1]-two_locus[0])
        v=mu/(len(hapfre)-1)
        hapfit=((1+S)-(1+S*hapfre[haplotype.index(Shap)]))/(1+S*hapfre[haplotype.index(Shap)])
        deltfre=[]
        for ele in haplotype:
            if ele == Shap:
                mean=v-(mu+v)*hapfre[haplotype.index(ele)]+hapfit
            else:
                mean=v-(mu+v)*hapfre[haplotype.index(ele)]
            deltfre.append(mean)
        Haptrac=Hapftrac(hapfre,Shap,haplotype,deltfre,N)
        Shapfrequency=[]
        for key in sorted(Haptrac.keys()):
            Shapfrequency.append(Haptrac[key][Shap])
        print "Print the track file of haplotype frequency"
        
        out="T"+"\t"+"00"+"\t"+"01"+"\t"+"10"+"\t"+"11"
        print >> trac,out
        for ele in Haptrac.keys():
            out=str(ele)+"\t"
            for key in sorted(Haptrac[ele].keys()):
                out=out+str(Haptrac[ele][key])+"\t"
            print >> trac,out
    

    #-----------step 2: Coalescent process ----------------
        locus1=two_locus[0]
        locus2=two_locus[1]
        print "Simulation the offspring"
        if S!=0:
            (leftparent, leftlengths,rightparent,rightlengths,sample,time)=Hapbackward(nsam,N,mu,Haptrac,theta,hapfre,Shap,locus1,locus2,haplotype,region,Shapfrequency,r,logout)
        else:
            (leftparent, leftlengths,rightparent,rightlengths,sample,time)=Twolocusneutral(nsam,N,r,mu,region,hapfre,logout)
        leftTree=Tree(leftlengths,leftparent,nsam)
        rightTree=Tree(rightlengths,rightparent,nsam)
        print "simulation the "+str(t)+"th replication"
        if not options.segsites:
            segsites = numpy.random.poisson(len(region)/100, 1)[0]+2
            position=random.sample(region,segsites)
            if locus1 not in position:
                position.append(locus1)
            if locus2 not in position:
                position.append(locus2)
        else:
            segsites = options.segsites
            position=random.sample(region,segsites)
            if locus1 not in position:
                position.append(locus1)
            if locus2 not in position:
                position.append(locus2)
            l1=position.index(locus1)
            l2=position.index(locus2)
            positionindex=range(0,len(position))
            positionindex.remove(l1)
            positionindex.remove(l2)
            if len(position) > segsites:
                rs=random.sample(positionindex,(len(position)-segsites))
            for ele in rs:
                position.remove(position[ele])
        position=sorted(position)
        offmutation=SepMutation(time,position,leftTree,rightTree,locus1,locus2)  
        hapSequence(position,offmutation,nsam,locus1,locus2,sample,res)
        print " A region of "+str(options.region)+'bp include '+str(len(position))+" segsites were simulated  with sample size "+str(nsam)+' for '+str(t+1)+' replication.'

if __name__ == "__main__":
    
    try:
        main()
    except KeyboardInterrupt:
        sys.stderr.write("User interrupt me, see you!\n")
        sys.exit(0)    

