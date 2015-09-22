'''dhp data structures'''


class DictDot(dict):
    """ A dictionary that provides dot-style access"""
    def __init__(self, *args, **kwargs):
        if args:
            dct = args[0]
        else:
            dct = {}
        if kwargs:
            dct.update(kwargs)
        for key in dct:
            if type(dct[key]) is dict:
                dct[key] = self.__class__(dct[key])
        super(DictDot, self).__init__(dct)

    def __getattr__(self, key):
        try:
            return object.__getattribute__(self, key)
        except AttributeError:
            try:
                return self[key]
            except KeyError:
                raise AttributeError(key)

    def __setattr__(self, key, val):
        if type(val) is dict:
            val = self.__class__(val)
        try:
            object.__getattribute__(self, key)
        except AttributeError:
            try:
                self[key] = val
            except:
                raise AttributeError(key)
        else:
            object.__setattr__(self, key, val)

    def __delattr__(self, key):
        try:
            object.__getattribute__(self, key)
        except AttributeError:
            try:
                del self[key]
            except KeyError:
                raise AttributeError(key)
        else:
            object.__delattr__(self, key)
