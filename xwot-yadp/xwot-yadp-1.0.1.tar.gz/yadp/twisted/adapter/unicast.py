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

import logging
from twisted.internet import protocol
from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol
from yadp.core.unicast import Sender


logger = logging.getLogger("unicast adapter")


class TCPReceiver(protocol.Protocol):

    def __init__(self, dispatcher):
        self._dispatcher = dispatcher
        self._buffer = []  # need to use a buffer because of the MTU!

    def connectionLost(self, reason):
        peer = self.transport.getPeer()
        addr = peer.host
        data = "".join(self._buffer)
        self._dispatcher(data, addr)

    def connectionMade(self):
        self._buffer = []

    def dataReceived(self, data):
        self._buffer.append(data)


class UDPReceiver(protocol.DatagramProtocol):

    def __init__(self, dispatcher):
        self._dispatcher = dispatcher

    def datagramReceived(self, datagram, host):
        self._dispatcher(datagram, host)


class TCPSender(Sender):
    """
    TCP implementation of a simple sender (client),
    """

    def __init__(self, reactor):
        logger.debug("create tcp unicast sender")
        self._reactor = reactor

    class SendHelper(protocol.Protocol):

        def send(self, message):
            self.transport.write(message)
            self.transport.loseConnection()

        def connectionLost(self, reason):
            pass

    def _send_callback(self, p, message):
        p.send(message)

    def _send_errback(self, failure):
        logger.debug("error: %s" % failure.getErrorMessage())

    def send(self, message, ip, port):
        send_helper = self.SendHelper()
        point = TCP4ClientEndpoint(self._reactor, ip, port)  # default is constant.UNICAST_PORT)
        deferred_connection = connectProtocol(point, send_helper)
        deferred_connection.addCallback(self._send_callback, message)
        deferred_connection.addErrback(self._send_errback)

    def close(self):
        pass

