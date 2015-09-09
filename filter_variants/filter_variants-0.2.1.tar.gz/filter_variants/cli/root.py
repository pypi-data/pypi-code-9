#!/usr/bin/env python
# encoding: utf-8
"""
filter_variants.py

Command line tool for annotating vcf variants with frequencies and then filter them based on frequency.

Created by Måns Magnusson on 2015-09-09.
Copyright (c) 2015 __MoonsoInc__. All rights reserved.
"""

from __future__ import (print_function)

import sys
import logging

import click
import tabix

from codecs import open

from filter_variants import logger as root_logger
from filter_variants import (__version__, init_log, LEVELS, HeaderParser,
get_thousand_g_frequency, print_headers, print_variant, add_vcf_info)

@click.command()
@click.argument('variant_file',
                    nargs=1,
                    type=click.File('r'),
                    metavar='<vcf_file> or -'
)
@click.option('-f', '--thousand_g',
                    type=click.Path(exists=True), 
                    help="""Specify the path to a bgzipped vcf file (with index) with 1000g variants"""
)
@click.option('-t', '--treshold',
                    default=0.05, 
                    help="""Treshold for filter variants. Default 0.05"""
)
@click.option('-a', '--annotate',
                    is_flag=True, 
                    help="""If the variants should be annotated with the frequency"""
)
@click.option('-k', '--keyword',
                    default="1000G", 
                    help="""If variants are already annotated this is the keyword to look for
                    If they are not annotated this is the annotation term. Default 1000G"""
)
@click.option('-o', '--outfile', 
                    type=click.File('w'),
                    help='Specify the path to a file where results should be stored.'
)
@click.option('-v', '--verbose', 
                count=True,
                default=0,
                help=u"Increase output verbosity. Can be used multiple times, eg. -vv"
)
@click.option('-l', '--logfile',
                    type=click.Path(exists=False),
                    help=u"Path to log file. If none logging is "\
                          "printed to stderr."
)
def cli(variant_file, thousand_g, treshold, outfile, annotate, keyword,
        verbose, logfile):
    """
    Filter vcf variants based on their frequency.
    
    Variants and 1000G file should be splitted and normalized(with vt).
    """
    loglevel = LEVELS.get(min(verbose,2), "WARNING")
    init_log(root_logger, logfile, loglevel)
    
    logger = logging.getLogger(__name__)
    
    #For testing
    logger = logging.getLogger("filter_variants.cli.root")
    logger.info("Running filter_variants version {0}".format(__version__))

    # logger.info("Initializing a Header Parser")
    # head = HeaderParser()
    
    if thousand_g:
        logger.debug("Opening 1000G frequency file with tabix open")
        thousand_g_handle = tabix.open(thousand_g)
        logger.debug("1000G frequency file opened")
    else:
        logger.warning("Please provide a 1000G file")
        logger.info("Exiting")
        sys.exit(1)
        
    # print_headers(head, outfile)
    
    for line in variant_file:
        line = line.rstrip()
        if line.startswith('#'):
            if outfile:
                outfile.write(line+'\n')
            else:
                print(line)
        else:
            variant_line = line.split('\t')
            chrom = variant_line[0].strip('chr')
            position = int(variant_line[1])
            alternative = variant_line[4]
            frequency = get_thousand_g_frequency(
                chrom = chrom,
                pos = position,
                alt = alternative,
                tabix_reader = thousand_g_handle
                )
            if frequency:
                if float(frequency) < treshold:
                    print_variant(line, outfile)
                else:
                    logger.debug("Frequency {0} is higher than treshold"\
                    " {1}. Skip printing variant".format(frequency, treshold))
            else:
                print_variant(line, outfile)
    
    # headers_done = False
    # for line in variant_file:
    #     line = line.rstrip()
    #     if line.startswith('#'):
    #         if line.startswith('##'):
    #             head.parse_meta_data(line)
    #         else:
    #             head.parse_header_line(line)
    #     else:
    #         if not headers_done:
    #             if annotate:
    #                 if keyword in head.info_dict:
    #                     logger.info("Variants already annotated")
    #                     annotate = False
    #                 else:
    #                     head.add_info(
    #                         info_id=keyword,
    #                         number='A',
    #                         entry_type='Float',
    #                         description="The 1000 genomes frequency"
    #                         )
    #             print_headers(head, outfile)
    #             headers_done = True
    #
    #         variant_line = line.split('\t')
    #
    #         chrom = variant_line[0].strip('chr')
    #         position = int(variant_line[1])
    #         alternatives = variant_line[4].split(',')
    #
    #         frequencies = []
    #         if thousand_g:
    #             for alternative in alternatives:
    #                 frequency = get_thousand_g_frequency(
    #                         chrom = chrom,
    #                         pos = position,
    #                         alt = alternative,
    #                         tabix_reader = thousand_g_handle
    #                     )
    #                 if frequency:
    #                     frequencies.append(frequency)
    #                 else:
    #                     frequencies.append('0')
    #         if annotate:
    #             for frequency in frequencies:
    #                 if frequency != '0':
    #                     line = add_vcf_info(line, keyword, ','.join(frequencies))
    #         for frequency in frequencies:
    #             if float(frequency) < treshold:
    #                 print_variant(line, outfile)
    #             else:
    #                 logger.debug("Frequency {0} is higher than treshold"\
    #                 " {1}. Skip printing variant".format(frequency, treshold))

if __name__ == '__main__':
    cli()
