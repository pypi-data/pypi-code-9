#!/usr/bin/env python
#Last-modified: 19 Aug 2015 11:07:47 PM

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

# ------------------------------------
# constants
# ------------------------------------

# ------------------------------------
# Misc functions
# ------------------------------------

# ------------------------------------
# Classes
# ------------------------------------

# ------------------------------------
# Main
# ------------------------------------

if __name__=="__main__":
    if len(sys.argv)==1:
        sys.exit("Example:"+sys.argv[0]+" junc1.txt junc2.txt ... ")
    matrix = {}
    L = len(sys.argv) -1
    junclst = []
    for i,f in enumerate(sys.argv[1:]):
        junclst.append(f.rstrip(".txt"))
        for item in IO.BioReader(f,ftype='bed',skip=1):
            key = "{0}\t{1}\t{2}".format(item.chrom,item.start,item.stop)
            matrix.setdefault(key,[item] + ['0']*(3*L))
            matrix[key][i+1] = '1'
            matrix[key][i+1+L] = str(int(item.score))
            matrix[key][i+1+2*L] = item.otherfields[1]
            matrix[key][0] = item
    print "#chrom\tstart\tend\tID\tscore\tstrand\t{0}\tCoverage\tsite\tBam_support\tGeneID\tTransID\tEsbl_GeneID\tEsbl_TransID\tLocation".format(";".join(junclst))
    for i,value in enumerate(matrix.values()):
        value[0].id = "Junc_{0}".format(i+1)
        value[0].otherfields[1] = ";".join(value[2*L+1:])
        print str(value[0])+"\t"+';'.join(value[1:L+1])+"\t"+";".join(value[L+1:2*L+1])+"\t"+"\t".join(value[0].otherfields)



