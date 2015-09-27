__author__ = 'Loris Mularoni'


# Import modules
import argparse
import os
import __main__
from multiprocessing import cpu_count
from functools import partial
from . import __version__


def check_file(input_file):
    """Check if the input file exists."""
    try:
        assert(os.path.isfile(input_file))
    except AssertionError as err:
        raise argparse.ArgumentTypeError("the file {} does not exist".format(input_file))
    return input_file


def check_value(value, length=1):
    """Check whether a value is a positive integer"""
    try:
        value = int(value)
    except ValueError as err:
        raise argparse.ArgumentTypeError("invalid integer value: '{}'".format(value))
    try:
        assert(value >= length)
    except AssertionError as err:
        raise argparse.ArgumentTypeError("invalid positive integer value: {}".format(value))
    return value


def run():
    parser = argparse.ArgumentParser(description='Find microsatellites.',
                                     prog=os.path.split(__main__.__file__)[1])

    parser.add_argument('-v', '--version',
                        action='version',
                        version='%(prog)s {}'.format(__version__))

    # Mandatory
    parser.add_argument('-i', '--input-fasta',
                        action='store',
                        dest='input_fasta',
                        type=check_file,
                        required=True,
                        help='[FILE] path of the fasta file containing the sequence(s) to ' +
                             'analyze. The file can be either a plain text file or a gzip ' +
                             'compressed file.')
    # Optional
    parser.add_argument('-o', '--output-file',
                        action='store',
                        dest='output_file',
                        default=None,
                        help='[FILE] path of the file to save with the results of the analysis. ' +
                             'The coordinates of the microsatellites will be 0-based.')
    # Mandatory
    parser.add_argument('-l', '--seed-length',
                        action='store',
                        dest='length',
                        type=partial(check_value, length=1),
                        required=True,
                        help='[INTEGER] length of the seed of the microsatellites.')

    # Optional
    parser.add_argument('-r', '--minimum-repetitions',
                        action='store',
                        dest='min_repetitions',
                        default=3,
                        type=partial(check_value, length=2),
                        help='[INTEGER] minimum number of repetitions of the seed. Minimum is 2 ' +
                             'and the default value is 3.')
    parser.add_argument('-a', '--alphabet',
                        action='store',
                        dest='alphabet',
                        default='dna',
                        choices=['dna', 'aa'],
                        type=str,
                        help='[STRING] alphabet to use for the microsatellites search. The ' +
                             'alphabet can be "dna" for DNA or "aa" for PROTEINS. Default is ' +
                             '"dna".')
    parser.add_argument('-im', '--imperfect',
                        action='store',
                        dest='imperfect',
                        default=-1,
                        type=partial(check_value, length=0),
                        help='[INTEGER] include imperfect microsatellites. With this option ' +
                             'microsatellites repeated at least "-r -1" times that share the ' +
                             'same seed and have a distance up to the "--imperfect" value will ' +
                             'be merged together and will be considered as a single ' +
                             'microsatellite. By default this option is disabled and ' +
                             'microsatellites are kept separated.')
    parser.add_argument('-s', '--strict',
                        action='store_true',
                        dest='strict',
                        default=False,
                        help='when "--imperfect"" is a positive integer, this option allows to ' +
                             'search for imperfect microsatellites only by using nucleotides ' +
                             'that are present in the seed. For instance, if the seed is "AT" ' +
                             'only the nucleotides "A" and "T" will be considered. By default' +
                             'this option is disabled and all the nucleotides (ACGT) are ' +
                             'considered.')
    parser.add_argument('-f', '--flanking',
                        action='store',
                        dest='flanks',
                        default=0,
                        type=partial(check_value, length=0),
                        help='[INTEGER] length of the sequences flanking the microsatellites. ' +
                             'The sequences will be written in the output file. Sequences that ' +
                             'overstep the boundaries of a chromosome will be truncated. By ' +
                             'default this option is disabled.')
    parser.add_argument('-c', '--cores',
                        action='store',
                        dest='cores',
                        default=cpu_count(),
                        choices=list(range(1, cpu_count() + 1)),
                        type=int,
                        help='[INTEGER] number of CPUs to use in the computation. By default it ' +
                             'uses all the available CPUs.')
    parser.add_argument('-p', '--progress',
                        action='store_true',
                        dest='progress',
                        default=False,
                        help='track the progress of the computation with a progress bar.')

    return parser.parse_args()


