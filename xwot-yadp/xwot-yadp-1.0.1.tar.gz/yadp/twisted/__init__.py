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
__all__ = ['client', 'Client', 'Service', 'service', 'debug', 'quiet']

from twisted.internet import protocol
from twisted.internet import task
import logging
from yadp.core import BaseService, constant
from yadp.core import BaseClient

from yadp.twisted.adapter.unicast import TCPSender as Adapter_TCPSender
from yadp.twisted.adapter.unicast import TCPReceiver as Adapter_TCPReceiver
from yadp.twisted.adapter.unicast import UDPReceiver as Adapter_U_UDPReceiver
from yadp.twisted.adapter.multicast import UDPReceiver as Adapter_M_UDPReceiver
from yadp.core import multicast

logger = logging.getLogger('twisted')


class FactoryHelper(protocol.Factory):

    def __init__(self, protocol_class, dispatcher):
        self._protocol_class = protocol_class
        self._dispatcher = dispatcher

    def buildProtocol(self, addr):
        return self._protocol_class(self._dispatcher)


def debug():
    logging.basicConfig(level=logging.DEBUG)


def quiet():
    logging.basicConfig(level=logging.NOTSET)


class Client(BaseClient):

    def __init__(self, reactor, port=constant.UNICAST_PORT):
        self._reactor = reactor
        logger.debug('create client')
        u_receiver_fac = FactoryHelper(Adapter_TCPReceiver, self.dispatch)  # **1
        reactor.listenTCP(port, u_receiver_fac)  # **2

        # for udp use this line here and comment lines **1, **2 and **3
        #reactor.listenUDP(constant.UNICAST_PORT, Adapter_U_UDPReceiver(self.dispatch))

        m_receiver = Adapter_M_UDPReceiver(self.dispatch)
        reactor.listenMulticast(constant.MULTICAST_PORT, m_receiver, listenMultiple=True)

        m_sender = multicast.UDPSender()

        super(Client, self).__init__(port, m_sender)

    def _hook_init(self):
        cleanup_task = task.LoopingCall(self._cleanup)
        cleanup_task.start(20.0)  # every 20 seconds

    def run(self, run_reactor=True):
        if run_reactor:
            self._reactor.run()


class Service(BaseService):

    def __init__(self, reactor):
        self._reactor = reactor
        logger.debug('create service')
        m_receiver = Adapter_M_UDPReceiver(self.dispatch)
        reactor.listenMulticast(constant.MULTICAST_PORT, m_receiver, listenMultiple=True)

        m_sender = multicast.UDPSender()
        u_sender = Adapter_TCPSender(reactor)  # **3

        # for udp use this line here and comment line **3
        # u_sender = unicast.UDPSender

        super(Service, self).__init__(m_sender=m_sender, u_sender=u_sender)

    def _hook_init(self):
        announcement_task = task.LoopingCall(self._send_announcements)
        announcement_task.start(20.0)  # every 20 seconds

    def run(self, run_reactor=True):
        if run_reactor:
            self._reactor.run()

YADP_SERVICE = None
YADP_CLIENT = None


def client(reactor, port=constant.UNICAST_PORT):
    global YADP_CLIENT
    if YADP_CLIENT is None:
        YADP_CLIENT = Client(reactor=reactor, port=port)
    return YADP_CLIENT


def service(reactor):
    global YADP_SERVICE
    if YADP_SERVICE is None:
        YADP_SERVICE = Service(reactor=reactor)
    return YADP_SERVICE