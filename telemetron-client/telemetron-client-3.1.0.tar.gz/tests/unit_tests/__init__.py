"""
Unit tests module
"""
import threading
import unittest
import time
import os
from random import randint

from telemetronclient.telemetronclient import TelemetronClient as Client
from telemetronclient.telemetronclient import BufferSizeTooLarge
from telemetronclient.telemetronclient import AutoFlushTelemetronClient \
                                              as AutoFlushClient

from tests.unit_tests.helpers import MockHTTPHandler
from tests.unit_tests.helpers import ThreadedTCPRequestHandler
from tests.unit_tests.helpers import ThreadedTCPServer


class TestAPIClient(unittest.TestCase):
    def setUp(self):
        self.server = ThreadedTCPServer(("localhost", 4443),
                                        MockHTTPHandler)
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()

    def test_APIClient_201(self):
        c = Client(transport=Client.TRANSPORT_API, host="localhost",
                   port=4443)
        MockHTTPHandler.ret_code = 201
        c.time("timer1", 20)
        self.assertTrue(c.flush())

    def test_APIClient_200(self):
        c = Client(transport=Client.TRANSPORT_API, host="localhost",
                   port=4443)
        MockHTTPHandler.ret_code = 200
        c.time("timer1", 20)
        self.assertFalse(c.flush())


class TestClientInitialization(unittest.TestCase):
    def setUp(self):
        CLIENT_HOST = "127.0.0.1"
        CLIENT_PORT = 2013

        self.server = ThreadedTCPServer((CLIENT_HOST, CLIENT_PORT),
                                        ThreadedTCPRequestHandler)
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()

    def test_ClientObject_CreateInvalidSocketType_Raises(self):
        self.assertRaises(ValueError, Client, transport="invalid")

    def test_ClientObject_CreateInvalidSampleRate_Raises(self):
        self.assertRaises(ValueError, Client, transport=Client.TRANSPORT_UDP,
                          init_transport=False, sample_rate=0)

        self.assertRaises(ValueError, Client, transport=Client.TRANSPORT_UDP,
                          init_transport=False, sample_rate=100)

    def test_AutoFlushClient_PopulateBufferUntilLimit_ShouldFlush(self):
        from random import randint

        c = AutoFlushClient(flush_size=10,
                            transport=Client.TRANSPORT_UDP)

        for i in range(9):
            c.time("time%d" % (i,), randint(1, 100), namespace="foo")

        self.assertEqual(c.buffer_count(), 9)

        c.time("time%d" % (10,), randint(1, 100), namespace="bar")

        self.assertEqual(c.buffer_count(), 0)


class TestBuffer(unittest.TestCase):
    def test_Buffer_PopulateAndFlush_IsEmpty(self):
        c = Client(transport=Client.TRANSPORT_UDP)
        for i in range(10):
            c.time("time%d" % (i,), randint(1, 100))
            c.gauge("gauge%d" % (i,), randint(1, 100))
            c.inc("inc%d" % (i,), randint(1, 100))

        c.flush()
        self.assertEqual(c.buffer_count(), 0)

    def test_BufferLine_GenerateLinesWithDiffTimeStamp_BeDifferent(self):
        t = time.time()
        c = Client(transport=Client.TRANSPORT_UDP, init_transport=False)
        line1 = c.make_line("foo", {}, 100, timestamp=t-10)
        line2 = c.make_line("bar", {}, 10, timestamp=t)
        self.assertEqual(int(line1.split(' ')[2])+10, int(line2.split(' ')[2]))

    def test_MaxBufferSize_Raise(self):
        c = Client(transport=Client.TRANSPORT_UDP, max_buffer_size=100)
        for i in range(c.max_buffer_size):
            c.time("time%d" % (i,), randint(1, 100))

        self.assertRaises(
            BufferSizeTooLarge,
            c.time,
            "time%d" % (c.max_buffer_size+1,),
            randint(1, 100)
            )
