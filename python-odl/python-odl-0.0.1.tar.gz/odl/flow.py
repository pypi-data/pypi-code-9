#!/usr/bin/env python
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
#
# Authors:
#          - Beraldo Leal <beraldo AT ncc DOT unesp DOT br>
#
# -*- coding: utf-8 -*-
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

from odl.exceptions import ODL404, FlowNotFound

class ODLFlow(object):
    """
    This class represents a switch table in OpenDayLight.
    """
    def __init__(self, xml, table):
        self.xml = xml
        self.table = table

    def __repr__(self):
        return "<ODLFlow: %s>" % self.id

    @property
    def id(self):
        return self.xml['id']

    @property
    def priority(self):
        return self.xml['priority']

    @property
    def idle_timeout(self):
        return self.xml['idle-timeout']

    @property
    def hard_timeout(self):
        return self.xml['hard-timeout']

    @property
    def cookie(self):
        return self.xml['cookie']

    def _get_flow_stats(self):
        """
        Return a dict with the flow statics when exists, if not return a empty
        dict.
        """
        try:
            return self.xml['opendaylight-flow-statistics:flow-statistics']
        except KeyError:
            return {}

    def to_dict(self):
        base = {self.id: {'priority': self.priority,
                          'idle_timeout': self.idle_timeout,
                          'hard_timeout': self.hard_timeout,
                          'cookie': self.cookie,
                          'stats': {'bytes': self.get_byte_count(),
                                    'packets': self.get_packet_count()}}}
        return base

    def get_byte_count(self):
        """
        Return the number of bytes that matches with this flow.
        """
        stats = self._get_flow_stats()
        try:
            return stats['byte-count']
        except KeyError:
            return None

    def get_packet_count(self):
        """
        Return the number of packets that matches with this flow.
        """
        stats = self._get_flow_stats()
        try:
            return stats['packet-count']
        except KeyError:
            return None

    def delete(self):
        """
        Delete a flow from config endpoint. We cannot delete flows in
        operational endpoint only.
        """
        odl_instance = self.table.node.odl_instance
        endpoint = self.table.config_endpoint + 'flow/' + self.id

        try:
            odl_instance.delete(endpoint)
        except ODL404:
            raise FlowNotFound("Flow id %s not found" % self.id)
