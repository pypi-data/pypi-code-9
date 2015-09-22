#!/usr/bin/env python

'''This script plots tables as a pdf. The type of plot is determined
    based on the columns in the input dataframe.'''
from __future__ import division
#Our standard Modules
import argparse
import numpy as np
import sys

import pandas as pd
import sortseq.utils as utils
import matplotlib.pyplot as plt
import weblogolib
import matplotlib as mpl
from scipy.optimize import newton


def draw_from_to(df,seq_dict,inv_dict):
    '''Plot probabilities of mutation of 1 type of base to another.'''
    L = len(seq_dict)    
    mutarr = np.zeros([L,L])
    for z in range(L):        
        mutarr[:,z] = df['mut'][z*L:(z+1)*L]
    #now plot
    fig, ax = plt.subplots()
    plt.pcolor(mutarr, cmap=plt.cm.coolwarm)
    ax.set_xticks(np.arange(L)+0.5, minor=False)
    ax.set_yticks(np.arange(L)+0.5, minor=False)
    ax.set_xticklabels([inv_dict[z] for z in range(L)], minor=False)
    ax.set_yticklabels([inv_dict[z] for z in range(L)], minor=False)
    plt.title('Mutation Rate',fontsize=20)
    plt.xlabel('Sequence Base',fontsize=20)
    plt.ylabel('Wild Type Base',fontsize=20)
    return fig

def draw_library(df,seq_dict):
    '''Make a Zipf plot of number vs rank order.'''
    fig, ax = plt.subplots()
    df = df.sort(columns='ct',ascending=False)
    ax.loglog(range(len(df['ct'])),df['ct'])
    plt.title('Zipf Frequency Plot',fontsize=20)
    plt.xlabel('Rank Order of Counts',fontsize=20)
    plt.ylabel('Counts',fontsize=20)
    return fig

def draw_enrichment_profile(df,seq_dict,inv_dict):
    '''For proteins, make a plot of enrichment of each residue 
        at each position.'''
    fig,ax = plt.subplots()
    column_headers = ['le_' + str(inv_dict[i]) for i in range(len(seq_dict))]
    #set special color for NaN values
    masked_array = np.ma.array(
        df[column_headers], mask=np.isnan(df[column_headers]))
    cmap = mpl.cm.coolwarm
    cmap.set_bad('w',1.)
    
    plt.pcolor(masked_array, cmap=cmap)
    ax.set_xticks(np.arange(len(seq_dict))+0.5, minor=False)
    ax.set_yticks(np.arange(len(df['pos']))+0.5, minor=False)
    plt.colorbar()
    
    ax.set_xticklabels([inv_dict[z] for z in range(len(seq_dict))], minor=False)
    ax.set_yticklabels(df['pos'], minor=False)
    plt.title('Enrichment Profile',fontsize=20)
    plt.xlabel('Amino Acid',fontsize=20)
    plt.ylabel('Position',fontsize=20)
    return fig

def draw_info_profile(df):
    '''Draw bar chart of mutual information btw position identity and batch.'''
    fig = plt.figure()
    ax = fig.add_subplot(111)
    df['pos'] = [a - .45 for a in df['pos']]
    ax.bar(df['pos'],df['val_info'],color = 'b',yerr=df['std_info'])
    plt.xlabel('Base Position',fontsize = 20)
    plt.ylabel('Mutual Information (bits)', fontsize = 20)
    figtitle = 'Information Profile'
    plt.title(figtitle, fontsize = 22)   
    return fig

def draw_mutrate(df):
    '''Plot total mutation rate at each position'''
    '''Draw bar chart of mutual information btw position identity and batch.'''
    fig = plt.figure()
    ax = fig.add_subplot(111)
    df['pos'] = [a - .45 for a in df['pos']]
    ax.bar(df['pos'],df['mut'],color = 'b',yerr=df['mut_err'])
    plt.xlabel('Base Position',fontsize = 20)
    plt.ylabel('Mutation Rate', fontsize = 20)
    figtitle = 'Mutation Profile'
    plt.title(figtitle, fontsize = 22)   
    return fig

def draw_matrix(df,seq_dict,inv_dict):
    '''Draw heatmap of linear energy matrix.'''
    column_headers = ['val_' + inv_dict[i] for i in range(len(seq_dict))]
    data = np.transpose(np.array(df[column_headers]))
    data = data - data.min(axis=0)
    fig, ax1 = plt.subplots()
    ax1.imshow(data,interpolation='nearest')
      
    ax1.set_xlabel('Position w.r.t. transcription start site')
    ax1.set_yticks(range(len(seq_dict)))
    ax1.set_yticklabels([seq_dict[inv_dict[i]] for i in range(len(seq_dict))])
    indices = np.arange(0,len(df['pos']),5)
    xtick_labels = list(df['pos'][indices])
    ax1.set_xticks(indices)
    ax1.set_xticklabels(xtick_labels)
    return fig

def PSSM_info(x,matrix):
    '''Calculate the mutual information contained in a PSSM'''
    L_matrix = matrix.shape[1]
    temp_pssm = utils.get_PSSM_from_weight_matrix(matrix,x)
    info = utils.compute_PSSM_self_information(temp_pssm)
    return info-L_matrix

def draw_logo_from_matrix(df,seq_dict,inv_dict):
    '''Display energy matrix as a logo.'''
    column_headers = ['val_' + inv_dict[i] for i in range(len(seq_dict))]
    matrix = np.transpose(np.array(df[column_headers]))
    matrix = utils.fix_matrix_gauge(matrix)
    rename_headers = ['freq_' + inv_dict[i] for i in range(len(seq_dict))]
    '''We need to supply a scalar to determine pssm total info, 
        we want total info content of approx 1 bit per basepair, 
        so we will solve info - L  = 0'''
    optimal_x = newton(PSSM_info,x0=19,args=(matrix,))
    pssm_df = pd.DataFrame(
        np.transpose(utils.get_PSSM_from_weight_matrix(matrix,optimal_x)),
        columns=rename_headers)
    pssm_df = pd.concat([df['pos'],pssm_df],axis=1)
   
    myimage = draw_logo(pssm_df,seq_dict,inv_dict)
    return myimage

def draw_pairwise_info(df,seq_dict):
    '''Display mutual information between a base being mutated at one position
        and a base being mutated at another. If there is a large amount of 
        mutual info, then the library might be unusable.'''
    L = 1 + df['pos_0'].max()-df['pos_0'].min()
    MI = np.zeros([L,L])
    for z, r in df.iterrows():
        MI[r['pos_0'],r['pos_1']] = r['MI']
        #Matrix will be symmetric
        MI[r['pos_1'],r['pos_0']] = r['MI']
    fig, ax = plt.subplots()
    plt.pcolor(MI, cmap=plt.cm.coolwarm)
    plt.colorbar()
    #cb.set_label('gdp_md_est')
    indices = np.arange(0,L,5)
    labels = np.arange(df['pos_0'].min(),df['pos_0'].max(),5)
    ax.set_xticks(indices+0.5, minor=False)
    ax.set_yticks(indices+0.5, minor=False)    
    ax.set_xticklabels(labels, minor=False)
    ax.set_yticklabels(labels, minor=False)
    plt.title('Information Between Base Mutations',fontsize=20)
    plt.xlabel('Position 1',fontsize=20)
    plt.ylabel('Position 2',fontsize=20)
    return fig


def draw_counts(df,seq_dict,inv_dict):
    '''Draw heatmap of counts of each base at each position.'''
    L = len(df['pos'])
    column_headers = ['ct_' + inv_dict[i] for i in range(len(seq_dict))]
    counts_arr = np.transpose(np.array(df[column_headers]))
         
    fig, ax = plt.subplots()
    plt.pcolor(counts_arr,cmap=plt.cm.coolwarm)
    indices = np.arange(0,len(df['pos']),5)
    xtick_labels = list(df['pos'][indices])
    ax.set_xticks(indices)
    ax.set_xticklabels(xtick_labels)
    ax.set_yticks(np.arange(len(seq_dict))+0.5, minor=False)
    ax.set_yticklabels([inv_dict[i] for i in range(len(seq_dict))], minor=False)
    plt.title('Mutation Profile',fontsize=20)
    plt.xlabel('Position',fontsize=20)
    plt.ylabel('Counts',fontsize=20)
    return fig

def draw_logo(df,seq_dict,inv_dict):
    '''Draw logo of sequences.'''
    #right now can only deal with dna
    al = weblogolib.unambiguous_dna_alphabet
    column_headers = ['freq_' + inv_dict[i] for i in range(len(seq_dict))]
    counts_arr = np.array(df[column_headers])
    data = weblogolib.LogoData.from_counts(al,counts_arr)
    
    #Set Logo options
    '''stack width in points, not default size of 10.8, but set to this 
        in weblogo call below'''
    stackwidth = 9.5 
    barheight = 5.5 # height of bars in points if using overlay
    barspacing = 2.0 # spacing between bars in points if using overlay
    '''ratio of stack height:width, doesn't count part going 
        over maximum value of 1'''
    stackaspectratio = 4.4 
    ymax = 1.0 
    logo_options = weblogolib.LogoOptions()
    logo_options.fineprint = None
    #logo_options.stacks_per_line = nperline
    logo_options.stack_aspect_ratio = stackaspectratio
    logo_options.show_errorbars = True
    
    logo_options.errorbar_fraction = .75
    logo_options.errorbar_gray = .9
    logo_options.errorbar_width_fraction = .9
    logo_options.stack_width = stackwidth
    #Command to uncomment if you want each column to have height = 1
    #logo_options.unit_name = 'probability'
    logo_options.show_yaxis = False
    #logo_options.yaxis_scale = ymax 


    #for dna
    colormapping = {}
    colormapping['A'] = '#008000'
    colormapping['T'] = '#FF0000'
    colormapping['C'] = '#0000FF'
    colormapping['G'] = '#FFA500'
    
    color_scheme = weblogolib.colorscheme.ColorScheme()
    for x in [inv_dict[i] for i in range(len(seq_dict))]:
       color_scheme.groups.append(
       weblogolib.colorscheme.ColorGroup(x, colormapping[x], "'%s'" % x))
    logo_options.color_scheme = color_scheme

    #set logo format and output
    myformat = weblogolib.LogoFormat(data,logo_options)
    myimage = weblogolib.pdf_formatter(data,myformat)   
    return myimage

def draw_compare_predictive_info(df,title=None):
    '''Draws a heat map of predictive info between Test data sets and models.
        The values displayed will be normalized by the maximum values in each
        column.'''
    #Get row labels, then Remove lableing column
    exprows = df['Training/Test']
    try:
        df.drop('Training/Test',axis=1,inplace=True)
    except:
        pass
    normalization = df.max(axis=0)
    normalized_df = df.div(normalization,axis=1)
    expcolumns = df.columns
    
    
    fig, ax = plt.subplots()
    heatmap = ax.pcolor(normalized_df, cmap=plt.cm.coolwarm,vmax=1,vmin=0)
    fig.set_figheight(10)
    fig.set_figwidth(15)
    cbar = plt.colorbar(heatmap)
    #cbar.set_label('Mutual Information', rotation=270)
    ax.set_xticks(np.arange(len(expcolumns))+0.5, minor=False)
    ax.set_yticks(np.arange(len(exprows))+0.5, minor=False)
    ax.set_xticklabels([expcolumns[z] for z in range(len(expcolumns))], minor=False)
    ax.set_yticklabels([exprows[z] for z in range(len(exprows))], minor=False)
    if title:
        plt.title('Model Comparison ' + title,fontsize=20)
    plt.xlabel('Test Data Set',fontsize=20)
    plt.ylabel('Training Data Set',fontsize=20)
    return fig

def draw_pairwise2(df):
    masked_array = np.ma.array(
        df, mask=np.isnan(df))
    fig, ax = plt.subplots()
    heatmap = ax.pcolor(masked_array, cmap=plt.cm.coolwarm,vmax = .5,vmin=0)
    cbar = plt.colorbar(heatmap)
    plt.xlabel('Position')
    plt.ylabel('Position')
    return fig

def main(df,dicttype,logo=False,title=None,pairwise=False):
    seq_dict,inv_dict = utils.choose_dict(dicttype)
    matrix_headers = ['val_' + inv_dict[i] for i in range(len(seq_dict))]
    columns = df.columns
    '''some functions can be output through plt.savefig, others must 
        be output via a write method'''
    output_via_write = False 
    #Autodetect the type of draw function to use.
    if {'ct','seq'}.issubset(columns):
        myimage = draw_library(df,seq_dict)
    elif pairwise == True:
        myimage = draw_pairwise2(df)
    elif {'pos_0','pos_1','MI'}.issubset(columns):
        myimage = draw_pairwise_info(df,seq_dict)
    elif (set(matrix_headers).issubset(columns) and not logo):
        myimage = draw_matrix(df,seq_dict,inv_dict)
    elif (set(matrix_headers).issubset(columns) and logo):
        myimage = draw_logo_from_matrix(df,seq_dict,inv_dict)
        output_via_write = True
    elif set(['freq_' + inv_dict[i] for i in range(len(seq_dict))]).issubset(columns):
        myimage = draw_logo(df,seq_dict,inv_dict)
        output_via_write = True
    elif set(['ct_' + inv_dict[i] for i in range(len(seq_dict))]).issubset(columns):
        myimage = draw_counts(df,seq_dict,inv_dict)
    elif {'pos','val_info'}.issubset(columns):
        myimage = draw_info_profile(df)
    elif {'wt','obs','mut'}.issubset(columns):
        myimage = draw_from_to(df,seq_dict,inv_dict)
    elif {'pos','mut'}.issubset(columns):
        myimage = draw_mutrate(df)
    elif {'pos','wt','le_A','le_C'}.issubset(columns):
        myimage = draw_enrichment_profile(df,seq_dict,inv_dict)
    elif {'Training/Test'}.issubset(columns):
        myimage = draw_compare_predictive_info(df,title=title)
    return myimage,output_via_write

# Define commandline wrapper
def wrapper(args):
    
    dicttype = args.type
    logo = args.logo
    # Run funciton
    if args.i:
        df = pd.io.parsers.read_csv(args.i,delim_whitespace=True)
    else:
        df = pd.io.parsers.read_csv(sys.stdin,delim_whitespace=True)
    
    
    myimage,output_via_write = main(df,dicttype,logo=args.logo,title=args.title,pairwise=args.pairwise)
    
    

    if args.out:
        outloc = open(args.out,'w')
    else:
        outloc = sys.stdout
    if not output_via_write:
        plt.savefig(outloc,format='pdf')
    else:
        outloc.write(myimage)
        outloc.close()

# Connects argparse to wrapper
def add_subparser(subparsers):
    p = subparsers.add_parser('draw')
    p.add_argument('-p','--pairwise',action='store_true')
    p.add_argument('-w','--wtseq',default=None,help ='Wild Type Sequence')
    p.add_argument('--logo',action='store_true',help='Draw matrix as logo')
    p.add_argument('-i', '--i', default=None,help='''Input file, otherwise input
        through the standard input.''')
    p.add_argument('--title',default=None,type=str)
    p.add_argument('-t', '--type', choices=['dna','rna','protein'], default='dna')
    p.add_argument('-o', '--out', default=None)
    p.set_defaults(func=wrapper)
