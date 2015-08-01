import sys as _sys


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

    @property
    def step(self):
        """
        The current step.
        """
        return self._step

    @step.setter
    def step(self, step):
        if step > self._total:
            step = self._total
        self._step = step
        bartext = '#'*round(step/self._total * self._length) + ' '*round((self._total-step)/self._total * self._length)
        text = '\r\033[1AOn step {} of {}:\n[ {} ]'.format(self._step, self._total, bartext)
        _sys.stdout.write(text)
        _sys.stdout.flush()
        # print(text)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        text = '\r\033[K\033[1A\033[K'
        _sys.stdout.write(text)
        _sys.stdout.flush()
