#!/usr/bin/env python

from twisted.internet.task import react
from twisted.internet.defer import inlineCallbacks
import txtorcon


@inlineCallbacks
def main(reactor):
    state = yield txtorcon.build_local_tor_connection(reactor)
    for circuit in state.circuits.values():
        first_relay = circuit.path[0]
        print "Circuit {} first hop: {}".format(circuit.id, first_relay.ip)
#    x = yield state.protocol.get_info('desc/id/B69D45E2AC49A81E014425FF6E07C7435C9F89B0')
#    x = yield state.protocol.get_info('desc/id/EAA0E6A2CD95F5AFF46CDF042623DE79C19E028A')
    x = yield state.protocol.get_info('desc/id/EAA0E6A2CD95F5AFF46CDF042623DE79C19E028A')
    print x

    if False:
        from guppy import hpy
        print "heap:"
        print hpy().heap()

if __name__ == '__main__':
    react(main)
