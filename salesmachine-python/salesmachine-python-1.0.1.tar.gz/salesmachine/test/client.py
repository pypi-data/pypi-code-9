from datetime import datetime
import unittest
import time
import six

from salesmachine.version import VERSION
from salesmachine.client import Client


class TestClient(unittest.TestCase):

    def fail(self, e, batch):
        """Mark the failure handler"""
        self.failed = True

    def setUp(self):
        self.failed = False
        self.client = Client("key", "secret", debug=True, on_error=self.fail)

    def test_requires_write_key(self):
        self.assertRaises(AssertionError, Client)

    def test_empty_flush(self):
        self.client.flush()

    def test_basic_track_event(self):
        client = self.client
        success, msg = client.track_event('contact_uid', 'event_uid')
        client.flush()
        self.assertTrue(success)
        self.assertFalse(self.failed)

        self.assertEqual(msg['contact_uid'], 'contact_uid')
        self.assertEqual(msg['event_uid'], 'event_uid')
        self.assertEqual(msg['method'], 'event')

    def test_basic_set_contact(self):
        client = self.client
        success, msg = client.set_contact('contact_uid', {'name': 'Jean'})
        client.flush()
        self.assertTrue(success)
        self.assertFalse(self.failed)

        self.assertEqual(msg['params'], {'name': 'Jean' })
        self.assertEqual(msg['contact_uid'], 'contact_uid')
        self.assertEqual(msg['method'], 'contact')

    def test_basic_set_account(self):
        client = self.client
        success, msg = client.set_account('account_uid', {'name': 'Jean Corp.'})
        client.flush()
        self.assertTrue(success)
        self.assertFalse(self.failed)

        self.assertEqual(msg['params'], {'name': 'Jean Corp.' })
        self.assertEqual(msg['account_uid'], 'account_uid')
        self.assertEqual(msg['method'], 'account')

    def test_basic_track_pageview(self):
        client = self.client
        success, msg = client.track_pageview('contact_uid', {'display_name': 'Jean has seen page 2.'})
        client.flush()
        self.assertTrue(success)
        self.assertFalse(self.failed)

        self.assertEqual(msg['params'], {'display_name': 'Jean has seen page 2.'})
        self.assertEqual(msg['contact_uid'], 'contact_uid')
        self.assertEqual(msg['method'], 'event')

    def test_flush(self):
        client = self.client
        # send a few more requests than a single batch will allow
        for i in range(60):
            success, msg = client.set_contact('contact_uid', { 'name': 'value' })

        self.assertFalse(client.queue.empty())
        client.flush()
        self.assertTrue(client.queue.empty())

    def test_overflow(self):
        client = Client('testkey', 'testsecret', max_queue_size=1)
        client.consumer.pause()
        time.sleep(5.1) # allow time for consumer to exit

        for i in range(10):
          client.set_contact('contact_uid')

        success, msg = client.set_contact('contact_uid')
        self.assertFalse(success)

    def test_error_on_invalid_write_key(self):
        client = Client('bad_key', 'bad_secret', on_error=self.fail)
        client.set_contact('contact_uid')
        client.flush()
        self.assertTrue(self.failed)

    def test_unicode(self):
        Client('tetskey', six.u('unicode_key'))

    def test_numeric_user_id(self):
        self.client.set_contact(789)
        self.client.flush()
        self.assertFalse(self.failed)

    def test_debug(self):
        Client('bad_key', 'bad_secret', debug=True)
