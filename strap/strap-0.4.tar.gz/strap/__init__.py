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

PACKAGE_VERSION = "0.4"
PROTOCOL_VERSION = "0.3"

# general
ERROR   = '\xff'
ANY     = '*'
END     = '.'
# commands
TRIPLES = 'T'
ADD     = 'A'
REMOVE  = 'R'
META    = 'M'
# subcommands
PREFIX  = '\xfe'
FLUSH   = 'F'
STACK   = 'S'
# node types
URIREF  = 'U'
BNODE   = 'B'
LITERAL = 'L'

class StrapInternalError (Exception):
    """
    A fatal error on this side.
    """
    pass

class StrapPeerError (Exception):
    """
    An error notified by the peer.
    """
    pass

class StrapProtocolError (Exception):
    """
    A protocol error from the peer.
    """
    pass


class StrapStackReceived (Exception):
    """
    Raised by _recv_int when a STACK signal is received.
    """
    pass

class StrapNoMoreTriples (Exception):
    """
    Raised by _recv_node when END is received.
    """
    pass


from sys import stderr
DEBUG_LOG = stderr

def safe_recv (recv):
    """
    Receive one byte and checks whether it is the error signal.

    If so, raises a StrapPeerError, else return it.

    @param recv: the function used to receive data
    @param pass_empty: whether to ignore empty input
    @return: the read byte
    """
    r = recv(1)
    if r == '':
        raise StrapProtocolError, "peer unexpectedly closed connection"
    elif r == ERROR:
        msg = recv_str (recv)
        raise StrapPeerError, msg
    return r

def _encode_int (i):
    """
    Return encoded int i.
    @param i: a positive int or -1
    """
    l = []
    while i:
        l.insert (0, i & 0xff)
        i >>= 8
    n = len (l) # nb 
    ones  = 0
    bytes = 1 # == 2**ones
    while bytes < n:
        ones  += 1
        bytes *= 2
    mask = ~(0x7f >> ones) & 0xff
    if bytes == n and (l[0] & mask) != 0:
        ones += 1
        bytes *= 2

    if ones > 6:
        raise TypeError, "integer is too long"

    l[0:0] = [0] * (bytes-n)
    if ones > 0:
        l[0] |= ~(0xff >> ones) & 0xff
    return "".join ([chr(i) for i in l])

def send_int (send, i):
    """
    Send encoded int i with function send.
    If i is -1, FLUSH is sent instead.

    @param send: the function used to send data
    @param i   : a non-negative int or -1
    """
    if i == -1:
        send (PREFIX+FLUSH)
    else:
        send (_encode_int (i))

def recv_int (recv, head=None):
    """
    Receive encoder int and return its value.

    @param recv: the function used to receive data
    @param head: the first char of the encoded int, if already received

    @return: the decoded int, -1 on flush
    @rtype:  int
    @exception: L{StrapStackReceived} is raised on STACK
    """
    if head is None:
        head = safe_recv (recv)
    
    if head == PREFIX:
        subcmd = recv(1)
        if subcmd == FLUSH:
            return -1
        elif subcmd == STACK:
            raise StrapStackReceived

    head  = ord(head)
    val   = head
    bytes = 1
    mask  = 0xff
    while head & 0x80:
        head <<= 1
        bytes *= 2
        mask >>= 1
    val = val & mask
    if bytes > 1:
        tail = recv(bytes-1)
        for c in tail:
            val <<= 8
            val |= ord(c)
    return val

def _encode_str (st):
    """
    Return encoded string st.
    @param st: a str in the default codec or a unicode
    """
    st = unicode (st).encode ("utf8")
    return _encode_int (len (st)) + st

def send_str (send, st):
    """
    Send string st with function send.

    @param send: the function used to send data
    @param st  : a str in the default codec or a unicode
    """
    send (_encode_str (st))

def recv_str (recv, head=None):
    """
    Receive a string.

    @param recv: the function used to receive data
    @param head: the first char of the formated string, if already received

    @return: a unicode
    """
    l = recv_int (recv, head)
    if l == 0:
        return u""
    else:
        return unicode (recv(l))

def _encode_node (n, uri_cls, bnode_cls, lit_cls):
    """
    Return encoded node n.

    @param n         : the node to encode
    @param uri_cls   : the class of URI nodes
    @param bnode_cls : the class of blank nodes
    @param lit_cls   : the class of literal nodes
    """
    if n is None:
        return (ANY)
    elif isinstance (n, uri_cls):
        return (URIREF + _encode_str (str (n)))
    elif isinstance (n, bnode_cls):
        return (BNODE + _encode_str (str (n)))
    elif isinstance (n, lit_cls):
        return (LITERAL
            + _encode_str (str (n))
            + _encode_str (str (n.language or ""))
            + _encode_str (str (n.datatype or ""))
        )
    else:
        raise TypeError, `n`

def send_node (send, n, uri_cls, bnode_cls, lit_cls):
    """
    Send a node with function send with the appropriate format.

    @param send      : the function used to send data
    @param n         : the node to send
    @param uri_cls   : the class of URI nodes
    @param bnode_cls : the class of blank nodes
    @param lit_cls   : the class of literal nodes
    """
    send (_encode_node (n, uri_cls, bnode_cls, lit_cls))
    #print >> DEBUG_LOG, "=== sent node", n

def recv_node (send, recv, uri_maker, bnode_maker, lit_maker, head=None):
    """
    Send a node with function send with the appropriate format, or raise a
    L{StrapNoMoreTriples} if END is received.

    @param recv        : the function used to recv data
    @param uri_maker   : a callable for making URI nodes
    @param bnode_maker : a callable for making blank nodes
    @param lit_maker   : a callable for making literals
    """
    if head is None:
        head = safe_recv (recv)
    
    if head == END:
        raise StrapNoMoreTriples, "No more triples"
    elif head == ANY:
        obj = None
    elif head == URIREF:
        obj = uri_maker (recv_str (recv))
    elif head == BNODE:
        obj = bnode_maker (recv_str (recv))
    elif head == LITERAL:
        obj = lit_maker (
            recv_str (recv), # value
            recv_str (recv), # language
            recv_str (recv), # datatypetype uri
        )
    else:
        error (send, "Unrecognized format %s" % head, StrapProtocolError)
    #print >> DEBUG_LOG, "=== received node", obj
    return obj

def send_nodes (send, prefix, ns, uri_cls, bnode_cls, lit_cls):
    """
    Send a list of nodes with function send with the appropriate format.

    @param send      : the function used to send data
    @param prefix    : a prefix to be sent befor the nodes
    @param ns        : an iterable of nodes
    @param uri_cls   : the class of URI nodes
    @param bnode_cls : the class of blank nodes
    @param lit_cls   : the class of literal nodes
    """
    send (prefix + "".join(
        [_encode_node (n, uri_cls, bnode_cls, lit_cls) for n in ns]
    ))
   
def error (send, msg, cls=StrapInternalError):
    """
    Report error to other side, and raise an exception of class C{cls}.
    """
    send (ERROR + _encode_str (msg))
    raise cls, msg



class StrapBase (object):
    """
    A common base for StrapClient and StrapServer.

    @see: L{strap.client.StrapClient}
    @see: L{strap.server.StrapServer}
    """
    def __init__ (
        self,
        send,
        recv,
        uri_cls, bnode_cls, lit_cls,
        uri_maker=None, bnode_maker=None, lit_maker=None,
    ):
        """
        send/recv must comply with the send/recv methods of sockets, or with
        the write/read methods of files.

        @param send       : a function used to send data
        @param recv       : a function used to receive data
        @param uri_cls    : the class of URI nodes
        @param bnode_cls  : the class of blank nodes
        @param lit_cls    : the class of literal nodes; must have C{language}
                            and C{datatype} attributes
        @param uri_maker  : a callable accepting 1 argument and returning an
                            instance of C{uri_cls} (defaults to C{uri_cls})
        @param bnode_maker: a callable accepting 1 argument and returning an
                            instance of C{bnode_cls} (defaults to C{bnode_cls})
        @param lit_maker  : a callable accepting 3 arguments (literal, lang,
                            type uri) and returning an instance of C{lit_cls}
                            (defaults to C{lit_cls})
        """
        self.send        = send
        self.recv        = recv
        self.uri_cls     = uri_cls
        self.bnode_cls   = bnode_cls
        self.lit_cls     = lit_cls
        self.uri_maker   = uri_maker or uri_cls
        self.bnode_maker = bnode_maker or bnode_cls
        self.lit_maker   = lit_maker or lit_cls



def url2addrpath (url):
    """
    Return a tuple (addr,path) corresponding to the given URL.

    Accepted URLs are:
        * relative of absolute file names
        * file:/// URLs
        * strap:/// (equivalent to file:///)
        * strap://host:port/path URLs (port is required)

    In the first 3 cases, the URL points to a UNIX socket path; the returned
    addr is the path of the socket as a string, and path is None (STRAP on a
    UNIX socket does not allows several graphs).

    In the 4th case, the URL points to an INET socket; the return addr is a
    tuple (host, port) and the path is the path part of the URL.

    """
    if url.startswith ("strap:///"):
        # change local strap URL to plain file name
        url = url[8:]
    if url.startswith ("strap://"):
        # distant strap URL
        url = url[8:]
        i = url.index('/')
        addr, path = url[:i], url[i:]
        addr = addr.split(':')
        if len (addr) == 1:
            raise StrapInternalError, "port number is required in strap URLs"
        addr = ( addr[0], int(addr[1]) )
    else:
        # file name or file URL
        if url.startswith ("file:///"):
            url = url[7:]
        addr = url
        path = None
    return addr, path
