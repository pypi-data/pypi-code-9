import json
import logging
import socket

from select import select
from zymbit.connector import get_connector
from zymbit.envelope import parse_buf
from zymbit.exceptions import NotConnected

BUFSIZE = 4096


class BaseServer(object):
    def __init__(self, host, port, message_handler=None):
        self.addr = (host, port)

        self._tcp_sock = None
        self._udp_sock = None

        self.connections = {}

        self.message_handler = message_handler

        self._run = True

    @property
    def logger(self):
        logger_name = '{}.{}'.format(__name__, self.__class__.__name__)
        return logging.getLogger(logger_name)

    @property
    def tcp_sock(self):
        if self._tcp_sock:
            return self._tcp_sock

        try:
            self._tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            self._tcp_sock.setblocking(0)
            self._tcp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self._tcp_sock.bind(self.addr)
            self._tcp_sock.listen(128)  # max 128 clients
        except socket.error:
            self.logger.warning('Unable to bind TCP socket at addr={}'.format(self.addr))
        else:
            self.logger.info("Listening on TCP addr={}".format(self.addr))

        return self._tcp_sock

    @property
    def udp_sock(self):
        if self._udp_sock:
            return self._udp_sock

        try:
            self._udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            self._udp_sock.setblocking(0)
            self._udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self._udp_sock.bind(self.addr)
        except socket.error:
            self.logger.warning('Unable to bind UDP socket at addr={}'.format(self.addr))
        else:
            self.logger.info("Listening on UDP addr={}".format(self.addr))

        return self._udp_sock

    def close_tcp(self):
        self._tcp_sock = None

    def close_udp(self):
        self._udp_sock = None

    def connect(self, info):
        conn, addr = info
        self.logger.info('%s, %s connected' % (conn, addr))

        self.connections[conn] = addr

    def disconnect(self, connection):
        addr = self.connections.pop(connection)
        self.logger.info('%s, %s disconnected' % (connection, addr))

    def fileno(self):
        return self.tcp_sock.fileno()

    def handle_message(self, client, buf):
        self.logger.info('client={}, buf={}'.format(client, buf))

    def loop(self, select_timeout=1.0):
        handled = None

        # check UDP
        try:
            buf, client = self.udp_sock.recvfrom(1024)
        except socket.error, exc:
            # (11, 'Resource temporarily unavailable')
            # [Errno 35] Resource temporarily unavailable
            error_number = exc[0]
            if error_number not in (11, 35):
                self.logger.exception(exc)
                self.logger.warning('got socket error_number={}'.format(error_number))

                self.close_udp()
        else:
            if buf:
                self.handle_message(client, buf)
                handled = True

        try:
            self.connect(self.tcp_sock.accept())
        except socket.error, exc:
            # (11, 'Resource temporarily unavailable')
            # [Errno 35] Resource temporarily unavailable
            error_number = exc[0]
            if error_number not in (11, 35):
                self.logger.exception(exc)
                self.logger.warning('got socket error_number={}'.format(error_number))

                self.close_tcp()

        ready, _, _ = select(self.connections, [], [], select_timeout)

        for client in ready:
            try:
                buf = client.recv(BUFSIZE)
                if buf == '':
                    self.disconnect(client)
                    continue
            except socket.error, exc:
                # [Errno 54] Connection reset by peer
                # [Errno 104] Connection reset by peer -- raspbian
                error_number = exc[0]
                if error_number not in (54, 104):
                    self.logger.exception(exc)
                    self.logger.warning('got socket error_number={}'.format(error_number))

                self.disconnect(client)
                continue

            self.handle_message(client, buf)
            handled = True

        if self.message_handler:
            self.message_handler.loop()

        return handled

    def quit(self):
        self.tcp_sock.close()
        self.udp_sock.close()

        # prevent getting exception where dictionary changes while looping
        connections = self.connections.keys()
        for connection in connections:
            self.disconnect(connection)

    def run(self):
        while self._run:
            self.loop()


class MessengerServer(BaseServer):
    def handle_message(self, client, buf):
        for line in buf.splitlines():
            if self.message_handler:
                self.message_handler.handle_message(client, self.connections[client], line)
            else:
                message = 'client={}, line={}'.format(self.connections[client], line)
                self.logger.info(message)

                try:
                    data = json.loads(line)
                except ValueError:
                    self.logger.error('unable to parse line={}'.format(line))
                else:
                    data['meta'] = {
                        'client': self.connections[client],
                    }

                    client.send(json.dumps(data))


class ConsoleMessengerServer(MessengerServer):
    port = 9628
    host = 'localhost'

    def __init__(self, host=None, port=None, message_handler=None):
        host = host or self.host
        port = port or self.port

        super(ConsoleMessengerServer, self).__init__(host, port, message_handler=message_handler)

    @property
    def connector(self):
        return get_connector()

    def handle_message(self, client, buf):
        message = parse_buf(buf)

        try:
            self.connector.send(message)
        except NotConnected:
            self.logger.warning('message={} dropped, not connected to upstream'.format(message))

    def loop(self, select_timeout=0.01):
        return super(ConsoleMessengerServer, self).loop(select_timeout=select_timeout)


if __name__ == '__main__':
    import argparse
    import sys

    parser = argparse.ArgumentParser()
    parser.add_argument('--loglevel', default='info')
    parser.add_argument('--host', default='localhost')
    parser.add_argument('--port', type=int, default=9628)

    args = parser.parse_args()

    loglevel = getattr(logging, args.loglevel.upper())
    logging.basicConfig(stream=sys.stdout, level=loglevel)

    server = BaseServer(args.host, args.port)
    try:
        server.run()
    except KeyboardInterrupt:
        server.quit()
