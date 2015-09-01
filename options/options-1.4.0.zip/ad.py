

from collections import OrderedDict


class attrdict(dict):
    """ A dictionary with attribute-style access. Maps attribute
        access to dictionary.

        >>> d = attrdict(a=1, b=2)
        >>> sorted(d.items())
        [('a', 1), ('b', 2)]
        >>> d.a
        1

        >>> d.c = 3
        >>> d.c
        3
        >>> d.d # doctest: +ELLIPSIS
        Traceback (most recent call last):
            ...
        AttributeError: ...
    """
    __slots__ = ()

    def __setattr__(self, key, value):
        return super(attrdict, self).__setitem__(key, value)

    def __getattr__(self, name):
        try:
            return super(attrdict, self).__getitem__(name)
        except KeyError:
            raise AttributeError(name)

class oattrdict(OrderedDict):

    def __init__(self, *args, **kwargs):
        OrderedDict.__init__(self)
        # self.update(**kwargs)

    def __setattr__(self, key, value):
        return OrderedDict.__setitem__(self, key, value)

    def __getattr__(self, name):
        try:
            return OrderedDict.__getitem__(self, name)
        except KeyError:
            raise AttributeError(name)

if __name__ == '__main__':
    a = oattrdict()
    a['a']  = 23
    print a
    print a.a
