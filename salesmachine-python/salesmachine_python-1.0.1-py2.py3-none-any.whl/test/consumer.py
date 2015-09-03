import unittest

try:
    from queue import Queue
except:
    from Queue import Queue

from salesmachine.consumer import Consumer


class TestConsumer(unittest.TestCase):

    def test_next(self):
        q = Queue()
        consumer = Consumer(q, '', debug=True)
        q.put(1)
        next = consumer.next()
        self.assertEqual(next, [1])

    def test_next_limit(self):
        q = Queue()
        upload_size = 50
        consumer = Consumer(q, '', debug=True, upload_size=upload_size)
        for i in range(10000):
            q.put(i)
        next = consumer.next()
        self.assertEqual(next, list(range(upload_size)))

    def test_upload(self):
        q = Queue()
        consumer  = Consumer(q, 'key', 'secret', debug=True)
        track = {
            'method': 'set_contact',
            'contact_uid': 'contact_uid'
        }
        consumer.request([track])
        q.put(track)
        success = consumer.upload()
        self.assertTrue(success)

    def test_request(self):
        consumer = Consumer(None, 'key', 'secret', debug=True)
        track = {
            'method': 'set_contact',
            'contact_uid': 'contact_uid'
        }
        consumer.request([track])

    def test_pause(self):
        consumer = Consumer(None, 'testsecret', debug=True)
        consumer.pause()
        self.assertFalse(consumer.running)
