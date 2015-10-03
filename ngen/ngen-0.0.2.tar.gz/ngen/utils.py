from functools import wraps
from twisted.internet import reactor


def threaded(func):
    """
        method decorator that will run the wrapped function in a thread
        managed by twisted's reactor
    """
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        reactor.callInThread(func, self, *args, **kwargs)
    return wrapper
