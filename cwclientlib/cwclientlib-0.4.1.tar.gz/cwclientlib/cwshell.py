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

from code import interact

from .cwcompleter import setup_autocompleter
from . import cwproxy_for, get_config
from .cwproxy import CWProxy

import argparse
try:
    import argcomplete
except ImportError:
    argcomplete = None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--server-ca', dest='ca', default=None,
                        help='Bundle CA to use to verify server certificate')
    parser.add_argument('endpoint', nargs=1,
                        choices=sorted(get_config()),
                        help='endpoint')
    if argcomplete is not None:
        argcomplete.autocomplete(parser)
    args = parser.parse_args()

    url = args.endpoint[0]
    try:
        client = cwproxy_for(url, verify=args.ca)
    except ValueError:
        if url.startswith(('http://', 'https://')):
            client = CWProxy(url, verify=args.ca)
        else:
            raise
    namespace = {'client': client,
                 'rql': client.execute,
                 'rqlio': client.rqlio}
    setup_autocompleter(client, namespace=namespace)
    interact('You are connected to {0}'.format(client.build_url('')),
             local=namespace)


if __name__ == "__main__":
    main()
