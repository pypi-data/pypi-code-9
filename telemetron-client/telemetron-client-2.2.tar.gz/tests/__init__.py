import threading
import SocketServer
import logging
import unittest
import time
from Queue import Queue

from Queue import Empty

from telemetronclient import TelemetronClient as Client
from telemetronclient import AutoFlushTelemetronClient as AutoFlushClient

server = None
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

SocketServer.TCPServer.allow_reuse_address = True

CLIENT_HOST = "127.0.0.1"
CLIENT_PORT = 2013


class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
    lastResponse = None
    receivedLines = Queue()

    def handle(self):
        if not hasattr(self, "buffer"):
            self.buffer = ""

        data = self.buffer + self.request.recv(1024)

        i = 0
        last = 0
        while 1:
            last = i
            i = data.find("\n", i)
            if i == -1:
                break
            self.receivedLines.put(data[last:i])
            i += 1

        self.buffer += data[last:]

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


    def testTcpType(self):
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


    def testUdpType(self):
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



class TestTimeStamp(unittest.TestCase):
    def testTimestampOverride(self):
        t = time.time()
        c = Client(socket_type=Client.UDP_SOCKET, start_socket=False)
        line1 = c.makeLine("foo", {}, 100, timestamp=t-10)
        line2 = c.makeLine("bar", {}, 10, timestamp=t)
        self.assertEqual(int(line1.split(' ')[2])+10, int(line2.split(' ')[2]))



class TestSampleRateRange(unittest.TestCase):
    def test(self):
        t = time.time()
        self.assertRaises(ValueError, Client, socket_type=Client.UDP_SOCKET,
                          start_socket=False, sample_rate=0)

        self.assertRaises(ValueError, Client, socket_type=Client.UDP_SOCKET,
                          start_socket=False, sample_rate=100)


class TestAutoFlushClient(unittest.TestCase):

    def setUp(self):
        self.server = ThreadedTCPServer((CLIENT_HOST, CLIENT_PORT), ThreadedTCPRequestHandler)
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()


    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()


    def testAutoFlush(self):
        from random import randint

        c = AutoFlushClient(flush_size=10,
            socket_type=Client.TCP_SOCKET)

        self.assertEqual(c.bufferCount(), 0)
        for i in range(9):
            c.time("time%d"%(i,), randint(1,100), namespace="foo")

        self.assertEqual(c.bufferCount(), 9)

        c.time("time%d"%(10,), randint(1,100), namespace="bar")

        self.assertEqual(c.bufferCount(), 0)

        counter = {
            'foo':0,
            'bar':0,
            'application':0
        }

        s = time.time()
        while 1:
            try:
                m = ThreadedTCPRequestHandler.receivedLines.get_nowait()
                if ".foo" in m:
                    counter["foo"] += 1
                elif ".bar" in m:
                    counter["bar"] += 1
                elif ".application" in m:
                    counter["bar"] += 1
                else:
                    raise ValueError("Invalid line type")
            except Empty:
                time.sleep(0.05)

            if sum(counter.values()) == 11:
                break

            self.assertLess(time.time()-s, 5.0)

        self.assertEqual(sum(counter.values()), 11)
