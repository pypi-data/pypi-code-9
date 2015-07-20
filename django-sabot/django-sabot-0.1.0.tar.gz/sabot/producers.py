from __future__ import unicode_literals

import datetime
from random import randint

__all__ = (
    'CountErrorProducer', 'RandomErrorProducer', 'TimeDeltaErrorProducer'
)


class ErrorProducer(object):
    """
    Error producer base class
    """

    def check(self, *args, **kwargs):
        raise NotImplementedError


class RandomErrorProducer(ErrorProducer):
    """
    Error produce class that raises the passed exception when a random number
    between `low` and `high` equals `low`
    """

    def __init__(self, exception, low, high):
        self.exception = exception
        self.low = low
        self.high = high

    def check(self, *args, **kwargs):
        if randint(self.low, self.high) == self.low:
            raise self.exception('Random number matched target trigger')


class CountErrorProducer(ErrorProducer):
    """
    Error produce class that raises the passed exception when the executed
    `number` amount of times.
    """

    def __init__(self, exception, number, reset=False):
        self.exception = exception
        self.number = number
        self._count = 0
        self.reset = reset

    def check(self, *args, **kwargs):
        self._count += 1
        if self._count >= self.number:
            if self.reset:
                self._count = 0

            raise self.exception('Count reached')


class TimeDeltaErrorProducer(ErrorProducer):
    """
    Error produce class that raises the passed exception when the `timedelta`
    time has passed since the class instantiation.
    """

    def __init__(self, exception, timedelta, reset=False):
        self.exception = exception
        self.timedelta = datetime.timedelta(**timedelta)
        self._start = datetime.datetime.now()
        self.reset = reset

    def check(self, *args, **kwargs):
        if datetime.datetime.now() > self._start + self.timedelta:
            if self.reset:
                self._start = datetime.datetime.now()
            raise self.exception('Time delta reached')
