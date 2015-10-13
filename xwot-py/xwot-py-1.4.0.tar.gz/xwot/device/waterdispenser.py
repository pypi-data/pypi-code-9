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

from xwot.model import Model
from xwot.model import BaseModel
from xwot.model import Sensor as XWOTSensor
from xwot.model import Context as XWOTContext
from xwot.model import Device as XWOTDevice


class WaterDispenser(XWOTDevice, BaseModel):

    __mutable_props__ = ['name', 'streetAddress', 'roomAddress', 'postalCode', 'addressLocality']
    __expose__ = __mutable_props__ + ['description', 'valve', 'sensor']

    def __init__(self, name, street_address, postal_code, address_locality, room_address):
        super(WaterDispenser, self).__init__()
        self._dic = {
            'name': name,
            'streetAddress': street_address,
            'postalCode': postal_code,
            'addressLocality': address_locality,
            'roomAddress': room_address
        }

        self.add_type('xwot-ext:WaterDispenser')
        self.add_link('valve')
        self.add_link('sensor')

    @property
    def resource_path(self):
        return '/waterdispenser'

    @property
    def name(self):
        return self._dic['name']

    @property
    def description(self):
        return "Hi there my name is %s. I'm a water dispenser and currently present in room %s at the location: %s, %s, %s" % \
               (self.name, self.roomAddress, self.streetAddress, self.addressLocality, self.postalCode)
    @property
    def valve(self):
        return '/waterdispenser/valve'

    @property
    def sensor(self):
        return '/waterdispenser/sensor'

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


from xwot.i2c.adapter import WaterDispenserAdapter


class Valve(XWOTContext, Model):

    __mutable_props__ = ['name', 'state']
    __expose__ = __mutable_props__ + ['description', 'waterdispenser']

    def __init__(self, name, adapter=WaterDispenserAdapter()):
        super(Valve, self).__init__()

        self._dic = {
            'name': name
        }
        self._adapter = adapter
        self.add_type('xwot-ext:Valve')
        self.add_link('waterdispenser')

    @property
    def resource_path(self):
        return '/waterdispenser/valve'

    @property
    def waterdispenser(self):
        return '/waterdispenser'

    @property
    def description(self):
        return "A valve that can be opened or closed. It controls the water supply of this water dispenser."

    @property
    def state(self):
        return self._adapter.solenoid_valve_state

    @property
    def name(self):
        return self._dic['name']

    def handle_update(self, dic):
        if dic.get('state') == 'closed':
            self._adapter.close_solenoid_valve()

        if dic.get('state') == 'opened':
            self._adapter.open_solenoid_valve()

        self._dic['name'] = str(dic.get('name', self._dic['name']))

        return 200


class Sensor(XWOTSensor, Model):

    __expose__ = ['name', 'unit', 'measures', 'description', 'measurement', 'symbol', 'waterdispenser']

    def __init__(self, adapter=WaterDispenserAdapter()):
        super(Sensor, self).__init__()
        self._adapter = adapter
        self.add_type('xwot-ext:SoilMoistureSensor')
        self.add_link('waterdispenser')

    @property
    def resource_path(self):
        return '/waterdispenser/sensor'

    @property
    def waterdispenser(self):
        return '/waterdispenser'

    @property
    def name(self):
        return 'Soil moisture Sensor'

    @property
    def unit(self):
        return 'Percentage'

    @property
    def symbol(self):
        return '%'

    @property
    def description(self):
        return 'A sensor that measures the soil moisture.'

    @property
    def measures(self):
        return 'Soil moisture'

    @property
    def measurement(self):
        val = self._adapter.soil_moisture
        return round(val, 2)

    def handle_update(self, dic):
        pass