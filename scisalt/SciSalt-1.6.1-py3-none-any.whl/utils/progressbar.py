import sys as _sys
import time as _time
import datetime as _dt


class progressbar(object):
    """
    .. versionadded:: 1.3

    Creates a progress bar with a number of steps *total* and a length of *length*.
    """
    def __init__(self, total, length=20):
        print('')
        self._step   = 0
        self._total  = total
        self._length = length
        self._timestamp = None
        self._timestart = None

    @property
    def step(self):
        """
        The current step.
        """
        return self._step

    @step.setter
    def step(self, step):
        lasttime = self._timestamp
        self._timestamp = _time.perf_counter()
        if lasttime is not None:
            dt = self._timestamp-lasttime
            time_remain = (self._total - step - 1) * dt
            remain_str = ', {} remain'.format(str(_dt.timedelta(seconds=time_remain)))
        else:
            remain_str = ''

        if self._timestart is None:
            self._timestart = self._timestamp
            elapsed_str = ''
        else:
            elapsed = self._timestamp-self._timestart
            elapsed_str = ', {} elapsed'.format(str(_dt.timedelta(seconds=elapsed)))

        if step > self._total:
            step = self._total
        self._step = step
        step = step - 1
        bartext = '#'*round(step/self._total * self._length) + ' '*round((self._total-step)/self._total * self._length)
        text = '\r\033[1AOn step {} of {} ({:0.1f}% completed{}{}):\n[ {} ]'.format(self._step, self._total, 100.0*step/self._total, remain_str, elapsed_str, bartext)
        _sys.stdout.write(text)
        _sys.stdout.flush()
        # print(text)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        text = '\r\033[K\033[1A\033[K'
        _sys.stdout.write(text)
        _sys.stdout.flush()
