#!/usr/bin/srv python

'''Returns subject sequence from BLAST hits below a specified e-value'''

import argparse
from bio_utils.iterators.m8 import m8_iter
from collections import defaultdict
import copy
from screed.fasta import fasta_iter
import sys

__version__ = '1.0.1.0'

def subject_sequence_retriever(fasta_handle, m8_handle, e_value):
    '''Returns FASTA entries for subject sequences from BLAST hits

    Stores M8 entries with e-values below the e_value cutoff. Then iterates
    through the FASTA file and if an entry matches the subject of an M8
    entry, it's sequence is extracted and returned as a FASTA entry.'''

    filtered_m8 = defaultdict(list)
    for m8Entry in m8_iter(m8_handle):
        if float(m8Entry['eValue']) <= e_value:
            filtered_m8[m8Entry['subjectID']].append(\
                (int(m8Entry['subjectStart']), int(m8Entry['subjectEnd']),\
                 float(m8Entry['eValue'])))
    for fastaEntry in fasta_iter(fasta_handle):
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
    parser.add_argument('fastaFile',
                        help = 'subject FASTA file')
    parser.add_argument('m8File',
                        help = 'M8 file with alignment data')
    parser.add_argument('e_value',
                        help = 'upper e-value cutoff')
    parser.add_argument('output',
                        default = None,
                        nargs = '?',
                        help = ' optional output file, defaults to STDOUT')
    args = parser.parse_args()

    with open(args.fastaFaile, 'rU') as fasta_handle:
        with open(args.m8File, 'rU') as m8_handle:
            for fastaEntry in subject_sequence_filter(fasta_handle,\
                                                      m8_handle,\
                                                      args.e_value):
                entry = '{} {}\n{}\n'.format(fastaEntry['name'],\
                                             fastaEntry['description'],\
                                             fastaEntry['sequence'])
                if args.output != None:
                    with open(args.output, 'w') as out_handle:
                            out_handle.write(entry)
                else:
                    print(entry)
    sys.exit(0)
