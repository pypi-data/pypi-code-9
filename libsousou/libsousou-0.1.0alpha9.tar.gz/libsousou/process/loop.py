import atexit
import contextlib
import grp
import logging
import multiprocessing
import os
import pwd
import signal
import sys
import threading
import time
import warnings

SIGNAL_MAP = dict((k, v) for v, k in reversed(sorted(signal.__dict__.items()))
     if v.startswith('SIG') and not v.startswith('SIG_'))


class BaseProcess(object):
    default_signals = [
        signal.SIGTERM,
        signal.SIGHUP,
        signal.SIGINT
    ]
    signals = []
    logger_name = None

    @classmethod
    def as_process(cls, defer=True, args=None, kwargs=None):
        args, kwargs = args or [], kwargs or {}
        p = cls(*args, **kwargs)
        return p.start_process(defer=defer)

    @classmethod
    def as_thread(cls, daemon=False, defer=True, args=None, kwargs=None):
        args, kwargs = args or [], kwargs or {}
        p = cls(*args, **kwargs)
        return p.start_threaded(daemon=daemon, defer=defer)

    def __init__(self, suppress_exceptions=False, framerate=None):
        """Initialize a new :class:`BaseProcess` instance.

        Args:
            suppress_exceptions (bool): indicates if exceptions are to be
                suppressed. Default is False, meaning that exceptions will
                be raised after cleaning up.
            framerate: specifies a waiting period after finished one
                event loop.
        """
        self._needs_update = True
        self._must_exit = False
        self._suppress_exceptions = suppress_exceptions
        self._framerate = framerate
        self._evnt_exit = threading.Event()
        self.signals = tuple(
            set(list(self.signals) + list(self.default_signals)))

        # The execution time of the last event loop.
        self.previous_execution_time = 1
        self.pid = os.getpid()
        self.thread = None
        self.process = None

    def _setup(self):
        self.logger = logging.getLogger(self.logger_name or '__main__')
        self.setup()
        self._needs_update = False

    def setup(self):
        """Hook to set up the process state."""
        pass

    def register_signals(self):
        """Binds signals to the :meth:`BaseProcess.signal_handler`
        method.
        """
        if isinstance(threading.current_thread(), threading._MainThread):
            for signum in self.signals:
                signal.signal(signum, self.signal_handler)

    def run(self):
        warnings.warn("run() is deprecated, use start() instead",
            DeprecationWarning, stacklevel=2)
        self.start()

    def start_threaded(self, defer=False, daemon=False):
        """Arrange for the main event loop to be started in a separate
        thread of control.

        Args:
            defer (bool): defer starting the main event loop.
            daemon (bool): indicates that the thread is a daemon,
                causing it to terminate when it's parent thread
                has terminated.

        Returns:
            threading.Thread
        """
        thread = threading.Thread(target=self.start)
        if daemon:
            thread.daemon = True
        if not defer:
            thread.start()
        self.thread = thread
        return thread

    def start_process(self, defer=False):
        """Arrange for the main event loop to be started in a separate
        process.

        Args:
            defer (boolean): defer starting the main event loop.

        Returns:
            multiprocessing.Process
        """
        process = multiprocessing.Process(target=self.start)
        if not defer:
            process.start()
        self.pid = process.pid
        return process

    def start(self):
        """Enter the process main loop and execute the
        :func:`BaseProcess.main_event`.
        """
        # Setup the process.
        try:
            self._setup()
        except Exception as e:
            self.logger.exception("FATAL: Exception during setup.")
            return
        logger = self.logger

        # Bind signals here. To change this behavior, override
        # register_signals().
        self.register_signals()

        exception = None
        while True:
            if self._evnt_exit.is_set():
                break

            started = time.time()
            try:
                # Check if we need to exit and if so bail out
                # immediately.
                if self.must_exit():
                    logger.debug("Cleaning up and exiting")
                    self.do_cleanup(True)
                    self.do_exit()
                    break

                # if the update() method has been called,
                # refresh the state of the process.
                if self._needs_update:
                    self._do_update()

                try:
                    started = time.time()
                    self.main_event()
                    ended = time.time()
                    self.previous_execution_time = ended - started
                except NotImplementedError:
                    raise
                except Exception as exception:
                    if self.exception_handler(exception):
                        self.do_cleanup(False)
                        if self.must_exit(): # Don't raise if we must exit.
                            break
                        raise
            except KeyboardInterrupt:
                self._evnt_exit.set()
                self.join()
            except Exception:
                self._evnt_exit.set()
                raise

        self._evnt_exit.set()

    def main_event(self):
        raise NotImplementedError

    def must_exit(self):
        """Returns a boolean indicating if the main event loop
        should exit.
        """
        return self._must_exit is True

    def update(self):
        """Indicates that :meth:`BaseProcess.do_update`
        should be called."""
        self._needs_update = True

    def stop(self):
        self._must_exit = True

    def join(self):
        """Gracefully exits the process."""
        self.logger.info("Gracefully exiting main event loop")
        self.stop()
        if self.thread:
            self.thread.join()

    def _do_update(self):
        try:
            self.do_update()
        except Exception as e:
            self.logger.exception("FATAL: Uncaught exception in do_update()!")
        finally:
            self._needs_update = False

    def do_update(self):
        """Hook to update the program state."""
        pass

    def do_exit(self):
        """Gracefully exit the process. May perform any cleanup
        tasks needed by the process."""
        pass

    def do_cleanup(self, gracecul):
        """Performs cleanup prior to exiting (wether it's gracecul or
        caused by an exception).

        Args:
            graceful: indicates if the cleanup is the result of a
                graceful main event loop interruption.

        Returns:
            None
        """
        pass

    def signal_handler(self, signum, frame):
        signame = SIGNAL_MAP.get(signum, '<UNKNOWN>')
        self.logger.debug("Interrupted by {0}".format(signame))
        if signum == signal.SIGHUP:
            self.update()
        if signum in (signal.SIGTERM, signal.SIGINT):
            self.join()

    def exception_handler(self, exception):
        """Hook to handle a fatal exception in the main event loop.
        MUST return a boolean indicating if the exception should
        be reraised.
        """
        return True

    def teardown(self):
        """Releases all resources and locks claimed by the process."""
