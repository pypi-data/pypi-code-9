#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
appa.py 
'''

from argparse import ArgumentParser
from .info import __version__
from .lib import main as App


def main(*args, **kwargs):
    """
    Runner main function
    """
    parser = ArgumentParser(
        description='Check Dota 2 Tournament Matches',
        prog='dotacli')
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s ver.{0}'.format(__version__))
    parser.add_argument('-d', '--debug', action='store_const', const=True,
                        default=False, help='Debug the program')
    args = parser.parse_args()
    try:
        App(args)
    except KeyboardInterrupt as e:
        print('\nQuitting...')
    except Exception as e:
        print("Error encountered: {0}".format(e))

if __name__ == '__main__':
    main()
# end
