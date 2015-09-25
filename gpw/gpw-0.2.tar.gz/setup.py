#!/usr/bin/env python2
from distutils.core import setup
setup(
    name = "gpw",
    version = "0.2",
    py_modules = ['gpw'],
    description = "A simple wrapper for Gnuplot",
    author = "Wicher Minnaard",
    author_email = "wicher@gavagai.eu",
    url = "http://smormedia.gavagai.nl/dist/gpw/",
    download_url = "http://smormedia.gavagai.nl/dist/gpw/gpw-0.2.tar.gz",
    keywords = ["gnuplot"],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: Public Domain",
        "Operating System :: POSIX",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Multimedia :: Graphics",
        ],
    long_description = """\
gpw - gnuplot wrapper module for interfacing Python with gnuplot.
------------------------------------------------------------------------------------
by Wicher Minnaard <wicher@gavagai.eu> <http://smorgasbord.gavagai.nl>

This is public domain software.

Difference with gnuplot-py: This module does not need numpy. Also, this module 
doesn't offer tight integration with gnuplot.

The main problem this module solves is that gnuplot needs a) data, b) instructions,
and generates c) graph output. a) comes from files, b) can be fed in stdin, and c)
can be written to stdout and used in your Python code.

For instance, you may want to feed data from Python into gnuplot according to
some dynamically generated instructions, catch some SVG back in a Python string, 
and push that out over HTTP without messing with temporary files.

But if you want to feed _data_ from Python into gnuplot, then you must use temporary
files because stdin is reserved for instructions.

This module employs filesystem FIFOs and doesn't write data to disk.


This version works with Python 2.7 and 3.1+.
"""
)
