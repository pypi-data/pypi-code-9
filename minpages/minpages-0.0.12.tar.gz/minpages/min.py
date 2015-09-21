#!/usr/bin/env python

from __future__ import print_function

import argparse
import os

from os.path import expanduser, join

from .page import Page

def main():
    parser = argparse.ArgumentParser(
            description='Min pages',
            )
    
    parser.add_argument('page', nargs='?', help='Which page to view/edit/delete' )
    parser.add_argument('-e','--edit', help='Edit/create a page', action='store_true')
    parser.add_argument('-d','--delete', help='Delete a page', action='store_true')
    def_page_dir =  join(expanduser('~'),'.minpages')
    parser.add_argument(
            '--page-dir', 
            help='The pages directory (default: {default})'.format(
                default=def_page_dir
                ), 
            default=def_page_dir
            )
    try:
        def_editor = os.environ['VISUAL']
    except KeyError:
        def_editor = 'vi'
    parser.add_argument(
            '--editor', 
            help='The editor to use (default: {default})'.format(
                default=def_editor
                ), 
            default=def_editor
            )

    args = vars(parser.parse_args())

    Page(args)

if __name__ == '__main__':
    main()
