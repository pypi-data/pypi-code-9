# -*- coding: UTF-8 -*-
# pylint: disable=missing-docstring

"""
Testing SyRPC
"""

# System imports
import mock
try:
    import unittest2           as unittest
except ImportError:  # pragma: no cover
    import unittest

# Project imports
import syrpc.constants as const
import syrpc.server    as server
import syrpc.client    as client
import syrpc


class TestBase(unittest.TestCase):
    def setUp(self):
        self.settings = {
            'app_name':      const.General.APP_NAME,
            'amq_host':      'virtual',
            'amq_transport': 'memory',
            'amq_msg_ttl':   1
        }
        self.server = server.Server(self.settings)
        self.client = client.Client(self.settings)
        self.expected_data = [{'foo': 'bar'}, {'baz': 9001}]
        self.type_ = 'ping'

    def tearDown(self):
        del self.client
        del self.server


class ClientTest(TestBase):
    """Testing client methods"""

    def put_request(self):
        return self.client.put_request(self.type_, self.expected_data)

    def test_put_request(self):
        result_id = self.put_request()
        self.assertIsNotNone(result_id)
        self.server.get_request()

    def test_get_result(self):
        result_id = self.put_request()
        (type_, srv_result_id, data) = self.server.get_request()
        self.assertEqual(self.type_, type_)
        self.assertEqual(str(result_id), srv_result_id)
        self.server.put_result(srv_result_id, data)
        result = self.client.get_result(result_id)
        expected_result = {
            'result_id': str(result_id),
            'data':      self.expected_data,
        }
        self.assertEqual(result, expected_result)

    def test_get_result_timeout(self):
        with self.assertRaises(syrpc.EmptyException):
            self.client.get_result('foo-bar-baz', 1)

    def test_wrong_result_id(self):
        self.put_request()
        message = self.server.request_queue.get(block=True, timeout=1)
        self.client.wait_id = 'foo-bar-baz'
        self.client.on_result(body=message.body, message=message)
        self.assertIsNone(self.client.response)


class ServerTest(TestBase):
    """Testing server methods"""

    def test_get_request_empty(self):
        ex = self.server.request_queue.Empty
        self.server.request_queue.get = mock.Mock()
        self.server.request_queue.get.side_effect = ex
        with self.assertRaises(server.EmptyException):
            self.server.get_request(timeout=0)

    def test_get_request_not_found(self):
        ex = server.aexcept.NotFound
        self.server.request_queue.get = mock.Mock()
        self.server.request_queue.get.side_effect = ex
        with self.assertRaises(server.QueueNotFoundException):
            self.server.get_request(timeout=0)

    def test_get_result_queue(self):
        queue1 = self.server.get_result_queue(1)
        queue2 = self.server.get_result_queue(1)
        self.assertEqual(queue1, queue2)
