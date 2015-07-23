import time


class Counter(object):
    """Time counter."""

    def __init__(self):
        """Sets start"""
        self._start = time.time()

    def begin(self):
        """Overwrites start"""
        self._start = time.time()

    def miliseconds(self):
        """Number of seconds from start"""
        return int(round((time.time() - self._start) * 1000))

    def as_string(self):
        """Number of seconds from start"""

        seconds = self.miliseconds() / 1000

        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        return "%d:%02d:%02d" % (h, m, s)