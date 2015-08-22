from withref import ref
from stuf import stuf
import pytest

def test_basic():
    a = stuf({ 'b': { 'c': { 'c1': 1 }, 'd': 44.1 } })

    assert a.b.c.c1 == 1

    with ref(a.b.c) as c:
        c.c1 = 99
        assert c.c1 == 99
        assert a.b.c.c1 == 99

    a_ideal = stuf({'b': {'c': {'c1': 99}, 'd': 44.1}})
    assert a == a_ideal

def test_array_style():

    a = stuf({ 'b': { 'c': { 'c1': 1 }, 'd': 44.1 } })

    with ref(a['b']['c']) as cc:
        cc['c1'] = 99

    a_ideal = stuf({'b': {'c': {'c1': 99}, 'd': 44.1}})
    assert a == a_ideal


def test_limitations():

    a = stuf({ 'b': { 'c': { 'c1': 1 }, 'd': 44.1 } })

    with ref(a.b.c) as c:
        c.c1 = 99

    with ref(a.b.c.c1) as c1:
        assert c1 == 99     # so far, so good!
        c1 = 12345
        assert c1 == 12345  # still good!

        # but c1 is just a local value there, and not the end value
        assert a.b.c.c1 == 99   # with heavy heart

def test_string():
    with ref("this is a string"[0:4]) as t:
        assert t == "this"


def test_exception():
    # Ensure exceptions propagete through the withref usage

    with pytest.raises(RuntimeError):
        with ref("word"[0:2]) as t:
            assert t == "wo"
            raise RuntimeError('yo')
