
"""
Minimal attribute-accessible version of OrderedDict.
Still require minmal version of ChainMap as attribute-accessible
dict. Reluctantly implementing these becasue of
isseus faced with orderedstuf
"""

from collections import OrderedDict

class aodict(object):
    def __init__(self, *args, **kwargs):
        odict = OrderedDict()
        super(aodict, self).__setattr__('_odict', odict)
        # update *args and **kwargs
        for arg in args:
            for k, v in arg:
                odict[k] = v
        odict.update(kwargs)

    def __getattr__(self, key):
        odict = super(aodict, self).__getattribute__('_odict')
        if key in odict:
            return odict[key]
        return super(aodict, self).__getattribute__(key)
        # not sure about this very last statement

    def __setattr__(self, key, val):
        self._odict[key] = val

    def __delattr__(self, key):
        del self._odict[name]

    def __getitem__(self, key):
        odict = super(aodict, self).__getattribute__('_odict')
        return odict[key]

    def __setitem__(self, key, val):
        self._odict[key] = val

    def __delitem__(self, key):
        del self._odict[name]

    def keys(self):
        return self._odict.keys()

    def items(self):
        return self._odict.items()

    def values(self):
        return self._odict.values()

    def update(self, d):
        self._odict.update(d)

    def __len__(self):
        return len(self._odict)

    def __contains__(self, key):
        return key in self._odict

    def __iter__(self):
        return iter(self._odict)

    def clear(self):
        self._odict.clear()

    def copy(self):
        return self.__class__(self.items())

    @classmethod
    def fromkeys(cls, seq, value=None):
        d = self.__class__()
        for k in seq:
            d[k] = value
        return d

    def get(self, key, default):
        return self._odict.get(key, default)

    def setdefault(self, key, default):
        return self._odict.setdefault(key, default)

    def pop(self, key, default=None):
        return self._odict.pop(key, default)

    def popitem(self):
        return self._odict.popitem()

    def __repr__(self):
        clsname = self.__class__.__name__
        odict = super(aodict, self).__getattribute__('_odict')
        guts =  ', '.join("{0}={1!r}".format(k, v) for k,v in odict.items())
        return "{0}({1})".format(clsname, guts)

    @property
    def __dict__(self):
        return self._odict
        # Not sure about this one

    def __setstate__(self, state): # Support copy.copy
        super(aodict, self).__setattr__( '_odict', OrderedDict() )
        self._odict.update( state )
        # not sure about this one

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)


if __name__ == '__main__':
    a = aodict(a=22, b=11)
    assert a.a == 22
    assert a.b == 11
    a['a']  = 23
    a['b'] = 44
    assert a['a'] == 23
    assert a.a == 23
    assert a['b'] == 44
    assert a.b == 44
    a.c  = 99
    assert a.c == 99

    b = aodict(a=22, b=aodict(c=233))
    assert b.b.c == 233

    oc = [('a', 1), ('b', 2), ('c', 3), ('d', 4)]
    o = aodict(oc)
    assert list(o.keys()) == 'a b c d'.split()
