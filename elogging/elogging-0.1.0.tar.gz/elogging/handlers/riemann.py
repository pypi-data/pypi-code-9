
import logging
import bernhard

from logging import Handler

from bernhard import Client
from bernhard import TransportError

TCPTransport = bernhard.TCPTransport
UDPTransport = bernhard.UDPTransport

bernhard.log.addHandler(logging.NullHandler())

class ConnectionError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

class RiemannHandler(Handler):
    def __init__(self, host='127.0.0.1', port=5555, transport=TCPTransport):
        Handler.__init__(self)
        self.client = Client(host, port, transport)
        try:
            conn = transport(host, port)
            conn.close()
        except TransportError:
            raise ConnectionError("Could not connect to Riemann server.")

    def emit(self, record):
        try:
            self.client.send(record.event)
        except TransportError:
            raise ConnectionError("Connection to Riemann server broken.")

