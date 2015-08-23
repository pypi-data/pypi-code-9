import json
import logging
import socket
import sys
import time

from select import select

import websocket

from backoff import Backoff

from zymbit.envelope import get_envelope


ACK_TIMEOUT = 5 # 5 seconds to get an ack
BUFSIZE = 4096
MAX_BACKOFF = 300 # retry connection once a minute


class MessengerClient(object):
    def __init__(self, host=None, port=None):
        self.addr = (host, port)

        self.sock = None

        # keep track of the last message sent in case the socket goes boom.  in
        # that case, requeue the last message to go out again.
        self.last_message = None

        # messages that have not been sent
        self.outbound_queue = []

        self.inbound_queue = []

    @property
    def logger(self):
        name = '{}.{}'.format(__name__, self.__class__.__name__)

        return logging.getLogger(name)

    @Backoff()
    def _check_connection(self):
        if self.sock:
            return True

        try:
            self.connect()
        except socket.error, exc:
            self.sock = None

            if exc[0] not in (61, 111):
                raise

            return False

        return True

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(self.addr)

        self.logger.debug('connected to %s' % (self.addr,))

    def fileno(self):
        return self.sock.fileno()

    def loop(self):
        """
        Process the outbound message queue
        """

        if not self._check_connection():
            return False

        ready, _, _ = select([self.sock], [], [], 0.01)
        if ready:
            try:
                buf = self._recv()

                # when an empty buffer is received, the connection is dead.
                if buf in (None, ''):
                    self.sock = None
                    return False

                self.logger.debug('buffer: %r' % (buf,))
                for line in buf.splitlines():
                    # skip empty lines
                    if not line:
                        continue

                    self.inbound_queue.append(json.loads(line))
            except socket.error, exc:
                # [Errno 54] Connection reset by peer
                # socket.error: (104, 'Connection reset by peer')
                if exc[0] not in (54, 104):
                    raise

                self.sock = None

                return False

        while self.outbound_queue:
            try:
                envelope = get_envelope(*self.outbound_queue[0])
                self._send('{}\n'.format(envelope))
            except socket.error, exc:
                # [Errno 32] Broken pipe
                if exc[0] != 32:
                    raise

                self.sock.close()
                self.sock = None

                break
            else:
                # remove from the queue
                self.outbound_queue.pop(0)

    def queue(self, action, params):
        self.outbound_queue.append((action, params))

    def _recv(self):
        return self.sock.recv(BUFSIZE)

    def recv(self):
        if self.inbound_queue:
            return self.inbound_queue.pop(0)

    def _send(self, envelope):
        self.sock.send(envelope)

    def send(self, action, params):
        print 'adding to queue, action={}, params={}'.format(action, params)
        self.queue(action, params)


class WebsocketMessengerClient(MessengerClient):
    def __init__(self, url):
        super(WebsocketMessengerClient, self).__init__()

        self.client = None
        self.sock = None

        self.url = url

    def _check_incoming(self):
        if not self.sock:
            return

        try:
            message = self.client.recv()

            self.inbound_queue.append(message)

            return True
        except websocket.WebSocketException, exc:
            return False
        except socket.error, exc:
            #socket.error: [Errno 35] Resource temporarily unavailable
            #socket.error: [Errno 54] Connection reset by peer
            if exc[0] not in (35, 54):
                raise

    def connect(self):
        print 'try to connect to websocket'
        try:
            self.client = websocket.create_connection(self.url)
            self.client.settimeout(0)

            self.sock = self.client.sock
        except socket.error, exc:
            self.client = None
            self.sock = None

            raise

    def fileno(self):
        return self.sock.fileno()

    def _recv(self):
        try:
            return self.client.recv()
        except websocket.WebSocketException, exc: # Not a valid frame None
            self.client = None
            self.sock = None
        except socket.error, exc:
            # [Errno 35] Resource temporarily unavailable
            if exc[0] != 35:
                raise

            self.client = None
            self.sock = None

    def _send(self, envelope):
        buf = json.dumps(envelope)
        self.client.send(buf)

