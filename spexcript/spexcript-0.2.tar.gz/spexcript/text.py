# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 15:10:51 2013

Tools for creating plain text spextex output.

@author: Koos Zevenhoven
"""
from __future__ import unicode_literals, print_function, division
import textwrap

line_end = "\r\n"
par_indent = 3
char_descr_indent = 3


def wrapped_lines(paragraphs, width = 79): 
    first = True
    for par in paragraphs:
        if not first:
            par = " " * par_indent + par
    
        wrapped_lines = textwrap.wrap(par,width=width)
    
        for l in wrapped_lines:
            yield l
        first = False
