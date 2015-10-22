from __future__ import print_function
import errno
import fcntl
import os
import sys


class FLock(object):
    """Locks a file until it's closed.

    Not compatible over NFS, but works with NFS mounted shares locally.
    """

    def __init__(self, filename):
        # This will create it if it does not exist already
        self._filename = filename
        self._handle = open(filename, 'w')

    # Bitwise OR fcntl.LOCK_NB if you need a non-blocking lock
    def acquire(self):
        fcntl.flock(self._handle, fcntl.LOCK_EX)

    def release(self):
        fcntl.flock(self._handle, fcntl.LOCK_UN)
        os.remove(self._filename)

    def __del__(self):
        self._handle.close()


class UsageCounter(object):
    """File based usage counter. Uses a lock file.
    """
    def __init__(self, filename):
        self._filename = filename
        self._lock = None

    def incr(self):
        return self._incr(1)

    def decr(self):
        return self._incr(-1)

    def reset(self):
        return self._set_value(0)

    def _incr(self, value):
        assert self._lock
        counter = self._get_value()
        counter += value
        if counter < 0:
            print("bad usage counter. Resetting to 0.", file=sys.stderr)
            counter = 0
        return self._set_value(counter)

    def _set_value(self, value):
        with open(self._filename, 'w') as f_obj:
            f_obj.write('%d' % value)
            return value

    def _get_value(self):
        assert self._lock
        try:
            with open(self._filename, 'r') as f_obj:
                counter = f_obj.read().strip()
            if counter and counter.isdigit():
                return int(counter)
            else:
                return 0
        except IOError as error:
            if not error.errno == errno.ENOENT:
                raise
            return 0

    def __enter__(self):
        self._lock = FLock(self._filename + '.lock')
        self._lock.acquire()

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._lock.release()
        self._lock = None

