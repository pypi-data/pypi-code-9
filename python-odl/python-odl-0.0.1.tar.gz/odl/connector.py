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

class ODLConnector(object):
    """
    This class represents a connector (switch port) in OpenDayLight.
    """
    def __init__(self, connector, node):
        self.connector = connector
        self.node = node

    def __repr__(self):
        return "<ODLConnector: %s>" % self.id

    def to_dict(self):
        base = {self.id: {
                'status': self.status,
                'port_number': self.port_number,
                'hardware_address': self.hardware_address,
                'name': self.name}}

        return base

    @property
    def id(self):
        return self.connector['id']

    @property
    def status(self):
        try:
            return self.connector['stp-status-aware-node-connector:status']
        except KeyError:
            return None

    @property
    def port_number(self):
        return self.connector['flow-node-inventory:port-number']

    @property
    def hardware_address(self):
        return self.connector['flow-node-inventory:hardware-address']

    @property
    def name(self):
        return self.connector['flow-node-inventory:name']
