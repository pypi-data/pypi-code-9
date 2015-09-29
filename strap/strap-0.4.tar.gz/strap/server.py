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

from strap  import *
from socket import socket
from sys    import stderr
from thread import start_new_thread

DEBUG_LOG = stderr

try:
    from socket import AF_UNIX
except ImportError:
    AF_UNIX = None

class StrapHandler (StrapBase):
    """
    An abstract class implementing the server side of the Streaming RDF Access
    Protocol (Strap).

    Methods L{triples}, L{query}, L{add} and L{remove} must be overriden by
    subclasses.
    """

    def handle (self):
        send = self.send
        recv = self.recv
        loop = True
        while (loop):
            loop = self.handle_one (send, recv)

    def handle_one (self, send, recv):
        try:
            cmd = safe_recv (recv)
        except StrapProtocolError:
            return False
        #print >> DEBUG_LOG, "--- cmd", cmd
        if cmd == TRIPLES:
            try:
                self.handle_triples (send, recv)
            except StopIteration:
                #print >> DEBUG_LOG, "--- aborting triples"
                pass
        elif cmd == ADD:
            self.handle_add (send, recv)
        elif cmd == REMOVE:
            self.handle_remove (send, recv)
        elif cmd == META:
            self.handle_meta (send, recv)
        else:
            error (send, "Unknown command %s" % cmd)
        return True

    def __recv_triple (self, send, recv, uri=None, bnode=None, lit=None):
        uri   = uri   or self.uri_maker
        bnode = bnode or self.bnode_maker
        lit   = lit   or self.lit_maker
        err   = lambda pos, typ: \
                    lambda *a: error ("%s cannot be %s" % (pos, typ))

        subj = recv_node (send, recv, uri, bnode,
            err("Subject", "literal"))
        pred = recv_node (send, recv, uri,
            err("Predicate", "blank node"), err("Subject", "literal"))
        obj  = recv_node (send, recv, uri, bnode, lit)
        #print >> DEBUG_LOG, "--- received triples"#, subj, pred, obj
        return subj, pred, obj

    def __recv_todo (self, send, recv, todo=0):
        if todo < 0:
            return -1
        while True:
            try:
                r = recv_int (recv)
                if r == 0:
                    raise StopIteration, "aborted by client"
                return r
            except StrapStackReceived:
                #print >> DEBUG_LOG, "--- PUSHING CONTEXT"
                self.handle_one (send, recv)
                #print >> DEBUG_LOG, "--- POPPING CONTEXT"

    def handle_triples (self, send, recv):
        """
        Handle a TRIPLES query.
        Raise a C{StopIteration} if aborted forcibly by the client.
        """
        BUFFER_MAX = 15 # number of nodes sent in a row if todo == -1
        uri   = self.uri_maker
        bnode = self.bnode_maker
        lit   = self.lit_maker
        rtodo = self.__recv_todo

        subj, pred, obj = self.__recv_triple (send, recv, uri, bnode, lit)

        todo   = rtodo (send, recv)
        buffer = []
        for s,p,o in self.triples (subj, pred, obj):
            if subj is not None: s = None # do not re-send constrained node
            if pred is not None: p = None # idem
            if obj  is not None: o = None # idem
            buffer.extend ((s,p,o))
            todo -= 1
            if todo == 0 or todo < -BUFFER_MAX:
                # todo == 0 if a positive number was given and reached
                # todo < -BUFFER_MAX if FLUSH (-1) was given
                #print >> DEBUG_LOG, "--- sending"
                send_nodes (send, "", buffer, uri, bnode, lit)
                del buffer[:]
                todo = rtodo (send, recv, todo)
                #print >> DEBUG_LOG, "--- continuing for", todo

        if todo == 0:
            todo = rtodo (send, recv)
            #print >> DEBUG_LOG, "--- continuing for", todo
        elif todo < 0:
            #print >> DEBUG_LOG, "--- sending tail"
            send_nodes (send, "", buffer, uri, bnode, lit)
        #print >> DEBUG_LOG, "--- end of triples result"
        send (END)

    def handle_add (self, send, recv):
        subj, pred, obj = self.__recv_triple (send, recv)
        if subj is None: error (send, "Cannot add triples with blank subject")
        if pred is None: error (send, "Cannot add triples with blank predicate")
        if obj  is None: error (send, "Cannot add triples with blank object")

        try:
            send_int (send, self.add (subj, pred, obj))
        except StrapInternalError, ex:
            error (send, ex)
            raise ex

    def handle_remove (self, send, recv):
        subj, pred, obj = self.__recv_triple (send, recv)
        try:
            send_int (send, self.remove (subj, pred, obj))
        except StrapInternalError, ex:
            error (send, ex)
            raise ex
    
    def handle_meta (self, send, recv):
        try:
            send_str (send, self.meta())
        except StrapInternalError, ex:
            error (send, ex)


    def triples (self, s, p, o):
        """
        ABSTRACT:
        iterate over the results of the given triple-filter.

        The filter is described by C{s}, C{p} and C{o} which can be either None
        or instances of the classes C{self.uri_cls}, C{self.bnode} and
        C{self.lit} (with the usual constraints on RDF triples).
        """
        pass
    
    def add (self, s, p, o):
        """
        ABSTRACT: (actually default implementation fails)
        add the given triple

        return a number:
          * 1 if the triple didn't previously existed
          * 0 if it already existed
          * -1 if we can not tell

        raise a StrapInternalError on error
        """
        raise StrapInternalError ("add not supported")

    def remove (self, s, p, o):
        """
        ABSTRACT: (actually default implementation fails)
        remove the triples matching the given filter (see L{triples})

        return a number:
          * the number of removed triples
          * -1 if we can not tell

        raise a StrapInternalError on error
        """
        raise StrapInternalError ("remove not supported")
    
    def meta (self):
        """
        ABSTRACT: (actually default implementation returns u"")
        return u"" or the URI of the RDF description of this graph, as a
        unicode string.

        raise a StrapInternalError on error
        """
        return u""


class StrapSocketServer (object):
    """
    An abstract class implementing a Strap server.

    usage: StrapSocketServer (addr)

    where addr is either a file path (if the OS supports UNIX, i.e. file-like
    sockets) or a tuple containing a host name and a port number.

    UNIX-socket based server are assume to serve a single graph.

    INET-socket based server are assume to serve several graph, so before any
    command, they expect the client to send them the path of the graph (as a
    string). This is encoded at the client side in strap URLs in the form::
        strap://host:port/path

    The abstract method L{make_handler} is given the socket of an incoming
    connection and the path of the required graph (None for UNIX-socket
    servers). It is expected to return the appropriate L{StrapHandler}
    """

    def __init__ (self, addr):
        if isinstance (addr, basestring):
            if AF_UNIX is None:
                raise StrapInternalError, "UNIX (file like) socket not supported"
            serv = socket (AF_UNIX)
            self._multigraph = False
        else:
            serv = socket()
            self._multigraph = True
        serv.bind (addr)
        self.__s = serv

    def serve_forever (self):
        serv  = self.__s
        serv.listen (1)
        while True:
            start_new_thread (self.handle, serv.accept())

    def handle (self, clientsocket, address):
        if self._multigraph:
            path = recv_str (clientsocket.recv)
        else:
            path = None
        handler = self.make_handler (path, clientsocket, address)
        if handler is not None:
            handler.handle()
        else:
            error (clientsocket.send, "No such graph: %s" % path)

    def make_handler (self, path, clientsocket, address):
        """
        ABSTRACT: make an appropriate L{StrapHandler}

        @param path: the path of the required graph, or None if the server is
          based on a UNIX-socket
        @param clientsocket: the socket open by the client
        @param address: the address of the client
        @return: an appropriate handler, None if path is wrong
        """
        raise NotImplementedException
