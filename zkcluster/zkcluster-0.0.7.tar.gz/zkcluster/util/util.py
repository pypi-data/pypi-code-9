import threading
import json


def json_dumps(text):
    return json.dumps(text)


def json_loads(text):
    return json.loads(text)


class memoized_property(object):
    """A read-only @property that is only evaluated once."""

    def __init__(self, fget, doc=None):
        self.fget = fget
        self.__doc__ = doc or fget.__doc__
        self.__name__ = fget.__name__

    def __get__(self, obj, cls):
        if obj is None:
            return self
        obj.__dict__[self.__name__] = result = self.fget(obj)
        return result

    def _reset(self, obj):
        memoized_property.reset(obj, self.__name__)

    @classmethod
    def reset(cls, obj, name):
        obj.__dict__.pop(name, None)


def periodic_timer(interval, start=0):
    """return True only every 'interval' seconds."""

    last_check = [start]

    def reset(now):
        last_check[0] = now

    def check(now):
        if now - last_check[0] > interval:
            last_check[0] = now
            return True
        else:
            return False
    check.last_check = last_check
    check.interval = interval
    check.reset = reset
    return check


class Startable(object):
    _started = False
    _starting = False

    @memoized_property
    def _startup_mutex(self):
        return threading.Lock()

    def start(self):
        if self._started:
            return
        with self._startup_mutex:
            if self._started:
                return

            self._starting = True
            try:
                self.do_start()
            finally:
                self._started = True
                self._starting = False

    def stop(self):
        if not self._started:
            return
        with self._startup_mutex:
            if not self._started:
                return

            try:
                self.do_stop()
            finally:
                self._started = False

    def do_start(self):
        raise NotImplementedError()

    def do_stop(self):
        raise NotImplementedError()



