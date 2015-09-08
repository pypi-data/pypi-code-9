import inspect


class Eq(object):
    id = {}
    params = {}
    eq_registry = {}

    def __init__(self, num=None):
        if num:
            if isinstance(num, int):
                self.num = num
            else:
                raise TypeError(u'num can be only int')
        else:
            if Eq.id:
                self.num = max(Eq.id.keys(), key=int) + 1
            else:
                self.num = 1

    def __call__(self, fn):
        def wrapped(*args, **kwargs):
            Eq.params[fn.__name__] = fn(*args, **kwargs)
            return Eq.params[fn.__name__]

        Eq.eq_registry[fn.__name__] = {}
        Eq.eq_registry[fn.__name__]['args'] = inspect.getargspec(fn).args
        Eq.eq_registry[fn.__name__]['fn'] = wrapped

        Eq.id[self.num] = fn.__name__

        return Eq.eq_registry[fn.__name__]['fn']
