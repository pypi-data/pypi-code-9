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

from os import listdir
from os.path import isfile, join, dirname, basename, splitext, realpath
import difflib
import re

INSTALL_DIR = dirname(realpath(__file__))
PERIPHERALBRD_DIR = 'peripheralboards'
MOTHERBRD_DIR = 'motherboards'
DAUGHTERBRD_DIR = 'daughterboards'


def get_files(dir):
    '''Return a list of files in a directory.'''
    return [join(dir, f) for f in listdir(join(INSTALL_DIR, dir))
            if not f.startswith('__') and f.endswith('.py') and
            isfile(join(INSTALL_DIR, dir, f))]


def file_to_module(file):
    '''Convert a file name to an importable python module name.'''
    return dirname(file) + '.' + basename(splitext(file)[0])


def get_board_modules(board_dir):
    '''Return a dictionary of board names and associated modules from a set of files.'''
    names = {}
    for f in get_files(board_dir):
        module = file_to_module(f)
        exec ('import ' + module + ' as mod')
        if isinstance(mod.brd['name'], type('')):
            # The board in this module has a single name.
            # Associate the python module with this name.
            names[mod.brd['name']] = module
        elif isinstance(mod.brd['name'], (type(()), type([]))):
            # The board in this module has a list of multiple aliases.
            # Associate the python module with these names.
            for n in mod.brd['name']:
                names[n] = module
        else:
            raise (Exception('Board name error'))
    return names


def get_board_list(board_dir):
    '''Return a list of board names found in a directory.'''
    return get_board_modules(board_dir).keys()


def get_board_port_types(board_dir, board_name):
    '''Return a set containing the types of ports on a board.'''
    module = get_board_modules(board_dir)[board_name]
    exec ('import ' + module + ' as mod')
    return set(mod.brd['port'].keys())


def get_port_type(board_dir, board_name, port_name):
    '''Return the port type string for the given port name on the given board.'''
    for type in get_board_port_types(board_dir, board_name):
        names = get_board_port_names(board_dir, board_name, type)
        if port_name in names:
            return type
    raise Exception('Port {0} not found on {1}.'.format(port_name, board_name))


def get_board_port_names(board_dir, board_name, port_type=None):
    '''Return a list of the port names on a board.'''
    module = get_board_modules(board_dir)[board_name]
    exec ('import ' + module + ' as mod')
    if port_type is None:
        port_types = get_board_port_types(board_dir, board_name)
    else:
        port_types = [port_type]
    port_names = []
    for type in port_types:
        port_names.extend(mod.brd['port'][type].keys())
    return port_names


def get_compatible_ports(brd_dir1, brd_nm1, brd_dir2, brd_nm2):
    '''Get the type and names for compatible ports on two boards.'''
    brd1_port_types = get_board_port_types(brd_dir1, brd_nm1)
    brd2_port_types = get_board_port_types(brd_dir2, brd_nm2)
    # Intersect the port types to find matching port types.
    compat_types = list(brd1_port_types & brd2_port_types)
    matching_ports = []
    for type in compat_types:
        brd_port_names1 = get_board_port_names(brd_dir1, brd_nm1, type)
        brd_port_names2 = get_board_port_names(brd_dir2, brd_nm2, type)
        matching_ports.extend([
            [n1, n2] for n1 in brd_port_names1 for n2 in brd_port_names2
        ])
    return matching_ports


def find_port_match(port_name, board_dir, motherbrd_name):
    '''Return the closest matching port name from a port list.'''

    try:
        # Get the list of ports for a given motherboard.
        port_list = get_board_port_names(board_dir, motherbrd_name)
        return find_closest_match(port_name, port_list, threshold=0.7)
    except:
        raise Exception(
            'Could not find matching port for {0} on motherboard {1}\n'.format(
                port_name, motherbrd_name))


def find_board_match(board_dir, board_name):
    '''Return the closest matching board name from a board list.'''

    try:
        # Get the list of boards from a board directory.
        board_list = get_board_list(board_dir)
        return find_closest_match(board_name, board_list)
    except:
        raise Exception(
            'Could not find matching board for {0}\n'.format(board_name))


def find_closest_match(name, name_list, threshold=0.0):
    # Scrub non-alphanumerics from names and lowercase them.
    scrubber = re.compile('[\W.]+')
    scrubbed_list = [scrubber.sub('', brd).lower() for brd in name_list]

    # Find the closest match to the given name in the scrubbed list.
    # Set the matching threshold to 0 so it always gives some result.
    scrubbed_name = difflib.get_close_matches(name, scrubbed_list, 1, threshold)[0]

    # Now match the scrubbed name against the original list and return the
    # non-scrubbed name. (This is horribly inefficient, but easy to do.)
    return difflib.get_close_matches(scrubbed_name, name_list, 1, threshold)[0]


def do_assignments(peripheralboard, motherboard, port_name, daughterboard):
    '''Determine the pin assignments for the given peripheral board,
       motherboard and port, and daughterboard.'''

    periph_name_to_module = get_board_modules(PERIPHERALBRD_DIR)
    mbrd_name_to_module = get_board_modules(MOTHERBRD_DIR)
    dbrd_name_to_module = get_board_modules(DAUGHTERBRD_DIR)

    # Import the net-to-I/O assignments for the peripheral board.
    try:
        exec (
            'import ' + periph_name_to_module[peripheralboard] + ' as peripheral'
        )
    except:
        raise Exception(
            'Problem importing peripheral board {0}'.format(peripheralboard))

    # Import the I/O-to-channel assignments for the motherboard.
    try:
        exec ('import ' + mbrd_name_to_module[motherboard] + ' as mother')
    except:
        raise Exception('Problem importing motherboard {0}'.format(motherboard))

    # Import the channel-to-pin assignments for the daughterboard.
    try:
        exec ('import ' + dbrd_name_to_module[daughterboard] + ' as daughter')
    except:
        raise Exception(
            'Problem importing daughterboard {0}'.format(daughterboard))

    # Get the type of port for the given port name on the motherboard and
    # get the name of the compatible port on the peripheral board.
    # (There should only be one.)
    per_port_type = get_port_type(MOTHERBRD_DIR, motherboard, port_name)
    try:
        per_port_name = get_board_port_names(PERIPHERALBRD_DIR,
                                             peripheralboard, per_port_type)[0]
    except KeyError:
        raise Exception('No {0} port found on {1} peripheral board.'.format(
            per_port_type, peripheralboard))

    # Look for a common port type between the mother and daughter boards.
    # This will be how they connect. There should only be one in the current
    # implementation of this program.
    try:
        md_port_name = get_compatible_ports(MOTHERBRD_DIR, motherboard,
                                            DAUGHTERBRD_DIR,
                                            daughterboard)[0][0]
        md_port_type = get_port_type(MOTHERBRD_DIR, motherboard, md_port_name)
    except KeyError:
        raise Exception('No matching port type for {0} and {1}.'.format(
            motherboard, daughterboard))

        # Get the list of net-to-I/O assignments for the peripheral board.
    try:
        nets = peripheral.brd['port'][per_port_type][per_port_name].items()
    except KeyError:
        raise Exception('No {0} port found on {1} peripheral board.'.format(
            per_port_type, peripheralboard))

    # For each net-to-I/O assignment in the peripheral board...
    pin_assignment = {}  # Start with no pin assignments.
    for net_io in nets:
        # ... search in the motherboard for the matching I/O and the associated channel ...
        try:
            mother_ch = mother.brd['port'][per_port_type][port_name][net_io[1]]
        except KeyError:
            raise Exception(
                'Unknown {0} I/O pin for connecting {1} port of {2} peripheral board to {3} port of {4} motherboard'.format(
                    net_io[1], per_port_type, peripheralboard, port_name,
                    motherboard))

        # ... then search in the daughterboard for the matching channel and the associated pin.
        try:
            daughter_ch = mother.brd['port'][md_port_type][md_port_name][mother_ch]
            daughter_pin = daughter.brd['port'][md_port_type][md_port_name][daughter_ch]
        except KeyError:
            raise Exception(
                'Unknown {0} channel from {1} motherboard to channel {2} of {3} daughterboard:'.format(
                    mother_ch, motherboard, daughter_ch, daughterboard))

        # Assign the daughterboard pin to the net of the peripheral.
        pin_assignment[net_io[0]] = daughter_pin

    return pin_assignment


def arguments_to_string(periphbrd, motherbrd, port, daughterbrd):
    '''Create a string showing the connection of the boards to each other.'''
    return '# {0} ==[{1}]==> {2} ==> {3}\n'.format(periphbrd, port, motherbrd,
                                               daughterbrd)


def assignments_to_string(periphbrd, motherbrd, port, daughterbrd, pin_assignment):
    '''Create a string of the board connections and the net-to-pin assignments.'''
    str = '#' * 72 + '\n'
    str += arguments_to_string(periphbrd, motherbrd, port, daughterbrd)
    width = max([len(net) for net in pin_assignment.keys()])
    for net in sorted(pin_assignment.keys()):
        str += 'net {0:{1}s} loc = {2};\n'.format(net, width, pin_assignment[net],)
    str += '#' * 72 + '\n'
    return str


def print_assignments(periphbrd, motherbrd, port, daughterbrd, pin_assignment):
    '''Print the list of net-to-pin assignments.'''
    print assignments_to_string(periphbrd, motherbrd, port, daughterbrd, pin_assignment)
