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
from xwot.model import Sensor as XWOTSensor
from xwot.model import Device as XWOTDevice
from xwot.model import Model
from xwot.model import BaseModel


class LightBulb(XWOTDevice, BaseModel):

    __mutable_props__ = ['name', 'streetAddress', 'roomAddress', 'postalCode', 'addressLocality']
    __expose__ = __mutable_props__ + ['description', 'switch', 'sensor']

    def __init__(self, name, street_address, postal_code, address_locality, room_address):
        super(LightBulb, self).__init__()
        self._dic = {
            'name': name,
            'streetAddress': street_address,
            'postalCode': postal_code,
            'addressLocality': address_locality,
            'roomAddress': room_address
        }

        self.add_type('xwot-ext:LightBulb')
        self.add_link('switch')
        self.add_link('sensor')

    @property
    def resource_path(self):
        return '/lightbulb'

    @property
    def name(self):
        return self._dic['name']

    @property
    def description(self):
        return "Hi there my name is %s. I'm a light bulb and currently present in room %s at the location: %s, %s, %s" % \
               (self.name, self.roomAddress, self.streetAddress, self.addressLocality, self.postalCode)

    @property
    def switch(self):
        return '/lightbulb/switch'

    @property
    def sensor(self):
        return '/lightbulb/sensor'

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


from xwot.i2c.adapter import LightBulbAdapter


class Switch(XWOTContext, Model):

    __mutable_props__ = ['name', 'state']
    __expose__ = __mutable_props__ + ['description', 'lightbulb']

    def __init__(self, name, adapter=LightBulbAdapter()):
        super(Switch, self).__init__()

        self._dic = {
            'name': name
        }
        self._adapter = adapter
        self.add_type('xwot-ext:Switch')
        self.add_link('lightbulb')

    @property
    def resource_path(self):
        return '/lightbulb/switch'

    @property
    def description(self):
        return "A light switch to turn off or on."

    @property
    def lightbulb(self):
        return '/lightbulb'

    @property
    def state(self):
        return self._adapter.state

    @property
    def name(self):
        return self._dic['name']

    def handle_update(self, dic):
        if dic.get('state') == 'off':
            self._adapter.switch_off()

        if dic.get('state') == 'on':
            self._adapter.switch_on()

        self._dic['name'] = str(dic.get('name', self._dic['name']))

        return 200


class Sensor(XWOTSensor, Model):

    __expose__ = ['name', 'unit', 'measures', 'description', 'measurement', 'symbol', 'lightbulb']

    def __init__(self, adapter=LightBulbAdapter()):
        super(Sensor, self).__init__()
        self._adapter = adapter
        self.add_type('xwot-ext:IlluminanceSensor')
        self.add_link('lightbulb')

    @property
    def resource_path(self):
        return '/lightbulb/sensor'

    @property
    def name(self):
        return 'Illuminance sensor'

    @property
    def lightbulb(self):
        return '/lightbulb'

    @property
    def unit(self):
        return 'Lux'

    @property
    def description(self):
        return 'A sensor that measures the illuminance of this light bulb.'

    @property
    def measures(self):
        return 'Illuminance'

    @property
    def measurement(self):
        return self._adapter.illuminance

    @property
    def symbol(self):
        return 'lx'

    def handle_update(self, dic):
        pass
