# encoding=utf-8

import sys
from loggers import logger
from tornado import gen

from painter import Painter
from communicator import TLVCommunicator


class LampCommunicator(TLVCommunicator):

    type_len = 1
    length_len = 2
    big_endian_byte_order = True

    def _decode_on(self, command, value):
        return 'on', None

    def _decode_off(self, command, value):
        return 'off', None

    def _decode_color(self, command, value):
        return 'color', map(self.from_bytes, value[::-1])

    data_decoders = {
        '\x12': _decode_on,
        '\x13': _decode_off,
        '\x20': _decode_color,
    }


def enum(*values):
    class Enum(object):
        pass

    for i, val in enumerate(values):
        setattr(Enum, val, i)

    return Enum


class Lamp(object):

    communicator_type = LampCommunicator
    painter_type = Painter

    States = enum('ON', 'OFF')

    def __init__(self, host, port):
        self.painter = self.create_painter()
        self.communicator = self.communicator_type(
            host, port,
        )
        self.state = self.States.OFF

    def create_painter(self):
        try:
            return self.painter_type()
        except Exception as e:
            error = (
                'Sorry! Cannot initialize painting mechanism. '
                '{}'
            ).format(e.message)
            sys.stderr.write(error)
            exit()

    @gen.coroutine
    def start(self):
        try:
            yield self.do_start()
        except Exception as e:
            logger.exception(e.message)
            raise

    @gen.coroutine
    def do_start(self):
        yield self.communicator.connect()

        self._running = True
        while self._running:
            yield self.execute_command()

    def finish(self):
        self.communicator.disconnect()
        self.painter.destroy()

    @gen.coroutine
    def execute_command(self):

        command, value = yield self.communicator.get_command()
        logger.info('Got command: {}, {}'.format(
            command, value,
        ))
        handler = self.command_to_handler(command)
        if not handler:
            logger.warning('Got unknown command: {}'.format(
                command
            ))
            return

        handler(value)

    def command_to_handler(self, command):
        return getattr(
            self, 'cmd_{}'.format(command.lower()), None
        )

    def cmd_on(self, value=None):
        if self.state == self.States.OFF:
            self.state = self.States.ON
            self.painter.on()

    def cmd_off(self, value=None):
        self.state = self.States.OFF
        self.painter.off()

    def cmd_color(self, rgb):
        if self.state == self.States.ON:
            self.painter.color(rgb)
