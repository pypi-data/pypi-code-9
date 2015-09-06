#!/usr/bin/env python

from twisted.python import log
from twisted.internet import reactor, defer
from zope.interface import implements

import txtorcon


class MyAttacher(object):
    implements(txtorcon.IStreamAttacher)

    def __init__(self, state):
        # pointer to our TorState object
        self.state = state

    @defer.inlineCallbacks
    def attach_stream(self, stream, circuits):
        """
        IStreamAttacher API
        """

        print "XXXX", stream
        x = yield self.state.protocol.queue_command('REDIRECTSTREAM %s timaq4ygg2iegci7.onion' % stream.id)
        print "X", x

        defer.returnValue(None)
#        x = yield self.state.protocol.queue_command('ATTACHSTREAM %s 0' % stream.id)
#        print "X", x


def do_setup(state):
    print "Connected to a Tor version", state.protocol.version

    attacher = MyAttacher(state)
    state.set_attacher(attacher, reactor)

    print "Existing state when we connected:"
    print "Streams:"
    for s in state.streams.values():
        print ' ', s

    print
    print "General-purpose circuits:"
    for c in filter(lambda x: x.purpose == 'GENERAL', state.circuits.values()):
        print ' ', c.id, '->'.join(map(lambda x: x.location.countrycode,
                                       c.path))


def setup_failed(arg):
    print "SETUP FAILED", arg
    reactor.stop()

d = txtorcon.build_local_tor_connection(reactor)
d.addCallback(do_setup).addErrback(setup_failed)
reactor.run()
