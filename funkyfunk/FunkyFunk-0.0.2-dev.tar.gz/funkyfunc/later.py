from threading import Lock, Thread


__all__ = [
    'getbacktome',
]


class NotPublished(Exception):
    pass


class FutureResult(object):
    def __init__(self):
        self.lock = Lock()
        self._value = None
        self._value_published = False

    def _publish(self, value):
        with self.lock:
            self._value = value
            self._value_published = True

    @property
    def value(self):
        with self.lock:
            if self._value_published:
                return self._value
            raise NotPublished()

    @property
    def published(self):
        with self.lock:
            return self._value_published


def getbacktome(f):
    '''
    >>> @getbacktome
    ... def slow_function(foo, bar):
    ...     import time; time.sleep(3)
    ...     return foo * bar
    ...
    >>> val = slow_function(2, 2)
    >>> val.published
    False
    >>> import time; time.sleep(1)
    >>> val.published
    False
    >>> time.sleep(2.1)
    >>> val.published
    True
    >>> val.value
    4
    '''
    def _wrapped_with_callback(*args, **kwargs):
        future = kwargs.pop('__future_result_obj')
        return_val = f(*args, **kwargs)
        future._publish(return_val)

    def _start_thread_wrapper(*args, **kwargs):
        future = FutureResult()
        kwargs['__future_result_obj'] = future
        Thread(
            target=_wrapped_with_callback,
            args=args,
            kwargs=kwargs
        ).start()
        return future

    return _start_thread_wrapper


if __name__ == '__main__':
    import doctest
    doctest.testmod()
