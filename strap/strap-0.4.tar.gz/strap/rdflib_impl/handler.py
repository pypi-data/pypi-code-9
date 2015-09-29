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

from strap.server import StrapHandler

from rdflib import URIRef, BNode, Literal
import rdflib.plugin

class StrapGraphHandlerRO (StrapHandler):
    """
    The C{triples} method of the graphs is assumed to be thread safe.

    @param send : the send method used by the STRAP protocol
    @param recv : the send method used by the STRAP protocol
    @param graph: the rdflib graph
    @param metadata_url: the URL of the metadata about that graph
    """
    def __init__ (self, send, recv, graph, metadata_url=u""):
        StrapHandler.__init__ (self, send, recv, URIRef, BNode, Literal)
        self._graph = graph
        self.__meta = metadata_url

    def triples (self, s, p, o):
        return self._graph.triples ((s, p, o))

    def meta (self):
        return self.__meta

class StrapGraphHandler (StrapGraphHandlerRO):
    """
    The C{triples} method of the graphs is assumed to be thread safe.
    Methods C{add} and C{remove} however, are never called concurently,
    they are protected by the given lock.

    @param send : the send method used by the STRAP protocol
    @param recv : the send method used by the STRAP protocol
    @param graph: the rdflib graph
    @param lock : a lock used to prevent concurent modification
    @param metadata_url: the URL of the metadata about that graph
    """
    def __init__ (self, send, recv, graph, metadata_url=u"", lock=None):
        StrapGraphHandlerRO.__init__ (self, send, recv, graph, metadata_url)
        self.__lock = lock

    def add (self, subject, predicate, object):
        mutex = self.__lock
        if mutex: mutex.acquire()
        try:
            self._graph.add ((subject, predicate, object))
            return -1
        finally:
            if mutex: mutex.release()

    def remove (self, subject, predicate, object):
        mutex = self.__lock
        if mutex: mutex.acquire()
        try:
            self._graph.remove ((subject, predicate, object))
            return -1
        finally:
            if mutex: mutex.release()
