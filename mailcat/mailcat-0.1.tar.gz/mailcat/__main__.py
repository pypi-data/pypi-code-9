# Copyright (C) 2015  Andrey Golovizin
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import absolute_import, print_function

import argparse
import sys

from . import Formatter
from .message import UnicodeEmailMessage


def when_color(when):
    if when == 'auto':
        return sys.stdout.isatty()
    elif when == 'always':
        return True
    elif when == 'never':
        return False
    else:
        raise ValueError(when)


def body_type(html=False, raw_html=False):
    if raw_html:
        return 'raw_html'
    elif html:
        return 'html'
    else:
        return 'text'


parser = argparse.ArgumentParser(description='Viewer for MIME mail files')
parser.add_argument('filename', nargs='*')
parser.add_argument('-a', '--all-headers', action='store_true')
parser.add_argument('--html', action='store_true', help='prefer HTML body (convert to text)')
parser.add_argument('--raw-html', action='store_true', help='show HTML body as-is, (implies --html)')
parser.add_argument('--color', choices=('never', 'auto', 'always'), default='auto')


def format_message(filename, args):
    msg = UnicodeEmailMessage.fromfile(filename)
    return Formatter(
        msg,
        all_headers=args.all_headers,
        body_type=body_type(args.html, args.raw_html),
        color=when_color(args.color),
    ).format()


def main():
    args = parser.parse_args()
    if not args.filename:
        parser.print_help()
        sys.exit(2)

    first = True
    for filename in args.filename:
        if not first:
            print()
            print()
        print(format_message(filename, args))
        first = False


if __name__ == '__main__':
    main()
