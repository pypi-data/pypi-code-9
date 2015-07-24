try:
    import cPickle
except ImportError:
    import pickle as cPickle


__all__ = ['cachedfunc']


class cachedfunc(object):
    def __init__(self, f):
        self.f = f
        self.cache = {}
        self.__doc__ = f.__doc__

    def __call__(self, *args, **kwargs):
        hashed = cPickle.dumps([args, kwargs])
        try:
            return self.cache[hashed]
        except KeyError:
            result = self.f(*args, **kwargs)
            self.cache[hashed] = result
            return result

    def reset(self):
        self.cache = {}
