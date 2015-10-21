#!/usr/bin/env python
#Last-modified: 19 Oct 2015 02:23:11 PM

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
import time
import pickle
from ngslib import IO,Bed,DB
from ncshunter import SplicedGene
# ------------------------------------
# constants
# ------------------------------------

# ------------------------------------
# Misc functions
# ------------------------------------
def reAnno(lstr,IDs):
    items = lstr.split('\t')
    # IDs[tid]['transcript_name']
    try:
        gid = IDs[items[1]]['transcript_name']
    except:
        gid = items[0]
    items.insert(2,gid) 
    return "\t".join(items)

# ------------------------------------
# Classes
# ------------------------------------

# ------------------------------------
# Main
# ------------------------------------

if __name__=="__main__":
    if len(sys.argv)==1:
        sys.exit("Example:"+sys.argv[0]+" junctions.tsv > annotated_junctions.tsv")
    IO.converters['splicing'] = SplicedGene
    db = DB('/scratch/bcb/ywang52/TData/genomes/hg19/gencode19/GRCh37.p13.genome.fa','fasta')
    gdb = DB('/scratch/bcb/ywang52/TData/genomes/hg19/gencode19/gencode.v19.mRNA_lncRNA_rsem.gpd.gz','genepred')
    IDs = pickle.load(open("/scratch/bcb/ywang52/TData/genomes/hg19/gencode19/gencode.v19.chr_patch_hapl_scaff.annotation.gtf.gz.dump",'rb'))
    print "Ensembl_id\ttranscript_id\ttranscript_name\tstrand\tCDSLength\tjunction\tpercent(%)\tjunc_trans_start\tjunc_trans_stop\tjunc_status\tjunc_details"

    for junc in IO.BioReader(sys.argv[1],'bed'):
        for gene in junc.fetchDB(gdb,converter="splicing"):
            lstr = gene.findChange(db,junc)
            if lstr:
                print reAnno(lstr,IDs)
    db.close()
    gdb.close()    

