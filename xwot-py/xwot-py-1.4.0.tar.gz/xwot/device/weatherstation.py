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
from xwot.model import Device as XWOTDevice
from xwot.model import Sensor as XWOTSensor
from xwot.model import Collection
from xwot.model import CollectionMember

__all__ = ['WeatherStation', 'GPSWeatherStation', 'SensorCollection', 'GPS']


class WeatherStation(XWOTDevice, BaseModel):
    __mutable_props__ = ['name', 'streetAddress', 'roomAddress', 'postalCode', 'addressLocality']
    __expose__ = __mutable_props__ + ['description', 'sensors']

    def __init__(self, name, street_address, postal_code, address_locality, room_address):
        super(WeatherStation, self).__init__()
        self._dic = {
            'name': name,
            'streetAddress': street_address,
            'postalCode': postal_code,
            'addressLocality': address_locality,
            'roomAddress': room_address
        }

        self.add_type('xwot-ext:WeatherStation')
        self.add_link('sensors')

    @property
    def resource_path(self):
        return '/weatherstation'

    @property
    def name(self):
        return self._dic['name']

    @property
    def description(self):
        return "Hi there my name is %s. I'm a weather station and currently present in room %s at the location: %s, %s, %s" % \
               (self.name, self.roomAddress, self.streetAddress, self.addressLocality, self.postalCode)

    @property
    def sensors(self):
        return '/weatherstation/sensors'

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

    @streetAddress.setter
    def streetAddress(self, v):
        self._dic['streetAddress'] = v

    @postalCode.setter
    def postalCode(self, v):
        self._dic['postalCode'] = v

    @addressLocality.setter
    def addressLocality(self, v):
        self._dic['addressLocality'] = v

    @roomAddress.setter
    def roomAddress(self, v):
        self._dic['roomAddress'] = v

    @property
    def sensors(self):
        return '/weatherstation/sensors'


class GPSWeatherStation(WeatherStation):

    __mutable_props__ = ['name', 'roomAddress']
    __expose__ = __mutable_props__ + ['description', 'sensors', 'gps', 'streetAddress', 'roomAddress', 'postalCode',
                                      'addressLocality']

    def __init__(self, name='GPS Weather Station', room_address='Unknown'):
        super(GPSWeatherStation, self).__init__(name=name, room_address=room_address, street_address='',
                                                postal_code='', address_locality='')
        self.add_link('gps')

    @property
    def gps(self):
        return '/weatherstation/gps'


class Sensor(XWOTSensor, CollectionMember, Model):
    __expose__ = ['name', 'unit', 'measures', 'description', 'measurement', 'symbol', 'waterdispenser',
                  'back_link1', 'back_link2']

    def __init__(self, name, unit, symbol, description, measures, type_iri, adapter, adapter_measurement_fun, id):
        super(Sensor, self).__init__()
        self._name = name
        self._id = id
        self._unit = unit
        self._symbol = symbol
        self._description = description
        self._measures = measures
        self._adapter = adapter
        self.add_type(type_iri)
        self._adapter_measurement_fun = adapter_measurement_fun
        self.add_link('back_link1')
        self.add_link('back_link2')

    @property
    def resource_path(self):
        return "/weatherstation/sensors/%s" % self._id

    @property
    def id(self):
        return self._id

    @property
    def back_link1(self):
        return '/weatherstation/sensors'

    @property
    def back_link2(self):
        return '/weatherstation'

    @property
    def name(self):
        return self._name

    @property
    def unit(self):
        return self._unit

    @property
    def symbol(self):
        return self._symbol

    @property
    def description(self):
        return self._description

    @property
    def measures(self):
        return self._measures

    @property
    def measurement(self):
        val = self._adapter_measurement_fun(self._adapter)
        if val is not None:
            return round(val, 2)
        else:
            return val

    def handle_update(self, dic):
        pass


from xwot.i2c.adapter import WeatherstationAdapter


def create_sensors():
    adapter = WeatherstationAdapter()

    _sensors = {
        'temperature_1': Sensor(id='temperature1', name='Temperature sensor 1', unit='Celsius', symbol='°C',
                                measures='Temperature',
                                description='A temperature sensor of this weather station.',
                                adapter=adapter, adapter_measurement_fun=lambda a: a.temperature_1,
                                type_iri='xwot-ext:TemperatureSensor'),

        'temperature_2': Sensor(id='temperature2', name='Temperature sensor 2', unit='Celsius', symbol='°C',
                                measures='Temperature',
                                description='A temperature sensor of this weather station.',
                                adapter=adapter, adapter_measurement_fun=lambda a: a.temperature_2,
                                type_iri='xwot-ext:TemperatureSensor'),

        'pressure': Sensor(id='pressure', name='Pressure sensor', unit='Pascal', symbol='pa', measures='Pressure',
                           description='A pressure sensor of this weather station.',
                           adapter=adapter, adapter_measurement_fun=lambda a: a.pressure,
                           type_iri='xwot-ext:PressureSensor'),

        'humidity': Sensor(id='humidity', name='Humidity sensor', unit='Percentage', symbol='%',
                           measures='Humidity',
                           description='A humidity sensor of this weather station.',
                           adapter=adapter, adapter_measurement_fun=lambda a: a.humidity,
                           type_iri='xwot-ext:HumiditySensor'),

        'altitude': Sensor(id='altitude', name='Altitude sensor', unit='Meters', symbol='m', measures='Altitude',
                           description='An altitude sensor of this weather station.',
                           adapter=adapter, adapter_measurement_fun=lambda a: a.altitude,
                           type_iri='xwot-ext:AltitudeSensor'),

        'illuminance': Sensor(id='illuminance', name='Illuminance sensor', unit='Lux', symbol='lx',
                              measures='Illuminance',
                              description='An illuminance sensor of this weather station.',
                              adapter=adapter, adapter_measurement_fun=lambda a: a.illuminance,
                              type_iri='xwot-ext:IlluminanceSensor'),

        'color': Sensor(id='color', name='Color sensor', unit='Kelvin', symbol='k', measures='Temperature',
                        description='A color sensor of this weather station.',
                        adapter=adapter, adapter_measurement_fun=lambda a: a.color_temperature,
                        type_iri='xwot-ext:ColorSensor')
    }

    return _sensors


class SensorCollection(Collection, Model):

    __expose__ = ['back_link']

    def __init__(self, sensors):
        super(SensorCollection, self).__init__()
        self._sensors = sensors
        self.add_link('back_link')

    @property
    def resource_path(self):
        return '/weatherstation/sensors'

    @property
    def members(self):
        return self._sensors

    @property
    def back_link(self):
        return '/weatherstation'

    def handle_update(self, dic):
        pass


from xwot.i2c.adapter import GPSAdapter


class GPS(XWOTDevice, Model):

    __expose__ = ['name', 'description', 'state', 'latitude', 'longitude', 'elevation', 'back_link']

    def __init__(self):
        super(GPS, self).__init__()
        self._adapter = GPSAdapter()
        self.add_type('schema:GeoCoordinates')
        self.add_link('back_link')

    @property
    def resource_path(self):
        return '/weatherstation/gps'

    @property
    def state(self):
        if self._adapter.found:
            return 'found'
        else:
            return 'lost'

    @property
    def found(self):
        return self._adapter.found

    @property
    def latitude(self):
        return self._adapter.latitude

    @property
    def longitude(self):
        return self._adapter.longitude

    @property
    def elevation(self):
        return self._adapter.elevation

    @property
    def back_link(self):
        return '/weatherstation'

    @property
    def description(self):
        return "A GPS navigation device is a device that accurately calculates geographical location " \
               "by receiving information from GPS satellites."

    @property
    def name(self):
        return 'GPS device'

    def handle_update(self, dic):
        pass
