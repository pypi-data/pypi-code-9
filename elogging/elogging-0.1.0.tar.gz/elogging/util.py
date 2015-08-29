
import time

def profile(f):
    """Function profiling decorator.

    It calculates the consumed time for every function call. Besides,
    stats information is 'stored' in the wrapper using currying technique.

    For example, 

    >>> @profile
    ... def foo():
    ...    sleep(3)

    >>> foo()
    >>> print foo.stats()
    3.00119876862 
    """

    _stats = 0.0

    def wrapper(*args, **kwargs):
        global _stats
        s = time.time()
        res = f(*args, **kwargs)
        e = time.time()
        _stats = e - s
        return res
        
    def stats():
        global _stats
        return _stats

    wrapper.stats = stats
    return wrapper

