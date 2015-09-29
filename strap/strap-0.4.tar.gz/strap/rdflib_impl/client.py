#
# (c)2005 LIRIS - University Claude Bernard Lyon 1
# http://liris.cnrs.fr/
#
# Author: Pierre-Antoine CHAMPIN
# http://champin.net/
#
# This software is distributed under the terms of the GNU LGPL v2.1.
# See LICENSE.txt for more details.
#

from   strap.client    import StrapSocketClient

from   rdflib          import URIRef, BNode, Literal
from   rdflib.backends import Backend
import rdflib.plugin
from   socket          import socket, AF_UNIX

class StrapBackendException (Exception):
    pass

class StrapBackend (Backend):
    """
    An rdflib backend using the Streaming RDF Access Protocol (strap) through a
    socket (UNIX or INET).

    Note that, since this class may open several connections to the given
    socket, the server is assumed to be synchronous (i.e. changes made through
    a connection are immediately reflected in other connections).
    """

    def __init__ (self, url, strap_window=1):
        self.context_aware = False
        self.__url          = url
        self.__strap_window = strap_window
        self.__c            = StrapSocketClient (url, URIRef, BNode, Literal)
        self.__prefix       = {}
        self.__namespace    = {}

    def __len__ (self):
        strap = self.__c
        old_window = strap.window
        strap.window = -1
        length = 0
        for t in strap.triples (None, None, None):
            length += 1
        strap.window = old_window
        return length

    def bind (self, prefix, namespace):
        self.__prefix[namespace] = prefix
        self.__namespace[prefix] = namespace

    def namespace(self, prefix):
        return self.__namespace.get(prefix, None)

    def prefix(self, namespace):
        return self.__prefix.get(namespace, None)

    def namespaces(self):
        return self.__namespace.iteritems()

    def add (self, (subject, predicate, object)):
        self.__c.add (subject, predicate, object)

    def remove (self, (subject, predicate, object)):
        self.__c.remove (subject, predicate, object)

    def triples (self, (subject, predicate, object)):
        return self.__c.triples (subject, predicate, object)

rdflib.plugin.register ('Strap', Backend, 'strap.client_rdflib', 'StrapBackend')
