# MIT license
# 
# Copyright (C) 2015 by XESS Corporation
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
'''
A script for generating pin location constraints for a peripheral board attached to a StickIt! motherboard.
'''

import sys
import argparse
from xsconnect import *
from __init__ import __version__

SUCCESS = 0
FAILURE = 1

def xsconn():
    parser = argparse.ArgumentParser(
        description=
        'Generate pin assignments for a given peripheral board, motherboard, and daughterboard.')
    parser.add_argument('-v', '--version',
                        action='version',
                        version='%(prog)s ' + __version__)
    parser.add_argument('-p', '--peripheralboard', nargs='?')
    parser.add_argument('-m', '--motherboard', nargs='?')
    parser.add_argument('-d', '--daughterboard', nargs='?')
    parser.add_argument('-n', '--portname', nargs='?')
    parser.add_argument('-l', '--list', action='store_true')
    args = parser.parse_args()

    if args.list:
        # List the available peripherals, motherboards (and ports), and daughterboards.
        print '\nPeripherals:'
        for periphbrd in get_board_list(PERIPHERALBRD_DIR):
            print '\t{0}'.format(periphbrd)
        print '\nMotherboards:'
        for motherbrd in get_board_list(MOTHERBRD_DIR):
            print '\t{0}:'.format(motherbrd),
            sep = ''
            for port in get_board_port_names(MOTHERBRD_DIR, motherbrd):
                print sep, port,
                sep = ','
            print
        print '\nDaughterboards:'
        for daughterbrd in get_board_list(DAUGHTERBRD_DIR):
            print '\t{0}'.format(daughterbrd)
    else:
        # Print the pin assignments for connecting the peripheral board to the daughterboard.
        try:
            # The arguments given by the user may not be an exact match for the
            # board or port names, so find the closest matches and use those.
            periph = find_board_match(PERIPHERALBRD_DIR, args.peripheralboard)
            mother = find_board_match(MOTHERBRD_DIR, args.motherboard)
            port = find_port_match(args.portname, MOTHERBRD_DIR, mother)
            daughter = find_board_match(DAUGHTERBRD_DIR, args.daughterboard)

            # Now do the pin assignments.
            assignments = do_assignments(periph, mother, port, daughter)
            print_assignments(periph, mother, port, daughter, assignments)
        except:
            # Print the error message without the exception traceback.
            print 'ERROR:', sys.exc_info()[1]
            sys.exit(FAILURE)

    sys.exit(SUCCESS)


if __name__ == '__main__':
    xsconn()
