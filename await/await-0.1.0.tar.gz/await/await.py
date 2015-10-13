from functools import wraps
import collections

from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import dill


class Awaitable(object):
    """
    Syntactic wrapper for Futures returned by Executors
    """

    def __init__(self, future, timeout):
        self.future = future
        self.timeout = timeout

    def await(self):
        serialized_result = self.future.result(self.timeout)
        return dill.loads(serialized_result)

    def result(self, *args, **kwargs):
        return self.await(*args, **kwargs)


class Serialized(object):
    """
    Serializes functions and their arguments using dill
    """
 
    def __init__(self, f, *args, **kwargs):
        self.f = dill.dumps(f)
        self.args = map(dill.dumps, args)
        self.kwargs = {k: dill.dumps(v) for k, v in kwargs.iteritems()}

    def __call__(self):
        f = dill.loads(self.f)
        args = map(dill.loads, self.args)
        kwargs = {k: dill.loads(v) for k, v in self.kwargs.iteritems()}
        return dill.dumps(f(*args, **kwargs))


def async(n, base_type, timeout=None):
    def decorator(f):
        if isinstance(n, int):
            pool = base_type(n)
        elif isinstance(n, base_type):
            pool = n
        else:
            raise TypeError(
                "Invalid type: %s"
                % str(base_type)
            )
        @wraps(f)
        def wrapped(*args, **kwargs):
            return Awaitable(
                pool.submit(
                    Serialized(f, *args, **kwargs), 
                ),
                timeout=timeout
            )
        return wrapped
    return decorator


def threads(n=None, timeout=None):
    return async(n, ThreadPoolExecutor, timeout)


def processes(n=None, timeout=None):
    return async(n, ProcessPoolExecutor, timeout)
