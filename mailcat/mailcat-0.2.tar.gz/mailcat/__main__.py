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
import locale
import sys

from . import Formatter
from .mailfile import iter_messages


if sys.version_info.major >= 3:
    echo = print
    stdin_bytes = sys.stdin.buffer
else:
    # in Python 2 print uses ASCII when stdout is a file or a pipe
    def echo(*args):
        encoding = encoding=locale.getpreferredencoding()
        if not encoding:
            encoding = 'UTF-8'
        print(*(arg.encode(encoding) for arg in args))
    stdin_bytes = sys.stdin


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


def format_message(msg, args):
    return Formatter(
        msg,
        all_headers=args.all_headers,
        body_type=body_type(args.html, args.raw_html),
        color=when_color(args.color),
    ).format()


def iter_all_messages(filenames):
    if not filenames:
        filenames = ['-']
    for filename in filenames:
        if filename == '-':
            for message in iter_messages(stdin_bytes): yield message
        else:
            with open(filename, 'rb') as file:
                for message in iter_messages(file): yield message


def main():
    args = parser.parse_args()

    first = True
    for message in iter_all_messages(args.filename):
        if not first:
            echo()
            echo()
        echo(format_message(message, args))
        first = False


if __name__ == '__main__':
    main()
