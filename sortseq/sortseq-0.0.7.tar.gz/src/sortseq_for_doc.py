#!/usr/bin/env python2.7

''' Primary function for sortseqtools. Currently supports: 

simulate_library
simulate_sublib
simulate_sortseq
simulate_selection
simulate_mpra

select_experiment
select_bin
select_bins
select_window

utils_tally
utils_convert
utils_getaligned
utils_getvalid

estimate_entropy
estimate_mi
estiamte_totalinfo
estimate_precictiveinfo

quantify_avgbin
quantify_enrichment

marginalize_count
marginalize_mutrate
marginalize_enrichment
marginalize_infofootprint

visualize_logo
visualize_enrichment
visualize_infofootprint

model_leastsquares
model_lasso
model_infomax
'''

from __future__ import division
import numpy as np
import scipy as sp
import argparse
import sys
import csv

# sst only works at the commandline


# Create argparse parser. 
parser = argparse.ArgumentParser()

# All functions can specify and output file. Default is stdout.
parser.add_argument('-o','--out',default=False,help='Output location/type, by default it writes to standard output, if a file name is supplied it will write to a text file')


# Add various subcommands individually viva subparsers
subparsers = parser.add_subparsers()

# preprocess
import sortseq.preprocess as preprocess
preprocess.add_subparser(subparsers)

# BIC_selection
import sortseq.BIC_selection as BIC_selection
BIC_selection.add_subparser(subparsers)

# simulate_library
import sortseq.simulate_library as simulate_library
simulate_library.add_subparser(subparsers)

# simulate_sublibrary
import sortseq.simulate_sublibrary as simulate_sublibrary
simulate_sublibrary.add_subparser(subparsers)

#gather_seqs
import sortseq.gatherseqs as gatherseqs
gatherseqs.add_subparser(subparsers)

#select_window
import sortseq.select_window as select_window
select_window.add_subparser(subparsers)

#simulate_expression
import sortseq.simulate_evaluate as simulate_evaluate
simulate_evaluate.add_subparser(subparsers)

#simulate_sorting
import sortseq.simulate_sort as simulate_sort
simulate_sort.add_subparser(subparsers)

#simulate_expression
import sortseq.simulate_expression as simulate_expression
simulate_expression.add_subparser(subparsers)

#simulate_selection
import sortseq.simulate_selection as simulate_selection
simulate_selection.add_subparser(subparsers)

#profile_freqs
import sortseq.profile_freqs as profile_freqs
profile_freqs.add_subparser(subparsers)

#profile_counts
import sortseq.profile_counts as profile_counts
profile_counts.add_subparser(subparsers)

#profile_mutrate
import sortseq.profile_mutrate as profile_mutrate
profile_mutrate.add_subparser(subparsers)

#marginalize_mutrate
import sortseq.fromto_mutrate as fromto_mutrate
fromto_mutrate.add_subparser(subparsers)

#marginalize_infofootprint
import sortseq.profile_info as profile_info
profile_info.add_subparser(subparsers)

#marginalize_infofootprint
import sortseq.profile_info_test as profile_info_test
profile_info_test.add_subparser(subparsers)

#profile_enrichment
import sortseq.profile_enrichment as profile_enrichment
profile_enrichment.add_subparser(subparsers)

#pairwise_mutrate
import sortseq.pairwise_mutrate as pairwise_mutrate
pairwise_mutrate.add_subparser(subparsers)

#logratio
import sortseq.logratio as logratio
logratio.add_subparser(subparsers)

#totalinfo
import sortseq.totalinfo as totalinfo
totalinfo.add_subparser(subparsers)

#errfromtags
import sortseq.errfromtags as errfromtags
errfromtags.add_subparser(subparsers)

#learn_matrix
import sortseq.learn_matrix as learn_matrix
learn_matrix.add_subparser(subparsers)

#convert_seqs
import sortseq.convertseqs as convertseqs
convertseqs.add_subparser(subparsers)

#convert_seqs
import sortseq.convert_fastq_to_seqs as convert_fastq_to_seqs
convert_fastq_to_seqs.add_subparser(subparsers)

#compare_predictiveinformation
import sortseq.compare_predictiveinformation as compare_predictiveinformation
compare_predictiveinformation.add_subparser(subparsers)

#compare_predictiveinformation
import sortseq.predictiveinfo as predictiveinfo
predictiveinfo.add_subparser(subparsers)

import sortseq.draw as draw
draw.add_subparser(subparsers)

# Final incantiation needed for this to work











