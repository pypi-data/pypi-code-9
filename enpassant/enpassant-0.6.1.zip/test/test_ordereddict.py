
# Test ordereddict sufficiently for its role as a Python 2.6 standin

import pytest
import sys
_PY26 = sys.version_info[:2] == (2, 6)
if _PY26:
    from enpassant.ordereddict import *


pytestmark = pytest.mark.skipif(not _PY26, reason='unnecessary')


def test_bad_constructor():
    with pytest.raises(TypeError):
        OrderedDict(1, 3, 4)


def test_delitem():
    od = OrderedDict()
    od['a'] = 4
    od['b'] = 55
    od['c'] = 323
    assert list(od.keys()) == list('abc')
    del od['b']
    assert list(od.keys()) == list('ac')


def test_reversed():
    od = OrderedDict()
    od['a'] = 4
    od['b'] = 55
    od['c'] = 323

    assert list(reversed(od)) == list('cba')


def test_eq():
    od = OrderedDict()
    od['a'] = 4
    od['b'] = 55
    od['c'] = 323

    od2 = OrderedDict()
    od2['a'] = 4
    od2['b'] = 55
    od2['c'] = 323

    assert od == od2

    od2['d'] = 42
    assert od != od2

    od3 = OrderedDict()
    od3['b'] = 55
    od3['a'] = 4
    od3['c'] = 323

    assert od != od3

    d3 = dict(od3.items())
    assert od == d3


def test_copy():
    od = OrderedDict()
    od['a'] = 4
    od['b'] = 55
    od['c'] = 323

    od2 = od.copy()

    assert od == od2
    assert od is not od2


def test_repr():
    od = OrderedDict()
    od['a'] = 4
    od['b'] = 55
    od['c'] = 323

    assert repr(od) == "OrderedDict([('a', 4), ('b', 55), ('c', 323)])"
    assert repr(OrderedDict()) == "OrderedDict()"


def test_fromkeys():
    od = OrderedDict.fromkeys(list('abc'), 33)
    assert list(od.keys()) == list('abc')
    assert list(od.values()) == [33] * 3


def test_popitem():
    od = OrderedDict()
    od['a'] = 4
    od['b'] = 55
    od['c'] = 323

    with pytest.raises(KeyError):
        OrderedDict().popitem()

    assert od.popitem(last=True) == ('c', 323)
    assert od.popitem(last=False) == ('a', 4)

def test_reduce():
    import pickle
    od = OrderedDict()
    od['a'] = 4
    od['b'] = 55
    od['c'] = 323

    od1 = pickle.loads(pickle.dumps(od))

    assert od == od1
