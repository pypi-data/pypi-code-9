#! /usr/bin/env python
# Copyright (C) 2007-2010, Stefan Schwarzer
# see the file LICENSE for the license of this software

"""
Run this file from the command line without arguments to have all
doctests executed.

To run a single doctest file, invoke the script with the file as
argument, e. g. `python test.py test_page.txt`.
"""

import doctest
import glob
import sys

# Websourcebrowser modules
# These aren't referenced explicitly below but they are searched
#  implicitly in the namespace of this module.
import coding
import config
import directory_converter
import tools
import urlpath


def main():
    # tests in docstrings in modules
    for item in globals().values():
        if isinstance(item, type(doctest)) and \
          item.__name__ not in ("__builtin__", "doctest"):
            doctest.testmod(item)
    # tests in text files
    # compare http://www.velocityreviews.com/forums/showthread.php?t=363458&page=2
    posixlike = """aix3 aix4 atheos beos5 darwin freebsd2 freebsd3 freebsd4
                   freebsd5 freebsd6 freebsd7 generic irix5 irix6 linux2
                   netbsd1 next3 os2emx riscos sunos5 unixware7""".split()
    skip_under_posix = glob.glob("test_*_windows.txt")
    skip_under_windows = glob.glob("test_*_posix.txt")
    skip_always = ["test_template.txt"]
    for file_name in glob.glob("test_*.txt"):
        if file_name in skip_always:
            continue
        if sys.platform.startswith('win') and (file_name in skip_under_windows):
            continue
        if sys.platform in posixlike and (file_name in skip_under_posix):
            continue
        doctest.testfile(file_name)

if __name__ == '__main__':
    # execute just the single test file if given on the command line
    if len(sys.argv) == 2:
        doctest.testfile(sys.argv[1])
    else:
        main()

