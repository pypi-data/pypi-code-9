#!/usr/bin/env python
from __future__ import division
#Our standard Modules
import argparse
import sys
import os
'''A Script which accepts a data frame with collumns ct_0, ct_1, tag, seq and 
    finds the standard deviation of lr by using seqs with multiple tags.'''
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
import scipy as sp
from Bio.SubsMat import MatrixInfo as matlist
from Bio import pairwise2
from Bio import SeqIO
import pandas as pd
import numpy as np
import sortseq.utils as utils

def wrapper(args):
    #First Quality filter
    matrix = matlist.blosum62
    if args.quality:
        fname = ''.join(['qcfilt_',args.forward.strip('.gz')])
        
        os.system('gunzip -c %s | fastq_quality_filter -q 20 -p 25 -o %s' % (args.forward,fname))
        if args.reverse: 
            rname = ''.join(['qcfilt_',args.reverse.strip('.gz')])
            os.system('fastq_quality_filter -q 20 -p 25 -i %s -o %s' % (args.reverse,rname))

    if args.split:
        #if file is compressed then unpack it for analysis
        if (args.forward).endswith('.gz'):
             if 'fastq' in args.forward:
                 os.system('gunzip -c %s | fastq_to_fasta -o tempforward.fasta' % (args.forward))
                 if args.reverse:
                     os.system('gunzip -c %s | fastq_to_fasta -o tempreverse.fasta' % (args.reverse))
             else:
                 os.system('gunzip -c %s > tempforward.fasta' % args.forward)
                 if args.reverse:
                     os.system('gunzip -c %s > tempreverse.fasta' % (args.reverse))
        else:
            if 'fastq' in args.forward:
                os.system('fastq_to_fasta -i %s -o tempforward.fasta' % (args.forward))
                if args.reverse:
                    os.system('fastq_to_fasta -i %s -o tempreverse.fasta' % (args.reverse))
            else:
                os.system('fasta_renamer -i %s -o tempforward.fasta -n COUNT' %args.forward)
                if args.reverse:
                    os.system('fastx_renamer -i %s -o tempreverse.fasta -n COUNT' %args.reverse)
            
        os.system(
                '''cat  tempforward.fasta | fastx_barcode_splitter.pl --exact --bcfile %s --prefix %s --bol''' %(args.bcfile_F,args.prefix +'_F'))
        if args.reverse:
            os.system(
                '''cat  tempreverse.fasta | fastx_barcode_splitter.pl --exact --bcfile %s --prefix %s --bol''' %(args.bcfile_R,args.prefix + '_R'))
        os.system('rm tempforward.fasta')
        if args.reverse:
            os.system('rm tempreverse.fasta')
    
    def align2(myseq):
        testLHS = np.array(list(myseq[5:5+len(LHS)]))
        testRHS = np.array(list(myseq[-len(RHS):]))
        if ((testLHS != LHS).sum() < 2 and (testRHS != RHS).sum() < 2):
            return 1
        else:
            return np.NaN
    
    if args.check_alignment:
        filelist = pd.io.parsers.read_csv(args.wtfile,delim_whitespace=True)
        for i,item in enumerate(filelist.iterrows()):
            LHS = np.array(list(item[1]['LHS']))
            RHS = np.array(list(item[1]['RHS']))
            print item[1]['file']
            df = pd.io.parsers.read_csv(item[1]['file'],delim_whitespace=True)
            
            df['good'] = df['seq'].apply(align2)
            df.dropna(inplace=True)
            pd.set_option('max_colwidth',int(1e8)) # Make sure columns are not truncated
            df.to_string(
                open(item[1]['file'],'w'), index=False,col_space=10,float_format=utils.format_string)

    if args.check_alignment_max:                    
        filelist = pd.io.parsers.read_csv(args.wtfile,delim_whitespace=True)
        for i,item in enumerate(filelist.iterrows()):
            df = pd.io.parsers.read_csv(item[1]['file'],delim_whitespace=True)
            dfc = df.copy()
            dfc['LHS'] = df['seq'].str.slice(5,17)
            dfc['RHS'] = df['seq'].str.slice(-10,None)
            
            LHS_counts = dfc['LHS'].value_counts()
            RHS_counts = dfc['RHS'].value_counts()
            LHS_counts.sort()
            RHS_counts.sort()
            LHS = np.array(list(LHS_counts.index[-1]))
            
            RHS = np.array(list(RHS_counts.index[-1]))
            print LHS
            print RHS
            df['good'] = df['seq'].apply(align2)
            df.dropna(inplace=True)
            pd.set_option('max_colwidth',int(1e8)) # Make sure columns are not truncated
            df.to_string(
                open(item[1]['file']+'_aligned','w'), index=False,col_space=10,float_format=utils.format_string)

    if (args.combine):        
        
        wtseqs = pd.io.parsers.read_csv(args.wtfile,delim_whitespace=True)
        
        for i,name in enumerate(wtseqs['forward_file']):
            print name
            for_dict = SeqIO.to_dict(SeqIO.parse(name,'fasta'))
            rev_dict = SeqIO.to_dict(SeqIO.parse(wtseqs['reverse_file'][i],'fasta'))
            Lwtseq = wtseqs['wtlength'][i]
            overlap = wtseqs['readlength'][i]*2 - Lwtseq
            offset = wtseqs['readlength'][i] - overlap # index of first base for which both sequences have a read
            aln_file = open(name + '_comb','w')
            for i in for_dict.keys():
                try:
                    forward_record = for_dict[i]
                    reverse_record = rev_dict[i]
                    reverse_record_rc = reverse_record.reverse_complement()
                    
                    combined_record = forward_record[:offset] + reverse_record_rc
                    if str(forward_record[offset:offset+overlap].seq) == str(reverse_record_rc[:overlap].seq):
                        print 'hi'
                        SeqIO.write(combined_record,aln_file,'fasta')
                except:
                    pass
            aln_file.close()   
    
        
# Connects argparse to wrapper
def add_subparser(subparsers):
    p = subparsers.add_parser('preprocess')
    p.add_argument('--split',action='store_true')
    p.add_argument('--all',action='store_true')
    p.add_argument('--combine',action='store_true')
    p.add_argument('--quality',action='store_true')
    p.add_argument('--check_alignment',action='store_true')
    p.add_argument('--check_alignment_max',action='store_true')
    p.add_argument(
        '-wt', '--wtfile', help ='''wt sequences file for removing sequences with
        insertions or deletions''')
    p.add_argument(
        '-bc_F', '--bcfile_F', help ='barcode file')
    p.add_argument(
        '-bc_R', '--bcfile_R', help ='barcode file')
    p.add_argument(
        '-f','--forward',help='forward read file')
    p.add_argument(
        '-r', '--reverse', help='reverse read file')
    p.add_argument('--prefix', help='Save prefix')
    p.add_argument('--readlength',type=int,help='''Paired end read length for combining''')
    p.set_defaults(func=wrapper)
