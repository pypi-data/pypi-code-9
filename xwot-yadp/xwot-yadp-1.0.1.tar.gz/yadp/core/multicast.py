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

import socket
import struct
import logging

from . import Sender, constant
from . import Receiver


logger = logging.getLogger('multicast')


class UDPSender(Sender):

    def __init__(self, udp_socket=None):
        logger.debug("create udp multicast sender")
        if udp_socket is None:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            self._socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, constant.TTL)
            self._socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)
            self._socket.settimeout(10)
        else:
            self._socket = udp_socket

    def send(self, message, ip=None, port=None):
        logger.debug("send message: %s" % message)
        self._socket.sendto(message, (constant.MULTICAST_ADDR, constant.MULTICAST_PORT))

    def close(self):
        self._socket.close()


class UDPReceiver(Receiver):

    def __init__(self, udp_socket=None):
        logger.debug("create udp multicast receiver")
        if udp_socket is None:
            # create multicast udp socket
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self._socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, constant.TTL)
            #self._socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)
            self._socket.bind((constant.BIND_ADDR, constant.MULTICAST_PORT))

            # don't ask me - it does the job
            # see: https://wiki.python.org/moin/UdpCommunication
            mreq = struct.pack("4sl", socket.inet_aton(constant.MULTICAST_ADDR), socket.INADDR_ANY)

            # register to multicast group
            self._socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
            self._socket.settimeout(10)
        else:
            self._socket = udp_socket

    def receive(self):
        return self._socket.recvfrom(constant.RECEIVE_MAX_BYTES)

    def close(self):
        self._socket.close()



