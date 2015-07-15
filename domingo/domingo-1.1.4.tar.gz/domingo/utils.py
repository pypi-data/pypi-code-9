import calendar
import random
from datetime import datetime


def hash96(seed=None):
    """
    Returns a 24 hexidecimal hash of the seed given. If no seed is given then
    it returns a random hash based on the internal clock.
    ipython:
        %timeit hash96('hello')
        10000 loops, best of 3: 21.8 microseconds per loop on a macbook air
    N.B. This function has been checked across OS platforms and cpus... yeah
    it's python...
    """

    def _hash(bits=96):
        assert bits % 8 == 0
        required_length = bits / 8 * 2
        s = hex(random.getrandbits(bits)).lstrip('0x').rstrip('L')
        if len(s) < required_length:
            return _hash(bits)
        else:
            return s
    random.seed(seed)

    return _hash()


class ClassPropertyDescriptor(object):

    def __init__(self, fget, fset=None):
        self.fget = fget
        self.fset = fset

    def __get__(self, obj, cls=None):
        if cls is None:
            cls = type(obj)
        return self.fget.__get__(obj, cls)()

    def __set__(self, obj, value):
        if not self.fset:
            raise AttributeError("can't set attribute")
        type_ = type(obj)
        return self.fset.__get__(obj, type_)(value)

    def setter(self, func):
        if not isinstance(func, (classmethod, staticmethod)):
            func = classmethod(func)
        self.fset = func
        return self


def classproperty(func):
    if not isinstance(func, (classmethod, staticmethod)):
        func = classmethod(func)

    return ClassPropertyDescriptor(func)


utcnow = datetime.utcnow


def utcstamp(
        timestamp=None,
        utcnow=datetime.utcnow,
        utcfromtimestamp=datetime.utcfromtimestamp,
        timegm=calendar.timegm
    ):
    "returns seconds since epoch in utc time [float]"
    if isinstance(timestamp, datetime):
        now = timestamp
    else:
        if not timestamp or timestamp is None:
            now = utcnow()
        else:
            now = utcfromtimestamp(float(timestamp))
    epoch_time = timegm(now.utctimetuple())
    return epoch_time + now.microsecond / 1000000.
