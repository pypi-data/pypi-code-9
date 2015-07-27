#! /usr/bin/env python

"""metameta 0.0.0.50 - meta-transcriptome/genome mapping analysis toolkit

Usage:

    metameta <tool> [arguments for tool]

Synopsis:

    metameta is a toolkit with a number of programs useful for analyzing
    meta-transcriptome/genome data that has been mapped to a reference.
    It is contains a number of generally useful bioinformatic scripts.
    Type "metameta --docs" for full documentation.

Options:

    Toolkit (options from metameta, no tool specified/needed):

        --help             This help
        --version          Print toolkit version and exits
        --docs             Show full manual

    General Tool Options (options shared by most or all tools):

        no arguments       Gives tool help and exits
        --help             Gives tool help and exits
        --version          Prints tool version and exits
        --verify           Verify relevant files before executing
        --log_file         Write output to the log file

    Verbosity Settings (all tools):

        none: Fatal errors only
        -v: Fatal errors and important information only
        -vv: Detailed information on everything the program is doing,
             best reserved for debugging purposes
        Note: any numbers of "v"s may be specified but anything greater than
        -vv will be identical to -vv.

Tools:

    compute_gene_abundance:

            Reads a GFF3 file and a FASTR or BAM file to produce a
            tab-delimited file containing genes and their abundance values.

    generate_fastr:

            Generates a FASTR file containing per base read depth data
            of a given FASTA or FASTQ file.
"""

__version__ = '0.0.0.50'

import argparse
import metameta.bin
from pkg_resources import resource_string
import subprocess
import sys


def tool_check(desired_tool):
    """Checks if given tool is valid and prints a list of tools if not"""

    tools = [
        'compute_gene_abundance',
        'generate_fastr',
    ]
    for tool in tools:
        if desired_tool == tool:
            return desired_tool
    print('No such tool: ' + desired_tool)
    print('Available tools:')
    for tool in tools:
        print(tool)
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.
                                     RawDescriptionHelpFormatter)
    parser.add_argument('tool',
                        type=tool_check,
                        default=None,
                        nargs='?',
                        help='tool to run')
    parser.add_argument('arguments',
                        nargs=argparse.REMAINDER,
                        help='arguments to pass to tool')
    parser.add_argument('--docs',
                        help='prints documentation and exits',
                        action='store_true')
    parser.add_argument('--version',
                        action='version',
                        version=__version__)
    args = parser.parse_args()

    location = metameta.bin.__file__.rstrip('__init__.pyc')
    if args.docs:
        documentation = resource_string('metameta.data', 'Documentation.txt')
        subprocess.call(['less', documentation])
    elif args.tool is None:
        print(__doc__)
    else:
        script = location + args.tool + '.py'
        command = ['python'] + [script] + args.arguments
        subprocess.call(command)


if __name__ == '__main__':
    main()
    sys.exit(0)
