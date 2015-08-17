#!/bin/env python3

# Copyright Louis Paternault 2015
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Command line client to :mod:`evs`"""

import argparse
import os
import textwrap
import glob
import sys
import re

import evariste

COMMAND_RE = re.compile(r'.*evs-(?P<command>\w*)')

def get_commands():
    """Return a dictionary of available commands, mapped to their corresponding binary.
    """
    commands = {}

    pathlist = os.environ['PATH'].split(":")
    for path in pathlist:
        path = os.path.expanduser(os.path.expandvars(path.strip()))
        for program in glob.iglob(os.path.join(path, "evs-*")):
            if os.path.isfile(program) and os.access(program, os.X_OK):
                match = COMMAND_RE.match(program)
                if match:
                    commands[match.groupdict()['command']] = program
    return commands

def print_error(error):
    """Print an error message."""
    print(error, "Try '--help' for more information.")

def print_version():
    """Print program version."""
    print(evariste.VERSION)

def print_help():
    """Print help text."""
    print(textwrap.dedent("""\
        usage: evs [-h] [--version] COMMAND [ARGUMENTS]

        Helper script for the evariste tool.

        positional arguments:
            COMMAND             Command to run. Available commands are: {commands}.

        optional arguments:
          -h, --help            show this help message and exit
          --version             Show version
        """).format(
            commands=", ".join(sorted(set(get_commands().keys()))),
        ))


def main():
    """Main function"""
    arguments = sys.argv[1:]

    if len(arguments) == 0:
        print_error("Not enough arguments.")
        sys.exit(1)

    if arguments[0] in ['-h', '--help']:
        print_help()
        sys.exit(0)

    if arguments[0] == '--version':
        print_version()
        sys.exit(0)

    commands = get_commands()
    if arguments[0] in commands:
        os.execvp(
            commands[arguments[0]],
            arguments,
            )

    print_error("Unrecognized command '{}'.".format(arguments[0]))
    sys.exit(1)
