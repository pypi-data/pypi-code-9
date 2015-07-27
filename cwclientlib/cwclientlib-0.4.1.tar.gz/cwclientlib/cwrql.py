#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# copyright 2014-2015 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr/ -- mailto:contact@logilab.fr
#
# This file is part of cwclientlib.
#
# cwclientlib is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, either version 2.1 of the License, or (at your
# option) any later version.
#
# cwclientlib is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License
# for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with cwclientlib. If not, see <http://www.gnu.org/licenses/>.

from __future__ import print_function
import sys

from . import cwproxy_for, get_config
from .cwproxy import CWProxy, RemoteValidationError

import argparse
try:
    import argcomplete
except ImportError:
    argcomplete = None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('endpoint', nargs=1,
                        choices=sorted(get_config()),
                        help='endpoint')
    parser.add_argument('query', nargs=1,
                        help='RQL query')
    parser.add_argument('-c', '--server-ca', dest='ca', default=None,
                        help='Bundle CA to use to verify server certificate')
    parser.add_argument('-S', '--no-ssl', dest='verify', default=True,
                        action='store_false',
                        help=('do NOT verify ssl server certificate; '
                              'ignored if --ca is given'),)

    if argcomplete is not None:
        argcomplete.autocomplete(parser)
    args = parser.parse_args()

    url = args.endpoint[0]
    verify = args.ca or args.verify  # path to the bundle CA or bool
    try:
        client = cwproxy_for(url, verify=verify)
    except ValueError:
        if url.startswith(('http://', 'https://')):
            client = CWProxy(url, verify=verify)
        else:
            raise
    rql = args.query[0]
    try:
        print(client.execute(rql))
    except RemoteValidationError as exc:
        print('** Request failed: {0}'.format(exc),
              file=sys.stderr)
        print('** RQL was %r' % (rql,), file=sys.stderr)


if __name__ == "__main__":
    main()
