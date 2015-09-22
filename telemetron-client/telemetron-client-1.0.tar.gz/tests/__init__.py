import threading
import SocketServer
import logging
import unittest

from telemetron.client import Client

server = None
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

SocketServer.TCPServer.allow_reuse_address = True

CLIENT_HOST = "127.0.0.1"
CLIENT_PORT = 2013

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
    lastResponse = None

    def handle(self):
        data = self.request.recv(1024)
        cur_thread = threading.current_thread()
        log.debug("Got data: '%s'" % (data,))
        lastResponse = data

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


class TestSocketTypes(unittest.TestCase):
    def setUp(self):
        self.server = ThreadedTCPServer((CLIENT_HOST, CLIENT_PORT), ThreadedTCPRequestHandler)
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()

    def testTcp(self):
        from random import randint
        c = Client(socket_type=Client.TCP_SOCKET)
        self.assertNotEqual(c._socket, None)
        for i in range(10):
            c.time("time%d"%(i,), randint(1,100))
            c.gauge("gauge%d"%(i,), randint(1,100))
            c.inc("inc%d"%(i,), randint(1,100))

        self.assertEqual(c.bufferCount(), 30)
        c.flush()
        self.assertEqual(c.bufferCount(), 0)


    def testUdp(self):
        from random import randint
        c = Client(socket_type=Client.UDP_SOCKET)
        self.assertNotEqual(c._socket, None)
        for i in range(10):
            c.time("time%d"%(i,), randint(1,100))
            c.gauge("gauge%d"%(i,), randint(1,100))
            c.inc("inc%d"%(i,), randint(1,100))

        self.assertEqual(c.bufferCount(), 30)
        c.flush()
        self.assertEqual(c.bufferCount(), 0)



    def testInvalid(self):
        self.assertRaises(ValueError, Client, socket_type="invalid")
