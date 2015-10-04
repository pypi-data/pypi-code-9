from .util import memoized_property
from .util import periodic_timer

import contextlib
import time
import threading
import sys


@contextlib.contextmanager
def stop_on_keyinterrupt():
    try:
        yield
    except KeyboardInterrupt:
        sys.exit()


class AsyncWaiter(object):
    __slots__ = (
        'factory', 'success', 'failure', 'timeout',
        'on_timeout', 'result', 'exception', 'event',
        'thread'
    )

    NO_RESULT = object()

    def __init__(self, factory, timeout=None, on_timeout=None):
        self.factory = factory
        self.timeout = timeout
        self.on_timeout = on_timeout
        self.event = factory.event()
        self.thread = None
        self.result = self.NO_RESULT
        self.exception = None

    def get(self):
        if self.thread is not None:
            self.thread.join()
        if self.exception:
            raise self.exception
        elif self.result is self.NO_RESULT:
            raise Exception(
                "No result loaded within timeout %s" % self.timeout)
        else:
            return self.result

    def set(self, value):
        self.result = value
        self.event.set()

    def set_exception(self, exception):
        self.exception = exception
        self.event.set()

    def start(self):
        self.thread = self.factory.spawn(self._wait)

    def _wait(self):
        if not self.event.wait(self.timeout):
            self.on_timeout()


class CallbackAsyncWaiter(AsyncWaiter):
    __slots__ = ('success', 'failure')

    def __init__(
            self, factory, success=None, failure=None, timeout=None,
            on_timeout=None):
        super(CallbackAsyncWaiter, self).__init__(factory, timeout, on_timeout)
        self.success = success
        self.failure = failure

    def get(self):
        raise NotImplementedError("can't call get() on a callback waiter")

    def _wait(self):
        if not self.event.wait(self.timeout):
            self.on_timeout()
        elif self.success and self.result is not self.NO_RESULT:
            self.success(self.result)
        elif self.failure and self.exception:
            self.failure(self.exception)


class AsyncSuite(object):
    @classmethod
    def get(cls, green=False):
        """Return a "suite" of async-sensitive utilities.

        This is a one-stop place to get a simple namespace with all those
        system calls that change w/ eventlet context.

        """
        if green:
            return _GreenAsyncSuite()
        else:
            return _ThreadedAsyncSuite()

    def create_connection(self, addr, timeout=None):
        return self.socket.create_connection(addr, timeout=timeout)

    def select_socket(self, socket, timeout):
        return self.select.select([socket], [], [], timeout)

    def background_thread(self, fn):
        def go():
            with stop_on_keyinterrupt():
                fn()

        thread = self.thread(go)
        thread.daemon = True
        thread.start()
        return thread

    def receive_messages(
            self, socket, message_terminator, ping_handler, ping_interval):

        ping_timer = periodic_timer(ping_interval)

        mtl = len(message_terminator)

        buf = []
        while True:

            try:
                ready_to_read, ready_to_write, in_error = \
                    self.select_socket(socket, int(ping_interval / 4))
            except self.select_error as se:
                raise IOError("Select error: %s" % se)

            if ready_to_read:
                data = socket.recv(1024)
                if data == '':
                    raise IOError("no more data")
                while True:
                    mti = data.find(message_terminator)
                    if mti != -1:
                        buf.append(data[0:mti])
                        data = data[mti + mtl:]
                        # print "receive message", ''.join(buf)
                        yield ''.join(buf)
                        buf[:] = []
                    else:
                        buf.append(data)
                        break

                continue

            if ping_timer(time.time()):
                # `print "running ping handler"
                ping_handler()

    def spawn_waiter(
            self, success=None, failure=None, timeout=None, on_timeout=None):
        if success:
            return CallbackAsyncWaiter(
                self, success, failure, timeout, on_timeout)
        else:
            return AsyncWaiter(self, timeout, on_timeout)

    def event(self):
        raise NotImplementedError()

    def sleep(self):
        raise NotImplementedError()

    def spawn(self, fn):
        raise NotImplementedError()

    def queue(self):
        raise NotImplementedError()

    @memoized_property
    def socket(self):
        raise NotImplementedError()

    @memoized_property
    def select(self):
        raise NotImplementedError()

    @memoized_property
    def select_error(self):
        return self.select.error

async_suite = AsyncSuite.get


class _ThreadedAsyncSuite(AsyncSuite):
    def event(self):
        return threading.Event()

    def sleep(self, duration):
        return time.sleep(duration)

    def spawn(self, fn, *args, **kw):
        t = threading.Thread(target=fn, args=args, kwargs=kw)
        t.start()
        return t

    def thread(self, fn):
        return threading.Thread(target=fn)

    def lock(self):
        return threading.Lock()

    @memoized_property
    def queue(self):
        import Queue
        return Queue.Queue

    @memoized_property
    def socket(self):
        import socket
        return socket

    @memoized_property
    def select(self):
        import select
        return select

    def server(self, address, callback, **ssl_args):
        raise NotImplementedError()


class _GreenAsyncSuite(AsyncSuite):
    def __init__(self):
        import eventlet as _et
        import eventlet.event as _et_event
        import eventlet.green as _et_green
        self._eventlet = _et
        self._eventlet_green = _et_green
        self._eventlet_event = _et_event

    def spawn(self, fn, *args, **kw):
        # we need a traditional threading API, e.g.
        # join()
        thread = self.threading.Thread(target=fn, args=args, kwargs=kw)
        thread.start()
        return thread

    @memoized_property
    def threading(self):
        from eventlet.green import threading
        return threading

    @memoized_property
    def queue(self):
        from eventlet import queue
        return queue.Queue

    def thread(self, fn):
        return self.threading.Thread(target=fn)

    @memoized_property
    def interrupted(self):
        import greenlet
        return greenlet.GreenletExit

    def event(self):
        from eventlet.green import threading
        return threading.Event()

    def sleep(self, duration):
        return self._eventlet.sleep(duration)

    def lock(self):
        return self.threading.Lock()

    @memoized_property
    def socket(self):
        return self._eventlet_green.socket

    @memoized_property
    def select(self):
        return self._eventlet_green.select

    def server(self, address, callback, **ssl_args):
        return _EventletServer(self, address, callback, **ssl_args)


class _EventletServer(object):
    def __init__(self, async_suite, address, callback, **ssl_args):
        if ssl_args:
            raise NotImplementedError("Ssl not supported yet")
        self.async_suite = async_suite
        self.address = address
        self.callback = callback

    def serve_forever(self):
        server = self.async_suite._eventlet.listen(self.address)
        with stop_on_keyinterrupt():
            while True:
                try:
                    socket, address = server.accept()
                except OSError:
                    pass
                else:
                    self.async_suite.spawn(self.callback, socket, address)
