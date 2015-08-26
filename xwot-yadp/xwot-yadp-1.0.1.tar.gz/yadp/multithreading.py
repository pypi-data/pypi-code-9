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
import threading
import time
import socket

from .core import BaseService
from .core import BaseClient
from .core import constant, unicast, multicast


logger = logging.getLogger('multithreading')


class MulticastReceiveListener(threading.Thread):
    """
    Listener for multicast messages.
    """

    def __init__(self, dispatcher, multicast_receiver):
        super(MulticastReceiveListener, self).__init__()
        self.daemon = True
        self._dispatcher = dispatcher
        self._STOP = threading.Event()
        self._multicast_receiver = multicast_receiver

    def run(self):
        while not self.stopped():
            try:
                data, addr = self._multicast_receiver.receive()
                # dispatch received multicast message
                self._dispatcher(data, addr)

            except:  # TODO: catch correct exception
                pass

    def terminate(self):
        logger.debug("multicast listener - terminate!")
        self._STOP.set()
        self._multicast_receiver.close()

    def stopped(self):
        return self._STOP.isSet()


class UnicastReceiveListener(threading.Thread):
    """
    Listener for unicast messages
    """

    def __init__(self, dispatcher, unicast_receiver):
        super(UnicastReceiveListener, self).__init__()
        self.daemon = True
        self._dispatcher = dispatcher
        self._STOP = threading.Event()
        self._unicast_receiver = unicast_receiver

    def run(self):
        while not self.stopped():
            try:
                data, addr = self._unicast_receiver.receive()
                # dispatch received unicast message
                self._dispatcher(data, addr)

            except socket.timeout:
                pass

    def terminate(self):
        logger.debug("unicast listener - terminate!")
        self._STOP.set()
        self._unicast_receiver.close()

    def stopped(self):
        return self._STOP.isSet()


class MainListener(threading.Thread):
    """
    The core implements the protocol core logic.
    """

    LOG_INTERVAL = 10
    LAST_LOG = time.time()

    def __init__(self, tasks, listeners):
        super(MainListener, self).__init__()
        self._tasks = tasks
        self._STOP = threading.Event()
        self._listeners = listeners
        self.daemon = True

    def terminate(self):
        [listener.terminate() for listener in self._listeners]
        logger.debug("core - terminate!")
        self._STOP.set()

    def stopped(self):
        return self._STOP.isSet()

    def run(self):
        logger.debug("run core!")
        [listener.start() for listener in self._listeners]

        while not self.stopped():
            self._debug()
            [task() for task in self._tasks]

    def _debug(self):
        current_time = time.time()
        if current_time - self.LAST_LOG > 10:
            logger.debug("core - still running!")
            self.LAST_LOG = time.time()


class Service(BaseService):

    def __init__(self):
        super(Service, self).__init__(m_sender=multicast.UDPSender(), u_sender=unicast.TCPSender())
        m_receiver = multicast.UDPReceiver()
        m_receive_listener = MulticastReceiveListener(self.dispatch, m_receiver)
        self._core = MainListener(tasks=[self._send_announcements], listeners=[m_receive_listener])

    def run(self, run_reactor=True):
        self._core.start()

    def _hook_shutdown(self):
        self._core.terminate()


class Client(BaseClient):

    def __init__(self, port=constant.UNICAST_PORT):
        super(Client, self).__init__(port, multicast.UDPSender())
        m_receiver = multicast.UDPReceiver()
        u_receiver = unicast.TCPReceiver()
        m_receive_listener = MulticastReceiveListener(self.dispatch, m_receiver)
        u_receive_listener = UnicastReceiveListener(self.dispatch, u_receiver)
        self._core = MainListener(tasks=[self._cleanup], listeners=[m_receive_listener, u_receive_listener])

    def run(self, run_reactor=True):
        self._core.start()

    def _hook_shutdown(self):
        logger.debug("shutdown client")
        self._core.terminate()