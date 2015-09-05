# coding: utf8

# Copyright 2015 Vincent Jacques <vincent@vincent-jacques.net>

from ..instructions import ReadData


class R8(object):
    def __init__(self, system, ident, address):
        self.__system = system
        self.__ident = ident
        self.__address = address

    def read(self):
        ident, error, response = self.__system.bus.send(self.__ident, ReadData(self.__address, 1))
        return response.data[0]


class RW8(object):
    def __init__(self, system, ident, address):
        self.__system = system
        self.__ident = ident
        self.__address = address

    def read(self):
        ident, error, response = self.__system.bus.send(self.__ident, ReadData(self.__address, 1))
        return response.data[0]

    def write(self, value):
        self.__system.bus.send(self.__ident, self.__system.instruction_for_writes(self.__address, [value]))


class R16(object):
    def __init__(self, system, ident, address):
        self.__system = system
        self.__ident = ident
        self.__address = address

    def read(self):
        ident, error, response = self.__system.bus.send(self.__ident, ReadData(self.__address, 2))
        return response.data[0] + 0x100 * response.data[1]


class RW16(object):
    def __init__(self, system, ident, address):
        self.__system = system
        self.__ident = ident
        self.__address = address

    def read(self):
        ident, error, response = self.__system.bus.send(self.__ident, ReadData(self.__address, 2))
        return response.data[0] + 0x100 * response.data[1]

    def write(self, value):
        self.__system.bus.send(self.__ident, self.__system.instruction_for_writes(self.__address, [value % 0x100, value // 0x100]))
