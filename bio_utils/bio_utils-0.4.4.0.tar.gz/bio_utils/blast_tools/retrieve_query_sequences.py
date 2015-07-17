#!/usr/bin/srv python

'''Returns query sequence from BLAST hits below a specified e-value'''

import argparse
from bio_utils.iterators.m8 import m8_iter
from collections import defaultdict
import copy
from screed.fasta import fasta_iter
from screed.fastq import fastq_iter
import sys

__version__ = '1.0.0.0'

def query_sequence_retriever(fastaq_handle, m8_handle, e_value,\
                             fastaq = 'fasta'):
    '''Returns FASTA entries for subject sequences from BLAST hits

    Stores M8 entries with e-values below the e_value cutoff. Then iterates
    through the fasta file and if an entry matches the query of an M8
    entry, it's sequence is extracted and returned as a FASTA entry
    plus the e-value'''

    filtered_m8 = defaultdict(list)
    for m8Entry in m8_iter(m8_handle):
        if float(m8Entry['eValue']) <= e_value:
            filtered_m8[m8Entry['queryID']].append(\
                (int(m8Entry['queryStart']), int(m8Entry['queryEnd']),\
                 float(m8Entry['eValue'])))
    fastaq_iter = fasta_iter if fastaq == 'fasta' else fastq_iter
    for fastaEntry in fastaq_iter(fastaq_handle):
        if fastaEntry['name'] in filtered_m8:
            for pair in filtered_m8[fastaEntry['name']]:
                subjectSequence = ''
                start = pair[0] - 1
                end = pair[1] - 1
                if start < end:
                    querySequence = fastaEntry['sequence'][start:end]
                elif start > end:
                    querySequence = fastaEntry['sequence'][end:start][::-1]
                else:
                    querySequence = fastaEntry['sequence'][start]
                yieldEntry = copy.deepcopy(fastaEntry)
                yieldEntry['sequence'] = querySequence
                yieldEntry['eValue'] = pair[2]
                yield yieldEntry

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = __doc__,
                                     formatter_class = argparse.\
                                     RawDescriptionHelpFormatter)
    parser.add_argument('fastaqFile',
                        help = 'query FASTAQ file')
    parser.add_argument('m8File',
                        help = 'M8 file with alignment data')
    parser.add_argument('e_value',
                        help = 'upper e-value cutoff')
    parser.add_argument('--fastq',
                        action = 'store_true',
                        help = 'specifies that input is ')
    parser.add_argument('output',
                        default = None,
                        nargs = '?',
                        help = ' optional output file, defaults to STDOUT')
    args = parser.parse_args()

    fastaq = 'fastq' if args.fastq else 'fasta'
    with open(args.fastaFaile, 'rU') as fasta_handle:
        with open(args.m8File, 'rU') as m8_handle:
            for fastaEntry in query_sequence_filter(fasta_handle,\
                                                    m8_handle,\
                                                    args.e_value,\
                                                    fastaq = fastaq):
                entry = '{} {}\n{}\n'.format(fastaEntry['name'],\
                                             fastaEntry['description'],\
                                             fastaEntry['sequence'])
                if args.output != None:
                    with open(args.output, 'w') as out_handle:
                            out_handle.write(entry)
                else:
                    print(entry)
    sys.exit(0)

