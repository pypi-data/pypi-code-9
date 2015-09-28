'''dhp data structures'''


class DictDot(dict):
    """A subclass of Python's dictionary that provides dot-style access.

    Nested dictionaries are recursively converted to DictDot.  There are a
    number of similar libraries on PyPI.  However, I feel this one does just
    enough to make things work as expected without trying to do too much.

    Example::

        dicdot = DictDot({
            'foo': {
                'bar': {
                    'baz': 'hovercraft',
                    'x': 'eels'
                }
            }
        })
        assert dicdot.foo.bar.baz == 'hovercraft'
        assert dicdot['foo'].bar.x == 'eels'
        assert dicdot.foo['bar'].baz == 'hovercraft'
        dicdot.bouncy = 'bouncy'
        assert dictdot['bouncy'] == 'bouncy'

    DictDot raises an AttributeError when you try to read a non-existing
    attribute while also allowing you to create new key/value pairs using
    dot notation.

    DictDot also supports keyword arguments on instantiation and is built to
    be subclass'able.
    """
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
            # try:
            self[key] = val
            # except:
            #     raise AttributeError(key)
        # else:
        #     object.__setattr__(self, key, val)

    def __delattr__(self, key):
        try:
            object.__getattribute__(self, key)
        except AttributeError:
            try:
                del self[key]
            except KeyError:
                raise AttributeError(key)
        # else:
        #     object.__delattr__(self, key)
