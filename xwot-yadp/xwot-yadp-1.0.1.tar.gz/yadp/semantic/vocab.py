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


__author__ = 'Alexander Rüedlinger'
__all__ = ['XWOT', 'SchemaOrg']


from rdflib import URIRef


class SchemaOrg(object):

    KNOWS = URIRef('http://schema.org/knows')
    NAME = URIRef('http://schema.org/name')
    DESCRIPTION = URIRef('http://schema.org/description')
    URL = URIRef('http://schema.org/url')
    ADDITIONAL_TYPE = URIRef('http://schema.org/additionalType')
    SAME_AS = URIRef('http://schema.org/sameAs')

    STREET_ADDRESS = URIRef('http://schema.org/streetAddress')
    ADDRESS_LOCALITY = URIRef('http://schema.org/addressLocality')
    POSTAL_CODE = URIRef('http://schema.org/postalCode')


class XWOT(object):

    RESOURCE = URIRef('http://xwot.lexruee.ch/vocab/core#Resource')
    DESCRIPTION = URIRef('http://xwot.lexruee.ch/vocab/core#Description')
    DEVICE = URIRef('http://xwot.lexruee.ch/vocab/core#Device')
    CONTEXT = URIRef('http://xwot.lexruee.ch/vocab/core#Context')
    SERVICE = URIRef('http://xwot.lexruee.ch/vocab/core#Service')
    SENSOR = URIRef('http://xwot.lexruee.ch/vocab/core#Sensor')
    ACTUATOR = URIRef('http://xwot.lexruee.ch/vocab/core#Actuator')
    TAG = URIRef('http://xwot.lexruee.ch/vocab/core#Tag')
    PUBLISHER = URIRef('http://xwot.lexruee.ch/vocab/core#Publisher')

    TEMPERATURE_SENSOR = URIRef('http://xwot.lexruee.ch/vocab/core-ext#TemperatureSensor')
    HUMIDITY_SENSOR = URIRef('http://xwot.lexruee.ch/vocab/core-ext#HumiditySensor')
    PRESSURE_SENSOR = URIRef('http://xwot.lexruee.ch/vocab/core-ext#PressureSensor')
    ALTITUDE_SENSOR = URIRef('http://xwot.lexruee.ch/vocab/core-ext#AltitudeSensor')
    ILLUMINANCE_SENSOR = URIRef('http://xwot.lexruee.ch/vocab/core-ext#IlluminanceSensor')
    SOIL_MOISTURE_SENSOR = URIRef('http://xwot.lexruee.ch/vocab/core-ext#SoilMoistureSensor')
    MAGNETIC_SENSOR = URIRef('http://xwot.lexruee.ch/vocab/core-ext#MagneticSensor')

    LIGHTBULB = URIRef('http://xwot.lexruee.ch/vocab/core-ext#LightBulb')
    WEATHERSTATION = URIRef('http://xwot.lexruee.ch/vocab/core-ext#WeatherStation')
    DOOR = URIRef('http://xwot.lexruee.ch/vocab/core-ext#Door')
    WINDOW = URIRef('http://xwot.lexruee.ch/vocab/core-ext#Window')
    WATERDISPENSER = URIRef('http://xwot.lexruee.ch/vocab/core-ext#WaterDispenser')
    VALVE = URIRef('http://xwot.lexruee.ch/vocab/core-ext#Valve')
    HANDLE = URIRef('http://xwot.lexruee.ch/vocab/core-ext#Handle')
    LOCK = URIRef('http://xwot.lexruee.ch/vocab/core-ext#Lock')
    SERVO = URIRef('http://xwot.lexruee.ch/vocab/core-ext#Servo')
    MOTOR = URIRef('http://xwot.lexruee.ch/vocab/core-ext#Motor')

    MEASURES = URIRef('http://xwot.lexruee.ch/vocab/core-ext#measures')
    UNIT = URIRef('http://xwot.lexruee.ch/vocab/core-ext#unit')
    SYMBOL = URIRef('http://xwot.lexruee.ch/vocab/core-ext#symbol')
    MEASUREMENT = URIRef('http://xwot.lexruee.ch/vocab/core-ext#measurement')
    STATE = URIRef('http://xwot.lexruee.ch/vocab/core-ext#state')

    ROOM_ADDRESS = URIRef('http://xwot.lexruee.ch/vocab/core-ext#roomAddress')