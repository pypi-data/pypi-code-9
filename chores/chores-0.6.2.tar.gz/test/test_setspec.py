
from chores.setspec import *


def test_splitwords():
    assert splitwords("a|b") == ['a', 'b']
    assert splitwords("a|b|c") == ['a', 'b', 'c']
    assert splitwords(" a   | b ") == ['a', 'b']
    assert splitwords(" a   | b | c ") == ['a', 'b', 'c']
    assert splitwords(" a   | b |c") == ['a', 'b', 'c']

def test_set2list():

    assert spec2list("a|b") == (['a', 'b'], [])
    assert spec2list("done|partial") == (['done', 'partial'], [])
    assert spec2list("done|previous") == (['done', 'previous'], [])
    assert spec2list("^partial|previous") == ([], ['partial', 'previous'])
    assert spec2list(" ^ partial | previous ") == ([], ['partial', 'previous'])
