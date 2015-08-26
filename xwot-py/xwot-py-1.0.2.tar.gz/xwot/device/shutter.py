#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# xwot.py - Python tools for the extended Web of Things
# Copyright (C) 2015  Alexander Rüedlinger
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>

__author__ = 'Alexander Rüedlinger'

from xwot.model import Context as XWOTContext
from xwot.model import Device as XWOTDevice
from xwot.model import Model
from xwot.model import BaseModel

from xwot.i2c.adapter import WindowAdapter
from xwot.i2c.adapter import ShutterAdapter
from xwot.device.window import Handle as WindowHandle


class Window(XWOTDevice, BaseModel):

    __mutable_props__ = ['name', 'streetAddress', 'roomAddress', 'postalCode', 'addressLocality']
    __expose__ = __mutable_props__ + ['description', 'handle', 'shutter']

    def __init__(self, name, street_address, postal_code, address_locality, room_address):
        super(Window, self).__init__()
        self._dic = {
            'name': name,
            'streetAddress': street_address,
            'postalCode': postal_code,
            'addressLocality': address_locality,
            'roomAddress': room_address
        }

        self.add_type('xwot-ext:Window')
        self.add_link('handle')
        self.add_link('shutter')

    @property
    def resource_path(self):
        return '/window'

    @property
    def name(self):
        return self._dic['name']

    @property
    def description(self):
        return "Hi there my name is %s. I'm a window and currently present in room %s at the location: %s, %s, %s" % \
               (self.name, self.roomAddress, self.streetAddress, self.addressLocality, self.postalCode)

    @property
    def handle(self):
        return '/window/handle'

    @property
    def shutter(self):
        return '/window/shutter'

    @property
    def streetAddress(self):
        return self._dic['streetAddress']

    @property
    def postalCode(self):
        return self._dic['postalCode']

    @property
    def addressLocality(self):
        return self._dic['addressLocality']

    @property
    def roomAddress(self):
        return self._dic['roomAddress']


class Handle(WindowHandle):

    def __init__(self, name, adapter=WindowAdapter()):
        super(Handle, self).__init__(name=name, adapter=adapter)


class Shutter(XWOTContext, Model):
    __mutable_props__ = ['name', 'state']
    __expose__ = __mutable_props__ + ['description', 'window']

    def __init__(self, name, adapter=ShutterAdapter()):
        super(Shutter, self).__init__()

        self._dic = {
            'name': name
        }
        self._adapter = adapter
        self.add_type('xwot-ext:Shutter')
        self.add_link('window')

    @property
    def resource_path(self):
        return '/window/shutter'

    @property
    def window(self):
        return '/window'

    @property
    def description(self):
        return "A shutter window which can be moved up and moved down."

    @property
    def state(self):
        return self._adapter.state

    @property
    def name(self):
        return self._dic['name']

    def handle_update(self, dic):
        if dic.get('state') == 'down':
            self._adapter.down()

        if dic.get('state') == 'up':
            self._adapter.up()

        self._dic['name'] = str(dic.get('name', self._dic['name']))

        return 200