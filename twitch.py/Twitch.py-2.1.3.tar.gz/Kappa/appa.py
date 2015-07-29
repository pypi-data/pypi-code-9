#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
appa.py 
Defines the main() function ran by "twitch"
'''

from argparse import ArgumentParser
from .info import __version__
from .lib import TwitchApp as App


def main(*args, **kwargs):
    """
    Runner main function
    """
    parser = ArgumentParser(
        description='Interact with Twitch.tv',
        prog='twitch.py')
    parser.add_argument('-g', type=str, nargs='+', metavar='text',
                        help='The game whose directory you wish to scan')
    parser.add_argument('-l', '--limit', type=int, default=App.default_limit, 
                        metavar='LIM', help='Number of streams to fetch')
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s ver.{0}'.format(__version__))
    parser.add_argument('-b', '--best', action='store_const', const=True,
                        default=False, help='Use best quality') 
    parser.add_argument('-d', '--debug', action='store_const', const=True,
                        default=False, help='Debug the program')
    args = parser.parse_args()
    if args.debug:
        App(args)
        print("Finished debugging")
    else:
        try:
            App(args)
        except KeyboardInterrupt as e:
            print('\nQuitting...')
        except Exception as e:
            print("Error encountered: {0}".format(e))
        finally:
            print('\nAll done!')
if __name__ == '__main__':
    main()
# end
