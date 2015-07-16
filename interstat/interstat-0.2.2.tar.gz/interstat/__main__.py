"""Command line entry points."""


from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

import argparse
import io
from os.path import basename, splitext

from pkg_resources import require

from . import __name__ as PACKAGE_NAME, file_as_html
from .formats import formats


def patharg(path, default_fd=0):
    """Return *default_fd* if *path* is the string `"-"` or empty, or
    *path* otherwise."""
    if not path or path == '-':
        return default_fd
    return path


def main():
    """Default command line entry point."""
    parser = argparse.ArgumentParser(
        description='Format IRC log files as HTML.')
    parser.add_argument(
        '-f', dest='format', metavar='FORMAT',
        choices=formats, default='omnipresence',
        help='log format (default: omnipresence)')
    parser.add_argument(
        '-l', dest='list_formats', action='store_true',
        help='list known formats and exit')
    parser.add_argument(
        '--stylesheet', metavar='URI',
        help='use stylesheet URI instead of inlining default styles')
    parser.add_argument(
        '--template-dir', metavar='DIR',
        help='override the default templates with those in DIR')
    parser.add_argument(
        '--title',
        help='HTML page <title> (default: log file basename)')
    parser.add_argument(
        '--variable', dest='variables', metavar='KEY=VALUE',
        action='append', default=[],
        help='specify a custom template variable '
             '(may be used multiple times)')
    parser.add_argument(
        '--version', action='version',
        version='%(prog)s ' + require(PACKAGE_NAME)[0].version)
    parser.add_argument(
        'log_path', metavar='LOGFILE', nargs='?',
        help='log file to format (default: stdin)')
    parser.add_argument(
        'html_path', metavar='HTMLFILE', nargs='?',
        help='output HTML file (default: stdout)')
    args = parser.parse_args()
    if args.list_formats:
        print(', '.join(formats))
        return
    # Handle custom template variables.
    kwargs = dict()
    if args.stylesheet is not None:
        kwargs['stylesheet'] = args.stylesheet
    for declaration in args.variables:
        key, sep, value = declaration.partition('=')
        if not sep:
            parser.error('invalid variable declaration "{}"'
                         .format(declaration))
        kwargs[key] = value
    # Manually using io.open instead of delegating to argparse.FileType
    # is necessary here because the latter yields byte strings instead
    # of Unicode strings on Python 2, causing UnicodeDecodeErrors down
    # the line.  This can be reverted when Python 2 support is dropped.
    with io.open(patharg(args.log_path, 0)) as log_file:
        if args.title:
            kwargs['title'] = args.title
        elif isinstance(log_file.name, int):  # file descriptor
            kwargs['title'] = 'Interstat log'
        else:
            kwargs['title'] = splitext(basename(log_file.name))[0]
        html = file_as_html(log_file, args.format,
                            template_dir=args.template_dir, **kwargs)
    with io.open(patharg(args.html_path, 1), 'w') as html_file:
        html_file.write(html)


if __name__ == '__main__':
    main()
