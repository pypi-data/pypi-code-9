#!/usr/bin/env python
#Last-modified: 19 Oct 2015 12:14:25 PM

#         Module/Scripts Description
# 
# Copyright (c) 2008 Yunfei Wang <Yunfei.Wang1@utdallas.edu>
# 
# This code is free software; you can redistribute it and/or modify it
# under the terms of the BSD License (see the file COPYING included with
# the distribution).
# 
# @status:  experimental
# @version: 1.0.0
# @author:  Yunfei Wang
# @contact: yfwang0405@gmail.com

# ------------------------------------
# python modules
# ------------------------------------

import os
import sys
from ngslib import IO
from itertools import chain

# ------------------------------------
# constants
# ------------------------------------

# ------------------------------------
# Misc functions
# ------------------------------------

def str_format(slst):
    cnt = 0
    lstr = []
    for ss in slst.split(';'):
        sss = ss.split(",")
        lstr.append(",".join(['{'+str(i)+'}' for i in range(cnt,cnt+len(sss))]))
        cnt += len(sss)
    return ";".join(lstr)
def find_all_pairs(workdir): # for TCGA data
    pairs = {}
    for f in os.listdir(workdir):
        if f.endswith('_junc.txt'):
            f = f.replace('_junc.txt','')
            key = f[:-3]
            pairs.setdefault(key,[])
            pairs[key].append(f+'.txt')
    lstr = ";".join([','.join(sorted(pairs[key])) for key in pairs])
    return lstr


# ------------------------------------
# Classes
# ------------------------------------

# ------------------------------------
# Main
# ------------------------------------

if __name__=="__main__":
    if len(sys.argv)==1:
        sys.exit("Example:"+sys.argv[0]+" junc1_rp1.txt,junc1_rep2.txt;junc2_rep1.txt,junc2_rep2.txt;...")
    
    matrix = {}
    junclst = []
    if not (',' in sys.argv[1] or ';' in sys.argv[1]): # samples provided
        sys.argv[1] = find_all_pairs(sys.argv[1]) # a folder is provided
    fstr = str_format(sys.argv[1])
    samples = list(chain(*[ss.split(',') for ss in sys.argv[1].split(';')]))
    L = len(samples)
    for i,f in enumerate(samples):
        junclst.append(f.rstrip(".txt"))
        for item in IO.BioReader(f,ftype='bed',skip=1):
            key = "{0}\t{1}\t{2}".format(item.chrom,item.start,item.stop)
            matrix.setdefault(key,[item] + ['0']*(2*L))
            matrix[key][i+1] = str(int(item.score)) # depth
            matrix[key][i+1+L] = item.otherfields[1] # bam depth
            matrix[key][0] = item
    print "#chrom\tstart\tend\tID\tpercent(%)\tstrand\tcount\tCoverage:{0}\tsite\tBam_support\tGeneID\tTransID\tEsbl_GeneID\tEsbl_TransID\tLocation".format(fstr.format(*junclst))
    tcga_type_keys = [f.split('_')[1] for f in junclst]
    for i,value in enumerate(matrix.values()):
        value[0].id = "Junc_{0}".format(i+1)
        value[0].otherfields[1] = fstr.format(*value[L+1:])
        value[0].score = (L-sum([v=='0' for v in value[L+1:]]))/float(L)*100.
        tcga_types = {}
        for t,d,b in zip(tcga_type_keys,value[L+1:],value[1:L+1]):
            tcga_types.setdefault(t,0)
            tcga_types[t] += 1 if d>b else 0
        tcga_type_str = "ALL:{0};".format(L)+";".join(["{0}:{1}".format(k,v) for k,v in tcga_types.iteritems()])
        print str(value[0])+"\t"+tcga_type_str+"\t"+fstr.format(*value[1:L+1])+"\t"+"\t".join(value[0].otherfields)



