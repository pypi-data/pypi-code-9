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

from twisted.internet import protocol
from yadp.core import constant


class UDPReceiver(protocol.DatagramProtocol):

    def __init__(self, dispatcher):
        self._dispatcher = dispatcher

    def startProtocol(self):
        self.transport.joinGroup(constant.MULTICAST_ADDR)
        self.transport.setTTL(constant.TTL)

    def datagramReceived(self, datagram, host):
        self._dispatcher(datagram, host)
