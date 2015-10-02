#! /usr/bin/env python

"""calculates gene abundance data from annotations of an assembly

Usage:

    compute_gene_abundance.py [--bam] [--delimiter] [--fasta] [--fastr]
                              [--normalize] <gff3> <output>

Synopsis:

    calculates and normalizes gene abundance of annotated genes in a GFF3
    file using a variety of files to obtain abundance data from:
    BAM files
    FASTA files from IDBA-UD
    FASTR files

Required Arguments:

    gff3             GFF3 formatted annotation file
    output           CSV file containing gene ID and abundance,
                     default delimiter is "\t"

Optional Arguments:

    --bam            BAM file containing alignment data
    --delimiter      the character to delimit the output file by
                     [Default: '\t']
    --fasta          IDBA-UD generated FASTA file used for assembly
    --fastr          FASTR file containing read depth data
    --normalize      Method to calculate coverage values (see below for more
                     information on normalization) [Default: 'read_count']

Supported Normalization Methods:

    arpb             Average Reads Per Base: average depth coverage of each
                     base
    read_count       Uses the number of reads used to assemble contig as
                     coverage [Default]
    rpk              Reads Per Kilobase: number of reads used to assemble
                     contig divided by kilobases in the contig (contig length
                     divided by 1,000)
    rpkt, rpb        rpk times 1,000 (equivalent to reads per base)
    rpkm             rpk times 1,000,000
    rpkb             rpk times 1,000,000,000
"""

from __future__ import division
from __future__ import print_function

import argparse
from bio_utils.iterators.gff3 import gff3_iter
from bio_utils.iterators.fastr import fastr_iter
from bio_utils.verifiers.binary import binary_verifier
from bio_utils.verifiers.fasta import fasta_verifier
from bio_utils.verifiers.fastr import fastr_verifier
from bio_utils.verifiers.gff3 import gff3_verifier
from metameta.metameta_utils.fastr_utils import decompress_fastr
from metameta.metameta_utils.output import output
import pysam
import re
from screed.fasta import fasta_iter
import statistics
import sys

__version__ = '0.0.0.9'


def compute_gene_abundance_from_bam(bam_file, gff3_file, database,
                                    normalization, out_file):
    with open(out_file, 'a') as out_handle:
        with pysam.AlignmentFile(bam_file, 'rb') as bam_handle:
            with open(gff3_file, 'rU') as gff3_handle:
                for entry in gff3_iter(gff3_handle):
                    db_id = extract_db_id(entry['attributes'], database)
                    if int(entry['start']) > int(entry['end']):
                        start = int(entry['end']) - 1
                        end = int(entry['start']) - 1
                    else:
                        start = int(entry['start']) - 1
                        end = int(entry['end']) - 1
                    if normalization == 'arpb':
                        reads_per_base = [pileUp.n for pileUp in bam_handle.
                            pileup(entry['seq_id'], start, end)]
                        coverage = normalize(normalization,
                                             per_base_depth=reads_per_base)
                    else:
                        read_count = len([read for read in bam_handle.fetch(
                            entry['seqid'], start, end)])
                        gene_length = end - start
                        coverage = normalize(normalization,
                                             read_count=read_count,
                                             length=gene_length)
                    if db_id is not None:
                        out_handle.write('{0}\t{1}\n'.format(db_id, coverage))


def compute_gene_abundance_from_fasta(fasta_file, gff3_file, database,
                                      normalization, out_file):
    gff3_dict = gff3_to_dict(gff3_file, database)
    with open(out_file, 'a') as out_handle:
        with open(fasta_file, 'rU') as fasta_handle:
            for entry in fasta_iter(fasta_handle):
                read_count = entry['description'].split('read_count_')[-1]
                if normalization != 'read_count':
                    contig_length = len(entry['sequence'])
                    read_count = normalize(normalization,
                                           length=contig_length,
                                           read_count=read_count)
                coverage = read_count
                if entry['name'] in gff3_dict:
                    for gene in gff3_dict[entry['name']]:
                        attributes = gff3_dict[entry['name']][gene] \
                            ['attributes']
                        db_id = extract_db_id(attributes, database)
                        if db_id is not None:
                            out_handle.write('{0}\t{1}\n'.format(db_id,
                                                                 coverage))


def compute_gene_abundance_from_fastr(fastr_file, gff3_file, database,
                                      normalization, out_file):
    if normalization != 'arpb':
        message = 'FASTR files can only be used to calculate coverage as ' \
                  'Average Reads Per Base (arpb). Run this program with the' \
                  ' "--normalzie arpb" flag or use a different file type to ' \
                  'calculate coverage from.'
        output(message, 0, 0, fatal=True)
    gff3_dict = gff3_to_dict(gff3_file, database)
    with open(out_file, 'a') as out_handle:
        with open(fastr_file, 'rb') as fastr_handle:
            for entry in fastr_iter(fastr_handle):
                if entry['name'] in gff3_dict:
                    fastr_sequence = decompress_fastr(entry['sequence'])
                    coverage_sequence = [int(base) for base in
                                         fastr_sequence.split('-')]
                    if entry['name'] in gff3_dict:
                        for gene in gff3_dict[entry['name']]:
                            gene = gff3_dict[entry['name']][gene]
                            if gene['start'] < gene['end']:
                                start = int(gene['end']) - 1
                                end = int(gene['start']) - 1
                            else:
                                start = int(gene['start']) - 1
                                end = int(gene['end']) - 1
                            reads_per_base = coverage_sequence[start:end]
                            coverage = normalize(normalization,
                                                 per_base_depth=reads_per_base)
                            db_id = extract_db_id(gene['attributes'], database)
                            if db_id is not None:
                                out_handle.write('{0}\t{1}\n'.format(db_id,
                                                                 coverage))


def extract_db_id(attributes, database):
    id_regex = re.compile('{0}:.*?;'.format(database))
    search_results = re.findall(id_regex, attributes)
    if len(search_results) == 1:
        db_id = search_results[0].lstrip('{0}:'.format(database)).rstrip(';')
        return db_id
    else:
        return None


def gff3_to_dict(gff3_file, database):
    gff3_dict = {}
    with open(gff3_file, 'rU') as gff3_handle:
        for entry in gff3_iter(gff3_handle):
            db_id = extract_db_id(entry['attributes'], database)
            if db_id is None:
                continue
            elif entry['seqid'] not in gff3_dict:
                gff3_dict[entry['seqid']] = {}
            gff3_dict[entry['seqid']][db_id] = entry
    return gff3_dict


def normalization_method(method):
    acceptable_methods = ['read_count', 'rpk', 'rpkt', 'rpkm', 'rpkb', ' rpb',
                          'arpb']
    if method in acceptable_methods:
        return str(method)
    else:
        message = '{0} is not a supported normalization method. Supported ' \
                  'normalization methods follow:\n{1}'.format(method,
                                        '\n'.join(acceptable_methods))
        output(message, 0, 0, fatal=True)


def normalize(normalization, length=0, read_count=0,
              per_base_depth=None):
    normalized_coverage = False
    if normalization == 'read_count':
        return read_count
    elif 'rpk' in normalization:
        normalization_factor = {
            'rpk': 1,
            'rpkt': 1000,
            'rpkm': 1000000,
            'rpkb': 1000000000
        }
        normalized_coverage = (read_count / (length / 1000)) * \
                              normalization_factor[normalization]
    elif normalization_method == 'arpb':
        assert type(per_base_depth) is list
        normalized_coverage = statistics.mean(per_base_depth)
    return normalized_coverage


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.
                                     RawDescriptionHelpFormatter)
    parser.add_argument('gff3', metavar='GFF3',
                        default=None,
                        nargs='?',
                        help='PROKKA GFF3 file with annotations for the same'
                             + ' metagenome as the FASTA or FASTR file')
    parser.add_argument('output', metavar='out_prefix',
                        default=None,
                        nargs='?',
                        help='name of TSV file to write')
    parser.add_argument('--bam', metavar='BAM',
                        default=None,
                        nargs='?',
                        help='BAM file containing mapping data')
    parser.add_argument('-d', '--database', metavar='DB',
                        default='ko',
                        help='extract hits from database "DB" [default: ko]')
    parser.add_argument('--fasta', metavar='FASTA',
                        default=None,
                        nargs='?',
                        help='IDBA generated FASTA file with read count data')
    parser.add_argument('--fastr', metavar='FASTR',
                        default=None,
                        nargs='?',
                        help='FASTR file containing read depth data for a ' +
                             'metatranscriptome mapped onto a metagenome')
    parser.add_argument('-l', '--log_file', metavar='LOG',
                        default=None,
                        help='log file to print all messages to')
    parser.add_argument('--normalize', metavar='normalization method',
                        type=normalization_method,
                        default='read_count',
                        help='how to normailze data [default: read_count]')
    parser.add_argument('-v', '--verbosity',
                        action='count',
                        default=0,
                        help='increase output verbosity')
    parser.add_argument('--verify',
                        action='store_true',
                        help='verify input files before use')
    parser.add_argument('--version',
                        action='store_true',
                        help='prints tool version and exits')
    args = parser.parse_args()

    if args.version:
        print(__version__)
    elif args.fastr is None and args.fasta is None and args.bam is None:
        print(__doc__)
    elif args.gff3 is None:
        message = 'Must specify a GFF3 file and either a BAM, FASTA, ' \
                  'or FASTR file'
        output(message, args.verbosity, 0, log_file=args.log_, fatal=True)
    else:
        if args.verify:

            # Verify BAM file
            if args.bam:
                output('Verifying {0}'.format(args.bam), args.verbosity, 1,
                       log_file=args.log_file)
                with open(args.bam, 'rU') as in_handle:
                    validBam = binary_verifier(in_handle)
                bamValidity = 'valid' if validBam else 'invalid'
                output('{0} is {1}'.format(args.bam, bamValidity),
                       args.verbosity, 1, log_file=args.log_file,
                       fatal=not validBam)

            # Verify FASTA file
            if args.fasta:
                output('Verifying {0}'.format(args.fasta), args.verbosity, 1,
                       log_file=args.log_file)
                with open(args.fasta, 'rU') as in_handle:
                    validFasta = fasta_verifier(in_handle)
                fastaValidity = 'valid' if validFasta else 'invalid'
                output('{0} is {1}'.format(args.fasta, fastaValidity),
                       args.verbosity, 1, log_file=args.log_file,
                       fatal=not validFasta)

            # Verify FASTR file
            if args.fastr:
                output('Verifying {0}'.format(args.fastr), args.verbosity,
                       1, log_file=args.log_file)
                with open(args.fasta, 'rU') as in_handle:
                    validFastr = fastr_verifier(in_handle)
                fastrValidity = 'valid' if validFastr else 'invalid'
                output('{0} is {1}'.format(args.fastr, fastrValidity),
                       args.verbosity, 1, log_file=args.log_file,
                       fatal=not validFastr)

            # Verify GFF3 file
            output('Verifying {0}'.format(args.gff3), args.verbosity, 1,
                   log_file=args.log_file)
            with open(args.gff3, 'rU') as in_handle:
                validGff3 = gff3_verifier(in_handle)
            gff3Validity = 'valid' if validGff3 else 'invalid'
            output('{0} is {1}'.format(args.gff3, gff3Validity),
                   args.verbosity, 1, log_file=args.log_file,
                   fatal=not validGff3)

        # Main portion of program
        # Write header to output
        with open(args.output, 'w') as out_handle:
            out_handle.write('Database_ID\tCoverage_{0}\n'.format(
                args.normalize))
        if args.bam:
            message = 'Computing gene abundances from BAM ' \
                      'file {0}'.format(args.bam)
            output(message, args.verbosity, 1, log_file=args.log_file)
            compute_gene_abundance_from_bam(args.bam,
                                            args.gff3,
                                            args.database,
                                            args.normalize,
                                            args.output)
        elif args.fasta:
            message = 'Computing gene abundances from IDBA-UD generated ' \
                      'FASTA file {0}'.format(args.fasta)
            output(message, args.verbosity, 1, log_file=args.log_file)
            compute_gene_abundance_from_bam(args.fasta,
                                            args.gff3,
                                            args.database,
                                            args.normalize,
                                            args.output)
        elif args.fastr:
            message = 'Computing gene abundances from FASTR ' \
                      'file {0}'.format(args.fastr)
            output(message, args.verbosity, 1, log_file=args.log_file)
            compute_gene_abundance_from_fastr(args.fastr,
                                              args.gff3,
                                              args.database,
                                              args.normalize,
                                              args.output)
        sys.exit(0)
