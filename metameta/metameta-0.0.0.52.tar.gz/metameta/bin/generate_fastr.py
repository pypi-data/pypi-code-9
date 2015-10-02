#! /usr/bin/env python

"""obtains read depth data for a FASTA/Q file from a BAM file

Usage:

    generate_fastr.py [--compressed] [--fastq] <fastaq> <bam> <output>

Synopsis:

    reads alignment data from a BAM file to produce a FASTR file
    containing read depth data for the FASTA/Q file

Required Arguments:

    fastaq             FASTA or FASTQ file used as the alignment mappingg
                       reference, defaults to FASTA
    bam                BAM file containing alignment data
    output             Name of FASTR file containing read depth data to write

Optional Arguments:

    --compressed       compress FASTR file being written
    --fastq            specifies that fastaq is a FASTQ file
"""

from __future__ import print_function

__version__ = '0.0.0.13'

import argparse
from bio_utils.verifiers.fasta import fasta_verifier
from bio_utils.verifiers.fastq import fastq_verifier
from bio_utils.verifiers.binary import binary_verifier
from metameta.metameta_utils.fastr_utils import compress_fastr, write_fastr
from metameta.metameta_utils.output import output
import pysam
from screed.fasta import fasta_iter
from screed.fastq import fastq_iter
import sys


def main():
    file_iter = fastq_iter if args.fastq else fasta_iter
    with pysam.Samfile(args.bam, 'rb') as bam_handle:
        with open(args.fastaq, 'rU') as fastaqFile:
            for entry in file_iter(fastaqFile):
                seq_id = entry['name']
                seq_length = len(entry['sequence'])
                seq_depth = [0 for base in range(seq_length)]

                # Extract sequence depth data form BAM file
                for pileUpColumn in bam_handle.pileup(seq_id):
                    seq_depth[pileUpColumn.pos] = str(pileUpColumn.n)

                # Compress sequence data if specified
                if args.compressed:
                    output('Compressing sequence of {0}'.format(seq_id),
                           args.verbosity, 2, log_file=args.log_file)
                    seq_fastr = compress_fastr(seq_depth)
                    output('Compressed sequence: {0}'.format(seq_fastr),
                           args.verbosity, 2, log_file=args.log_file)
                else:
                    seq_fastr = '-'.join(seq_depth)

                # Ensure that read depth is not only zero
                total_sum = sum([int(base) for base in seq_depth])
                if total_sum == 0:
                    message = 'Appending read depth for {0} to {1}'.format(
                        seq_id, args.output)
                    output(message, args.verbosity, 2,
                           log_file=args.log_file)
                    write_fastr([seq_id], [seq_fastr], open(args.output, 'a'))
                else:
                    message = '{0} has a read depth of zero for ' \
                              'each base. Not appending to {1}'.format(
                                  seq_id, args.output)
                    output(message, args.verbosity, 2,
                           log_file=args.log_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.
                                     RawDescriptionHelpFormatter)
    parser.add_argument('fastaq', metavar='FASTA or FASTQ',
                        default=None,
                        nargs='?',
                        help='FASTA or FASTQ file to analyze the read depth ' +
                             'of using the given BAM file [default: FASTA]')
    parser.add_argument('bam', metavar='BAM',
                        default=None,
                        nargs='?',
                        help='BAM file containing mapping ' +
                             'data for given FASTA or FASTQ file')
    parser.add_argument('output',
                        default=None,
                        nargs='?',
                        help='name of FASTR file to be written')
    parser.add_argument('--fastq',
                        action='store_true',
                        help='specifies FASTA/Q input file as a FASTQ file')
    parser.add_argument('--compressed',
                        action='store_true',
                        help='compresses FASTR output file')
    parser.add_argument('-l', '--log_file', metavar='LOG',
                        default=None,
                        help='log file to print all messages to')
    parser.add_argument('-v', '--verbosity',
                        action='count',
                        default=0,
                        help='increase output verbosity')
    parser.add_argument('--verify',
                        action='store_true',
                        help='verify input files before use')
    parser.add_argument('--version',
                        action='version',
                        version=__version__)
    args = parser.parse_args()

    if args.fastaq is None:
        print(__doc__)
    elif args.bam is None or args.output is None:
        message = 'Need to specify a FASTA/Q, BAM, and output file.'
        output(message, args.verbosity, 0, fatal=True)
    else:
        if args.verify:

            # Verify args.fastq
            output('Verifying {0}'.format(args.fastaq), args.verbosity, 1,
                   log_file=args.log_file)
            fastaqVerifier = fastq_verifier if args.fastq else fasta_verifier
            with open(args.fastaq, 'rU') as in_handle:
                validFastaq = fastaqVerifier(in_handle)
            fastaqValidity = 'invalid' if not validFastaq else 'valid'
            output('{0} is {1}'.format(args.fastq, fastaqValidity),
                   args.verbosity, 1, log_file=args.log_file,
                   fatal=not validFastaq)

            # Verify args.bam
            output('Verifying {0}'.format(args.bam), args.verbosity, 1,
                   log_file=args.log_file)
            with open(args.bam, 'rU') as in_handle:
                validBam = binary_verifier(in_handle)
            bamValidity = 'invalid' if not validBam else 'valid'
            output('{0} is {1}'.format(args.fastq, bamValidity),
                   args.verbosity, 1, log_file=args.log_file,
                   fatal=not validBam)

        # Main portion of program
        output('Generating FASTR file: {0}'.format(args.output),
               args.verbosity, 1, log_file=args.log_file)
        main()
        output('{0} generated successfully.'.format(args.output),
               args.verbosity, 2, log_file=args.log_file)
    output('Exiting generate_fastr.py', args.verbosity, 1,
           log_file=args.log_file)
    sys.exit(0)
