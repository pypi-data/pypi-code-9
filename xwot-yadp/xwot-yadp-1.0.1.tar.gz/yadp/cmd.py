#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Yadp  - Yet Another Discovery Protocol
# Copyright (C) 2015  Alexander Rüedlinger
#
# This file is part of Yadp.
#
# Yadp is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Yadp is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Yadp.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import absolute_import

__author__ = 'Alexander Rüedlinger'
__all__ = ['yadp_listener', 'semantic_yadp_listener']

from twisted.internet import task
from twisted.internet import reactor

from time import gmtime, strftime
import argparse


def _yadp_discovery_fun(client, urn):
    dt = strftime("%Y-%m-%d %H:%M:%S", gmtime())

    devices = client.discovered(urn=urn)

    print("discovered '%s' devices[%s] - %s:" % (urn, len(devices), dt))

    for device in devices:
        print("\t urn: %s, url: %s" % (device.urn, device.location))


def yadp_listener():
    """
    yadp command
    """

    import yadp
    from yadp.twisted import Client

    parser = argparse.ArgumentParser(description='yadp listener')
    parser.add_argument('-u', '--urn', dest='urn', type=str, nargs='?', help='urn filter', default=None)
    parser.add_argument('-d', '--debug', dest='debug', type=bool, nargs='?', help='show debug messages', default=False)
    parser.add_argument('-p', '--port', dest='port', type=int, nargs='?', help='port', default=2017)

    args = parser.parse_args()

    if args.debug:
        yadp.debug()

    client = Client(reactor, port=int(args.port))
    reactor.addSystemEventTrigger('before', 'shutdown', client.shutdown)

    urn = args.urn or 'urn:xwot:*'

    if not urn.startswith('urn:'):
        urn = "urn:%s" % urn

    client.browse(urn=urn)

    discovery_task = task.LoopingCall(_yadp_discovery_fun, client, urn)
    discovery_task.start(5.0)  # every 5 seconds

    reactor.run()

DEFAULT_PREFIXES = {
        'xwot': 'http://xwot.lexruee.ch/vocab/core#',
        'xwot-ext': 'http://xwot.lexruee.ch/vocab/core-ext#'
}


def _semantic_yadp_discovery_fun(client, iri):
    pretty_iri = None
    if iri is not None:
        for key, val in DEFAULT_PREFIXES.items():
            if iri.startswith(key):
                iri = iri.replace(key + ":", val)
                break

        pretty_iri = "'%s" % iri

    dt = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    resources = client.find_resources(iri)

    if pretty_iri:
        print "discovered %s resources[%s] - %s:" % (pretty_iri, len(resources), dt)
    else:
        print "discovered resources[%s] - %s:" % (len(resources), dt)

    for r in resources:
        print('-------------------------------------------------------------------------')
        print("\t%s: %s" % ('url', r.url))
        print("\t%s: %s" % ('type', r.type))
        print("\t%s: %s" % ('name', r.name))
        print("\t%s: %s" % ('description', r.description))
        print('-------------------------------------------------------------------------')
        print("")


def semantic_yadp_listener():
    """
    semantic-yadp command
    """

    import yadp
    from yadp.twisted import Client
    from yadp.semantic import Client as SemanticClient

    parser = argparse.ArgumentParser(description='semantic yadp listener')
    parser.add_argument('-i', '--iri', dest='iri', type=str, nargs='?', help="iri filter (xwot and xwot-ext short iri's are supported", default=None)
    parser.add_argument('-d', '--debug', dest='debug', type=bool, nargs='?', help='show debug messages', default=False)
    parser.add_argument('-p', '--port', dest='port', type=int, nargs='?', help='port', default=2018)

    args = parser.parse_args()

    if args.debug:
        yadp.debug()

    yadp_client = Client(reactor, port=int(args.port))
    client = SemanticClient(yadp_client=yadp_client)
    client.browse()

    discovery_task = task.LoopingCall(_semantic_yadp_discovery_fun, client, args.iri)
    discovery_task.start(5.0)  # every 5 seconds

    reactor.run()


def web_yadp():
    from yadp.util import web

    parser = argparse.ArgumentParser(description='web-yadp')
    parser.add_argument('-d', '--debug', dest='debug', type=bool, nargs='?', help='show debug messages', default=False)
    parser.add_argument('-i', '--interface', dest='interface', type=str, nargs='?', help='host', default='localhost')
    parser.add_argument('-p', '--port', dest='port', type=int, nargs='?', help='port', default=8080)

    args = parser.parse_args()
    server = web.create_server(reactor, yadp_port=2019, server_port=int(args.port), host=args.interface)
    server.run()