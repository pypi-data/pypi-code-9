# encoding=utf-8

import socket

from loggers import logger
from tornado import gen
from tornado.tcpclient import TCPClient


class TLVCommunicator(object):

    type_len = 1
    length_len = 1
    big_endian_byte_order = True

    data_decoders = {}  # command bytes -> unbound method

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.stream = None

    @gen.coroutine
    def connect(self):
        self.stream = yield TCPClient().connect(
            self.host, self.port,
            af=socket.AF_INET,
        )
        logger.info("Connected to {}:{}".format(
            self.host, self.port
        ))

    def disconnect(self):
        if not self.stream:
            return

        self.stream.close()
        self.stream = None
        logger.info("Disconnected from {}:{}".format(
            self.host, self.port
        ))

    @gen.coroutine
    def get_command(self):

        command = yield self.read_partial(self.type_len)
        value = yield self.read_value()

        decoder = self.data_decoders.get(command)
        if decoder:
            command, value = decoder(self, command, value)

        raise gen.Return([command, value])

    @gen.coroutine
    def read_value(self):
        ret = None

        if self.length_len:
            length_bytes = yield self.read_partial(self.length_len)
            value_length = self.from_bytes(length_bytes)

            if value_length:
                ret = yield self.read_partial(value_length)

        raise gen.Return(ret)

    def from_bytes(self, bytes):
        if self.big_endian_byte_order:
            bytes = bytes[::-1]

        ret = 0
        base = 1
        for byte in bytes:
            ret += ord(byte) * base
            base *= 10 ** 8

        return ret

    def read_partial(self, num_bytes):
        return self.stream.read_bytes(num_bytes, partial=True)
