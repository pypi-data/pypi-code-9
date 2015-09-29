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
"""
@var _ALIVE : L{StrapTripleIterator} state indicating that the iterator is 
              still using the communication stream (but may be inactive,
              meaning that a more recent iterator is using it instead)
@var _CACHE : L{StrapTripleIterator} state indicating that the iterator is 
              not using the communication stream anymore, but still has triples
              to deliver in its cache.
@var _EMPTY : L{StrapTripleIterator} state indicating that the iterator is 
              empty -- hence of course not using the communication stream
              anymore.
"""

from strap     import *
from socket    import socket
from sys       import stderr
from warnings  import warn
from weakref   import ref as weakref, proxy as weakproxy
try:
    from socket import AF_UNIX
except ImportError:
    AF_UNIX = None

import sys
DEBUG_LOG = sys.stderr

class IllFormedIteratorUse (Warning):
    """
    Issued whenever an iterator is used before iterators stacked over it are
    closed.
    @see L{StrapTripleIterator}
    """
    pass

# iterator states
_ALIVE = 2 # still using the communication stream
_CACHE = 1 # not using the communication stream, but cache not empty
_EMPTY  = 0 # empty

class StrapTripleIterator (object):
    """
    This object is an iterator yielding the results of a strap T command.

    If this iterator is used while another iterator is stacked over it, an
    L{IllFormedIteratorUse} will be issued (see L{StrapClient}).

    @var window : the number of triples retrieved at a time from the server
                  (of course, C{next} always return one at a time).
                  IMPORTANT: NOT USED IN THE CURRENT IMPLEMENTATION.
    @var empty  : whether this iterator is empty
    @var alive  : whether this iterator is still in communication with the
                  server (though it might not be the I{active} iterator, i.e.
                  the topmost iterator in the iterator stack)

    @see L{StrapClient.triples}
    """

    def __init__ (self, parent, s, p, o):
        self.__parent = parent # the StrapClient creating us
        self.__filter = s,p,o
        self.__state  = _ALIVE
        self.window   = parent.window

    # attributes

    @property
    def empty (self):
        return self.__state == _EMPTY

    @property
    def alive (self):
        return self.__state == _ALIVE

    # private and protected methods


    def __check_illformed (self, do_warn=True):
        """
        Check that this iterator is the active iterator of its parent client.
        If it is not, issue a L{IllFormedIteratorUse} warning and flush alive
        iterators until it becomes active.

        @see : L{__flush_all}
        """
        if self.__state < _ALIVE:
            return
        get_active = self.__parent._get_active_iter
        active = get_active()
        if active is not self:
            raise IllFormedIteratorUse, "Iterators not correctly embeded"

    def _flush_stream (self):
        """
        Flush the communication stream with the server, and keep everything
        in the cache.
        """
        pass

    def __abort (self):
        """
        Flush the communication stream and abort the TRIPLES command.
        Assumes that this iterator is *active*.
        """
        self._flush_stream ()
        send_int (self.__parent.send, 0)
        self.__state = _EMPTY

    # public methods

    def __iter__ (self):
        return self

    def next (self):
        if self.__state != _ALIVE:
            raise StopIteration
        self.__check_illformed()

        p    = self.__parent
        send = p.send

        send_int (send, 1)
        try:
            args = (send, p.recv, p.uri_maker, p.bnode_maker, p.lit_maker)
            s = recv_node (*args)
            p = recv_node (*args)
            o = recv_node (*args)
        except StrapNoMoreTriples:
            self.__state = _EMPTY
            raise StopIteration

        f = self.__filter
        if s is None: s = f[0]
        if p is None: p = f[1]
        if o is None: p = f[2]
        return (s,p,o)

    def abort (self):
        """
        Forcibly abort the query.
        Does nothing is the iterator is not alive.
        """
        print >> DEBUG_LOG, "=== aborting forcibly"
        self.__check_illformed()
        if self.__state == _ALIVE:
            self.__abort()


    def __del__ (self):
        #print >> DEBUG_LOG, >> DEBUG_LOG, "=== deleting iterator", id(self)
        if self.__state >= _ALIVE:
            self.__abort()


class StrapClient (StrapBase):
    """
    A class implementing the client side of the Streaming RDF Access
    Protocol (Strap).

    WARNING: this class implements a single communication channel with a Strap
    server; as a result, this class is *not* thread safe. Furthermore,
    iterables generated with =triples= are stacked, i.e. older ones are not
    supposed to be used until more recent ones are emptied or explicitely
    closed. Should this happen, an L{IllFormedIteratorUse} exception is raised.
    In the future, this will only be a Python warning, and the recent iterators
    will be flushed and cached in memory. This will work, but may take a lot of
    time and memory, hence the warning.
    
    @var window  : the default window for created L{StrapTripleIterator}s
    """


    def __init__ (self, *a, **kw):
        StrapBase.__init__ (self, *a, **kw)
        self.__iter_stack = []
        self.__active_iter = lambda: None
        self.window = 1

    # private and protected methods

    def _get_active_iter (self):
        a = self.__active_iter()
        s = self.__iter_stack
        if a is not None and not a.alive:
            a = None
        while a is None and len (s) > 0:
            a = s.pop()
            if not a.alive:
                a = None
        if a is not None:
            self.__active_iter = weakref (a)
        assert (a is None or a.alive)
        return a

    def __stack_if_needed(self, triples=False):
        """
        If required (i.e. if C{_get_active_iter} does not return None),
        flush the active iter and send a STACK subcommand.

        @triples : must be True if the command to STACK is TRIPLES
        """
        a = self._get_active_iter()
        while a is not None:
            a._flush_stream()
            if a.alive:
                break
            else:
                assert (a is not self._get_active_iter())
                a = self._get_active_iter()
        if a is not None:
            # flushing the communication stream did not finish the iterator
            self.send (PREFIX+STACK)
            if triples:
                self.__iter_stack.append (a)
                #print >> DEBUG_LOG, "=== iter_stack", [id(i) for i in self.__iter_stack]

    # public methods

    def triples (self, s, p, o):
        """
        Iterate over the triples matching the given triple-filter.

        The filter is described by C{s}, C{p} and C{o} which can be either None
        or instances of the classes C{self.uri_cls}, C{self.bnode} and
        C{self.lit} (with the usual constraints on RDF triples).
        """
        self.__stack_if_needed(True)

        #print >> DEBUG_LOG, "=== sending filter", s, p, o
        send_nodes (
            self.send, TRIPLES, (s,p,o),
            self.uri_cls, self.bnode_cls, self.lit_cls,
        )
        #print >> DEBUG_LOG, "=== filter sent"

        r = StrapTripleIterator (self, s, p, o)
        self.__active_iter = weakref (r)
        #print >> DEBUG_LOG, "=== push active", id(r), id(self.__active_iter)
        return r

    def add (self, subject, predicate, object):
        """
        Add the given triple.

        Return the integer value returned by the server.
        """
        self.__stack_if_needed()
        send_nodes (
            self.send, ADD, (subject, predicate, object),
            self.uri_cls, self.bnode_cls, self.lit_cls,
        )
        return recv_int (self.recv)

    def remove (self, subject, predicate, object):
        self.__stack_if_needed()
        send_nodes (
            self.send, REMOVE, (subject, predicate, object),
            self.uri_cls, self.bnode_cls, self.lit_cls,
        )
        return recv_int (self.recv)

    def meta (self):
        self.__stack_if_needed()
        self.send (META)
        return recv_str (self.recv)


    def __del__ (self):
        try:
            a = self._get_active_iter()
            while a is not None:
                a.abort()
                a = self._get_active_iter()
        except AttributeError:
            # may happen if __del__ is called before __init__
            pass


class StrapSocketClient (StrapClient):
    """
    A subclass of L{StrapClient} specialized in socket connection.

    Its constructor accepts a URL (see below) followed by the node classes and
    factory expected by L{StrapBase}.

    Accepted URLs are:
        * relative of absolute file names
        * file:/// URLs
        * strap:/// (equivalent to file:///)
        * strap://host:port/path URLs (port is required)
    """
    def __init__ (self, url, *a, **k):
        addr, path = url2addrpath (url)
        if isinstance (addr, basestring):
            if AF_UNIX is None:
                raise StrapInternalError, \
                    "UNIX (file like) socket not supported"
            s = socket (AF_UNIX)
        else:
            s = socket()
        s.connect (addr)
        self.__socket = s

        StrapClient.__init__ (self, s.send, s.recv, *a, **k)

        if path is not None:
            send_str (s.send, path)

    def __del__ (self):
        super (StrapSocketClient, self).__del__()
        try:
            self.__socket.close()
        except AttributeError:
            pass

