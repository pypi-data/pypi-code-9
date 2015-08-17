# coding: utf-8
'''
Main function lives here.
'''
from __future__ import absolute_import
from __future__ import print_function


import sys
import argparse
import logging
FORMAT = '%(asctime)s %(name)s %(levelname)s %(message)s'
# Set for all modules using logging
logging.basicConfig(format=FORMAT, level=logging.INFO)


from .input import process_input
from .version import (
    __version__, __authors__, __license__,
    __program_name__, __short_description__,
    get_platform_id)


def get_version_banner():
    '''Returns an unicode object with a description of
the program and the platform'''

    banner = u'''{name} version {version}.
Platform: '{platform}'.

{short_description}

Distributed under {license}.
Authors: {authors}.
'''
    params = {
        'version': __version__,
        'authors': ', '.join(__authors__),
        'license': __license__,
        'platform': get_platform_id(),
        'name': __program_name__,
        'short_description': __short_description__,
    }
    banner = banner.format(**params)
    return banner


def main():
    '''Main().'''
    # NOTE not used: logger = logging.getLogger(__name__)
    # Prepare CLI args parser
    parser = argparse.ArgumentParser(
        description=__short_description__,
        epilog=None,
    )
    parser.add_argument('-V', '--version',
                        help='Show version and platform',
                        action='store_true')
    parser.add_argument('hexnumbers_l', metavar='hexnumbers',
                        help='Hex number to convert. You '
                        'can also pipe to stdin.',
                        nargs=argparse.REMAINDER)
    args = parser.parse_args()

    # Have to show the version?
    if args.version:
        banner = get_version_banner()
        print(banner)
        sys.exit(0)

    # Read hexas from cli or from stdin?
    if len(args.hexnumbers_l) == 0:
        source = sys.stdin
        input_lines = source.readlines()
    else:
        input_lines = args.hexnumbers_l

    # Convert them to words
    output = process_input(input_lines)
    if output is None:
        sys.exit(1)
    output = output.strip()
    print(output)
    sys.exit(0)
