# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 GNS3 Technologies Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Interface for Auto UDP NIOs.
"""

import asyncio
from .nio import NIO

import logging
log = logging.getLogger(__name__)


class NIOUDPAuto(NIO):
    """
    Dynamips auto UDP NIO.

    :param hypervisor: Dynamips hypervisor instance
    :param lhost: local host/address
    :param lport_start: start local port range
    :param lport_end: end local port range
    """

    _instance_count = 0

    def __init__(self, hypervisor, lhost, lport_start, lport_end):

        NIO.__init__(self, hypervisor)

        # create an unique ID
        self._id = NIOUDPAuto._instance_count
        NIOUDPAuto._instance_count += 1
        name = 'nio_udp_auto' + str(self._id)
        self._lhost = lhost
        self._lport_start = lport_start
        self._lport_end = lport_end
        self._lport = None
        self._rhost = None
        self._rport = None
        super().__init__(name, hypervisor)

    @classmethod
    def reset(cls):
        """
        Reset the instance count.
        """

        cls._instance_count = 0

    @asyncio.coroutine
    def create(self):

        lport = yield from self._hypervisor.send("nio create_udp_auto {name} {lhost} {lport_start} {lport_end}".format(name=self._name,
                                                                                                                       lhost=self._lhost,
                                                                                                                       lport_start=self._lport_start,
                                                                                                                       lport_end=self._lport_end))
        self._lport = int(lport[0])
        log.info("NIO UDP AUTO {name} created with lhost={lhost}, lport_start={start}, lport_end={end}".format(name=self._name,
                                                                                                               lhost=self._lhost,
                                                                                                               start=self._lport_start,
                                                                                                               end=self._lport_end))

    @property
    def lhost(self):
        """
        Returns the local host/address

        :returns: local host/address
        """

        return self._lhost

    @property
    def lport(self):
        """
        Returns the local port

        :returns: local port number
        """

        return self._lport

    @property
    def rhost(self):
        """
        Returns the remote host/address

        :returns: remote host/address
        """

        return self._rhost

    @property
    def rport(self):
        """
        Returns the remote port

        :returns: remote port number
        """

        return self._rport

    @asyncio.coroutine
    def connect(self, rhost, rport):
        """
        Connects this NIO to a remote socket

        :param rhost: remote host/address
        :param rport: remote port number
        """

        yield from self._hypervisor.send("nio connect_udp_auto {name} {rhost} {rport}".format(name=self._name,
                                                                                              rhost=rhost,
                                                                                              rport=rport))
        self._rhost = rhost
        self._rport = rport

        log.info("NIO UDP AUTO {name} connected to {rhost}:{rport}".format(name=self._name, rhost=rhost,  rport=rport))

    def __json__(self):

        return {"type": "auto_nio_udp",
                "lport_start": self._lport_start,
                "lport_end": self._lport_end,
                "lhost": self._lhost,
                "lport": self._lport,
                "rhost": self._rhost,
                "rport": self._rport}
