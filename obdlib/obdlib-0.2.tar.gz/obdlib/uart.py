DEFAULT_BAUDRATE = 38400
import sys

if (hasattr(sys, 'implementation') and
            sys.implementation.name == 'micropython'):
    # if using pyBoard
    from pyb import UART as uart_base
else:
    from serial import Serial as uart_base

from obdlib.logging import logger


class UART(object):
    def __init__(self):
        self.bus_name = uart_base.__name__
        self.bus = None
        self.map = {}

    def connection(self, port, baudrate=DEFAULT_BAUDRATE):
        try:
            self.bus = uart_base(port, baudrate)
            self._mapping()
        except Exception as err:
            # logging exception
            logger.error(err)
            return None

        return self

    def __getattr__(self, item):
        def args_wrapper(*args, **kwargs):
            try:
                response = getattr(self.bus, item)(*args, **kwargs)
            except AttributeError:
                response = self._invoke_mapping(item, *args, **kwargs)
            return response

        return args_wrapper

    def _invoke_mapping(self, method, *args, **kwargs):
        try:
            item = self.map[self.bus_name][method]
            return getattr(self.bus, item)(*args, **kwargs) if item else None
        except KeyError:
            raise Exception(
                "Unregistered method or attribute {}".format(method))

    def _mapping(self):
        self.map = {
            "UART": {
                "close": "deinit",
                "flushInput": "",
                "flushOutput": ""
            },
        }
