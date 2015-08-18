#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''digs

Usage:
  digs <url> [--depth=INT] [--to=PATH] [--sameroot] [--log=PATH] [-o]
  digs -i
  digs -h | --help
  digs --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  -i            Start the Graphical Interface.
  --depth=INT   depth on tree of search website [default: 0].
  --to=PATH     A path to save all text data: [default: ./].
                Avoid the use of "~" shortcut.
  -o            Overwrite if some file exists yet. [default: False].
  --sameroot    All children links should have the <url> domain as root. [default: True]
  --log=PATH    Path to save the log file. [default: ./].
'''

# TODO
# -f            Flatten. Do not save on folders by level. [default: False].


from __future__ import unicode_literals, print_function
from docopt import docopt

__version__ = "0.1.7"
__author__ = "Jonathan S. Prieto C."
__license__ = "BSD3"


def main():
    '''Main entry point for the digs CLI.'''
    opts = docopt(__doc__, version=__version__)
    print(opts)

if __name__ == '__main__':
    main()
