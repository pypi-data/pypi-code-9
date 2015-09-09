#!/usr/bin/env python
# encoding: utf-8
"""
print_variants.py

Print the variants of a file to vcf file.

There are two modes, 'vcf' or 'modified'.
If 'vcf' we expect plain vcf variants and print them as they came in.
If 'modified' the first column has been used for sorting so we skip that one.

If a outfile is provided the variants will be printed to this one.

Created by Måns Magnusson on 2015-01-22.
Copyright (c) 2015 __MoonsoInc__. All rights reserved.
"""

from __future__ import print_function

from codecs import open


def print_variant(variant_line, outfile=None, silent=False):
    """
    Print the variants.
    
    If a result file is provided the variante will be appended to the file, 
    otherwise they are printed to stdout.
    
    Args:
        variants_file (str): A string with the path to a file
        outfile (FileHandle): An opened file_handle
        silent (bool): Bool. If nothing should be printed.
    
    """
    
    if not variant_line.startswith('#'):
        if outfile:
            outfile.write(variant_line+'\n')
        
        else:
            if not silent:
                print(variant_line)
    return

