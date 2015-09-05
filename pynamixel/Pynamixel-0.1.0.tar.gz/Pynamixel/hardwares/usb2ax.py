# coding: utf8

# Copyright 2015 Vincent Jacques <vincent@vincent-jacques.net>

import sys

import serial  # https://pypi.python.org/pypi/pyserial

# http://www.xevelabs.com/doku.php?id=product:usb2ax:usb2ax
# https://github.com/Xevel/usb2ax


class USB2AX(object):
    """
    @todoc
    """
    def __init__(self, port, baudrate):
        self.__port = serial.Serial(port=port, baudrate=baudrate, timeout=1, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)

    def send(self, data):
        assert isinstance(data, list) and all(isinstance(b, int) and 0 <= b <= 0xFF for b in data), data
        self.__port.write(data)

    def receive(self, count):
        if sys.hexversion >= 0x03000000:
            read = self.__port.read(count)
            assert isinstance(read, bytes), read
            return list(read)
        else:
            read = self.__port.read(count)
            assert isinstance(read, str), read
            return [ord(c) for c in read]
