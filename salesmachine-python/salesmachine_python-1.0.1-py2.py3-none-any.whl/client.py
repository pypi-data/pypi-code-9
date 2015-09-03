from datetime import datetime
from uuid import uuid4
import logging
import numbers

from dateutil.tz import tzutc
from six import string_types

from salesmachine.utils import guess_timezone, clean
from salesmachine.consumer import Consumer
from salesmachine.version import VERSION

try:
    import queue
except:
    import Queue as queue


ID_TYPES = (numbers.Number, string_types)


class Client(object):
    """Create a new Salesmachine client."""
    log = logging.getLogger('salesmachine')

    def __init__(self, key=None, secret=None, url = 'https://api.salesmachine.io/v1/batch', debug=False, max_queue_size=10000,
                 send=True, on_error=None):
        require('key', key, string_types)
        require('secret', secret, string_types)

        self.queue = queue.Queue(max_queue_size)
        self.consumer = Consumer(self.queue, key, secret, url, on_error=on_error)
        self.key = key
        self.on_error = on_error
        self.url = url
        self.send = send

        if debug:
            self.log.setLevel(logging.DEBUG)

        # if we've disabled sending, just don't start the consumer
        if send:
            self.consumer.start()

    def set_contact(self, contact_uid, params={}):
        msg = {
            'method': 'contact',
            'contact_uid': contact_uid,
            'params': params
        }

        return self._enqueue(msg)

    def set_account(self, account_uid, params={}):
        msg = {
            'method': 'account',
            'account_uid': account_uid,
            'params': params
        }

        return self._enqueue(msg)

    def track_event(self, contact_uid, event_uid, params={}):
        msg = {
            'method': 'event',
            'contact_uid': contact_uid,
            'event_uid': event_uid,
            'params': params
        }

        return self._enqueue(msg)

    def track_pageview(self, contact_uid, params={}):
        msg = {
            'method': 'event',
            'contact_uid': contact_uid,
            'event_uid': 'pageview',
            'params': params
        }

        return self._enqueue(msg)

    def _enqueue(self, msg):
        """Push a new `msg` onto the queue, return `(success, msg)`"""
        timestamp = datetime.utcnow().replace(tzinfo=tzutc())

        require('type', msg['method'], string_types)
        require('timestamp', timestamp, datetime)

        # add common
        timestamp = guess_timezone(timestamp)
        #msg['timestamp'] = timestamp.isoformat()

        msg = clean(msg)
        self.log.debug('queueing: %s', msg)

        if self.queue.full():
            self.log.warn('salesmachine-python queue is full')
            return False, msg

        self.queue.put(msg)
        self.log.debug('enqueued ' + msg['method'] + '.')
        return True, msg

    def flush(self):
        """Forces a flush from the internal queue to the server"""
        queue = self.queue
        size = queue.qsize()
        queue.join()
        self.log.debug('successfully flushed {0} items.'.format(size))

    def join(self):
        """Ends the consumer thread once the queue is empty. Blocks execution until finished"""
        self.consumer.pause()
        self.consumer.join()


def require(name, field, data_type):
    """Require that the named `field` has the right `data_type`"""
    if not isinstance(field, data_type):
        msg = '{0} must have {1}, got: {2}'.format(name, data_type, field)
        raise AssertionError(msg)
