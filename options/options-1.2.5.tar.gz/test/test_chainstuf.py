
from options.chainstuf import chainstuf
import pytest


def test_one():
    base = dict(a=1, b=2)
    top = dict(a=5)
    chain = chainstuf(top, base)

    assert chain['a'] == 5
    assert chain.a == 5
    assert chain['b'] == 2
    assert chain.b == 2

    with pytest.raises(KeyError):
        chain['c']

    with pytest.raises(KeyError):
        chain.c

    assert chain.__getattr__ is not None