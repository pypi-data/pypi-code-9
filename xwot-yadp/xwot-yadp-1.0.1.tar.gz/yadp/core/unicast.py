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
import logging

from . import Receiver, constant
from . import Sender


logger = logging.getLogger('unicast')


class UDPReceiver(Receiver):
    """
    UDP implementation of a simple receiver (server),
    """

    def __init__(self):
        logger.debug("create udp unicast receiver")
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.bind((constant.BIND_ADDR, constant.UNICAST_PORT))

    def receive(self):
        return self._socket.recvfrom(constant.RECEIVE_MAX_BYTES)

    def close(self):
        self._socket.close()


class UDPSender(Sender):
    """
    UDP implementation of a simple sender (client),
    """

    def __init__(self):
        logger.debug("create udp unicast sender")

    def send(self, message, ip, port):
        _socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        _socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        _socket.sendto(message, (ip, port))
        _socket.close()

    def close(self):
        pass


class TCPReceiver(Receiver):
    """
    TCP implementation of a simple receiver (server),
    """

    def __init__(self):
        logger.debug("create tcp unicast receiver")
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.bind((constant.BIND_ADDR, constant.UNICAST_PORT))
        self._socket.listen(5)

    def receive(self):
        client_socket, addr, = self._socket.accept()
        data = client_socket.recv(constant.RECEIVE_MAX_BYTES)
        return data, addr

    def close(self):
        self._socket.close()


class TCPSender(Sender):
    """
    TCP implementation of a simple sender (client),
    """

    def __init__(self):
        logger.debug("create tcp unicast sender")

    def send(self, message, ip, port):
        _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        _socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            _socket.connect((ip, port))
            _socket.send(message)
        except:
            logger.warn("TCP Sender error!")
        finally:
            _socket.close()

    def close(self):
        pass