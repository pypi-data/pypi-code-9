from __future__ import absolute_import

from concurrent.futures import Future
from threading import Event, Thread

from tornado import ioloop

from .exceptions import ThreadNotStartedError

# Python3's concurrent.futures.Future doesn't allow
# setting exc_info... but exc_info works w/o setting explicitly
_FUTURE_HAS_EXC_INFO = hasattr(Future, "set_exception_info")


class ThreadLoop(object):
    """Tornado IOLoop Backed Concurrent Futures.

    Run Tornado Coroutines from Synchronous Python.

    This is made possible by starting the IOLoop in another thread. When
    coroutines are submitted, they are ran against that loop, and their
    responses are bound to Concurrent Futures.

    .. code-block:: python

        from threadloop import ThreadLoop
        from tornado import gen

        @gen.coroutine
        def coroutine(greeting="Goodbye"):
            yield gen.sleep(1)
            raise gen.Return("%s World" % greeting)

        with ThreadLoop() as threadloop:

            future = threadloop.submit(coroutine, "Hello")

            print future.result() # Hello World

    """
    def __init__(self, io_loop=None):

        self._thread = None
        self._ready = Event()

        if io_loop is None:
            self._io_loop = ioloop.IOLoop()
        else:
            self._io_loop = io_loop

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args):
        self.stop()

    def start(self):
        """Start IOLoop in daemonized thread."""
        assert self._thread is None, 'thread already started'

        # configure thread
        self._thread = Thread(target=self._start_io_loop)
        self._thread.daemon = True

        # begin thread and block until ready
        self._thread.start()
        self._ready.wait()

    def _start_io_loop(self):

        def mark_as_ready():
            self._ready.set()

        self._io_loop.add_callback(mark_as_ready)
        self._io_loop.start()

    def is_ready(self):
        """Is thread & ioloop ready."""

        if not self._thread:
            return False

        if not self._ready.is_set():
            return False

        return True

    def stop(self):
        """Stop IOLoop & close daemonized thread."""
        self._io_loop.stop()
        self._thread.join()

    def submit(self, fn, *args, **kwargs):
        """Submit Tornado Coroutine to IOLoop in daemonized thread.

        :param fn: Tornado Coroutine to execute
        :param args: Args to pass to coroutine
        :param kwargs: Kwargs to pass to coroutine
        :returns concurrent.futures.Future: future result of coroutine
        """
        if not self.is_ready():
            raise ThreadNotStartedError(
                "The thread has not been started yet, "
                "make sure you call start() first"
            )

        future = Future()

        def on_done(tornado_future):

            if not tornado_future.exception():
                future.set_result(tornado_future.result())
                return

            exception, traceback = tornado_future.exc_info()[1:]

            # python2 needs exc_info set explicitly
            if _FUTURE_HAS_EXC_INFO:
                future.set_exception_info(exception, traceback)
                return

            # python3 just needs the exception, exc_info works fine
            future.set_exception(exception)

        self._io_loop.add_callback(
            lambda: fn(*args, **kwargs).add_done_callback(on_done)
        )

        return future
