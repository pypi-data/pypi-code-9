import socket
import logging
import threading
import Queue

from pyasn1.codec.ber import encoder

from ber import Message


class QriPython(threading.Thread):

    def __init__(self, host=None, port=None):
        super(QriPython, self).__init__()
        self.host = host
        self.port = port
        self.queue = Queue.Queue()
        self.alive = threading.Event()
        self.alive.set()
        self.daemon = True
        self.sock = None
        self.msg = Message()

        self.connect()
        self.start()

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.sock.connect((self.host, self.port))
            return self.sock

        except socket.error, msg:
            logging.error("[QRI-PY] Server {0}:{1} unreachable: {2}".format(
                self.host, self.port, msg
            ))
            return None

    def run(self):
        while self.alive.isSet():
            try:
                packed_data = self.queue.get()
                self._send(packed_data)
            except Queue.Empty as e:
                continue

    def join(self, timeout=None):
        self.alive.clear()
        threading.Thread.join(self, timeout)

    def close(self):
        return self.sock.close()

    def reconnect(self):
        self.close()
        return self.connect()

    def _send(self, packed_data):
        try:
            return self.sock.send(packed_data)
        except socket.error:
            sock = self.reconnect()
            if not sock:
                return None

            try:
                return sock.send(packed_data)
            except socket.error, msg:
                logging.error("[QRI-PY] Error occurred during sending: {0}".format(msg))
                return None

    def send(self, peer=None, checksum=None, message=None):
        self.msg.setComponentByName('peer', peer)
        self.msg.setComponentByName('checksum', checksum)
        self.msg.setComponentByName('message', message)
        return self.queue.put(encoder.encode(self.msg))
