__version__ = '1.0.4'
__authors__ = ['timchow<jordan23nbastar@yeah.net>']

import inspect
import socket
from kombu import Connection

class Discard(StandardError): pass
class Requeue(StandardError): pass

def ignore_exceptions(*exceptions):
    def _inner(f):
        def _innest(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except exceptions as e:
                return e
        return _innest
    return _inner

def check_function(f, n=1):
    assert callable(f), "%r is not a callable object" % f
    assert len(inspect.getargspec(f).args) >= n, \
        "%s must take at least %d argument(s)" % (f, n)
    return f

class Message:
    def __init__(self, f, queue, tag, *args, **kwargs):
        self._f = check_function(f, 1)
        self._q = queue
        self._tag = tag

        self._is_quit = False
        self._requeue_exceptions = tuple()
        self._discard_exceptions = tuple()
        self._exc_cb = self.default_exception_callback
        self._conn = Connection(*args, **kwargs)

    def default_exception_callback(self, channel, message, e):
        channel.basic_reject(message.delivery_tag, requeue=True)

    def close(self):
        if hasattr(self, '_chan') and hasattr(self._chan, 'close'):
            ignore_exceptions(Exception)(self._chan.close)()
        ignore_exceptions(Exception)(self._conn.close)()

    def _init_channel(self, prefetch_size=0, prefetch_count=4, a_global=True, *args, **kwargs):
        self._conn = self._conn.ensure_connection(*args, **kwargs)
        self._chan = self._conn.channel()
        self._chan.basic_qos(prefetch_size, prefetch_count, a_global)
        self._chan.basic_consume(queue=self._q, no_ack=False, 
                    callback=self._wrap_f, consumer_tag=self._tag)

    def _wrap_f(self, message, *args , **kwargs):
        try:
            self._f(message, *args, **kwargs)
        except (Discard, ) + self._discard_exceptions:
            self._chan.basic_reject(message.delivery_tag, requeue=False)
        except (Requeue, ) + self._requeue_exceptions:
            self._chan.basic_reject(message.delivery_tag, requeue=True)
        except Exception as e:
            self._exc_cb(self._chan, message, e)
        else:
            self._chan.basic_ack(message.delivery_tag)

    def loop(self, timeout=3, *args, **kwargs):
        self._init_channel(*args, **kwargs)
        while not self._is_quit:
            try:
                self._conn.drain_events(timeout=timeout)
            except socket.timeout:
                pass
            except IOError as exc:
                if "[Errno 4] Interrupted system call" in str(exc):
                    continue
                self._init_channel(*args, **kwargs)
        self.close()

    def __del__(self):
        self.close()

    def is_quit(self, quit):
        self._is_quit = bool(quit)

    def set_requeue_exceptions(self, *args, **kwargs):
        self._requeue_exceptions = args

    def set_discard_exceptions(self, *args, **kwargs):
        self._discard_exceptions = args

    def set_exception_callback(self, cb):
        self._exc_cb = check_function(cb, 3)

