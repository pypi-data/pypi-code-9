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

import struct
import smbus


class Adapter(object):

    def __init__(self, bus=1, i2c_addr=0x04):
        self._bus = smbus.SMBus(bus)
        self._i2c_addr = i2c_addr

    @property
    def bus(self):
        return self._bus

    @property
    def i2c_addr(self):
        return self._i2c_addr

    def _to_int(self, data):
        """
        Assumes that data is in big endian format: [msb, ..., lsb]
        """
        b = ''.join(chr(i) for i in data)
        r = struct.unpack('>i', b)
        return r[0]

    def _to_uint(self, data):
        """
        Assumes that data is in big endian format: [msb, ..., lsb]
        """
        b = ''.join(chr(i) for i in data)
        r = struct.unpack('>I', b)
        return r[0]

    def _to_short(self, data):
        """
        Assumes that data is in big endian format: [msb, ..., lsb]
        """
        b = ''.join(chr(i) for i in data)
        r = struct.unpack('>h', b)
        return r[0]

    def _to_ushort(self, data):
        """
        Assumes that data is in big endian format: [msb, ..., lsb]
        """
        b = ''.join(chr(i) for i in data)
        r = struct.unpack('>H', b)
        return r[0]

    def _to_float(self, data):
        """
        Assumes that data is in big endian format: [msb, ..., lsb]
        """
        b = ''.join(chr(i) for i in data)
        r = struct.unpack('>f', b)
        return r[0]

    def _to_double(self, data):
        """
        Assumes that data is in big endian format: [msb, ..., lsb]
        """
        b = ''.join(chr(i) for i in data)
        r = struct.unpack('>d', b)
        return r[0]

    def write_byte(self, reg):
        try:
            self._bus.write_byte(self._i2c_addr, reg)
            return True
        except IOError:
            return False

    def write_word(self, reg, val):
        try:
            self._bus.write_word_data(self._i2c_addr, reg, val)
            return True
        except IOError:
            return False

    def read_byte(self, reg):
        try:
            return self._bus.read_byte_data(self._i2c_addr, reg)
        except IOError:
            return None

    def read_bytes(self, reg, byte_count):
        try:
            return self._bus.read_i2c_block_data(self._i2c_addr, reg, byte_count)
        except IOError:
            return None

    def read_int32(self, reg):
        data = self.read_bytes(reg, 4)
        if data is not None:
            return self._to_int(data)
        else:
            return None

    def read_uint32(self, reg):
        data = self.read_bytes(reg, 4)
        if data is not None:
            return self._to_uint(data)
        else:
            return None

    def read_int16(self, reg):
        data = self.read_bytes(reg, 2)
        if data is not None:
            return self._to_short(data)
        else:
            return None

    def read_uint16(self, reg):
        data = self.read_bytes(reg, 2)
        if data is not None:
            return self._to_ushort(data)
        else:
            return None

    def read_float(self, reg):
        data = self.read_bytes(reg, 4)
        if data is not None:
            return self._to_float(data)
        else:
            return None

    def read_double(self, reg):
        data = self.read_bytes(reg, 8)
        if data is not None:
            return self._to_double(data)
        else:
            return None