#!/usr/bin/env python

"""
Validate metadata

Copyright 2015, Outernet Inc.
Some rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

import json

import conz

from . import validator

cn = conz.Console()

try:
    FILE_ERRORS = (IOError, OSError, FileNotFoundError)
except NameError:
    FILE_ERRORS = (IOError, OSError,)


def load(path):
    """ Load JSON data from file """
    with open(path, 'r') as f:
        data = json.load(f)
    return data


def validate_path(path):
    path = path.strip()
    try:
        data = load(path)
    except FILE_ERRORS:
        cn.pverr(path, 'file not found')
        raise RuntimeError()
    except ValueError:
        cn.pverr(path, 'invalid JSON format')
        raise RuntimeError()
    errors = validator.validate(data)
    if errors:
        cn.pstd(cn.color.red('{} ERR'.format(path)))
        for key, err in sorted(errors.items(), key=lambda x: x[0]):
            err, _ = err.args
            cn.pverb('{}: {}'.format(key, cn.color.red(err)))
        return 1
    cn.pstd(cn.color.green('{} OK'.format(path)))
    return 0


def main():
    from .argutil import getparser

    parser = getparser('Validate metadata file',
                       usage='\n    %(prog)s [-h] [-V] PATH\n    '
                       'PATH | %(prog)s [-h] [-V]')
    parser.add_argument('paths', metavar='PATH', help='optional path to '
                        'metadata file (defaults to info.json in current '
                        'directory, ignored if used in a pipe)',
                        default=['./info.json'], nargs='*')
    args = parser.parse_args()

    if cn.interm:
        cn.verbose = True
        src = args.paths
    else:
        src = cn.readpipe()

    for p in src:
        try:
            validate_path(p)
        except RuntimeError:
            cn.pstd(cn.color.red('{} ERR'.format(p)))


if __name__ == '__main__':
    main()
