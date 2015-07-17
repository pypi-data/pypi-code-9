
import pytest
from intspan import *
from intspan import ParseError

def test_basic():
    s = intspanlist()
    tests = ['', '1','1-2', '1-3,9-10', '1-3,14,29,92-97']
    for t in tests:
        s = intspanlist(t)
        assert str(s) == t

def test_parse_error():
    with pytest.raises(ParseError):
        s = intspanlist('7*99')
    with pytest.raises(ParseError):
        s = intspanlist('1-4,5-')

def test_negatives():
    assert list(intspanlist('-2')) == [-2]
    assert list(intspanlist('-2-1')) == [-2, -1, 0, 1]
    assert list(intspanlist('-2--1')) == [-2, -1]

def test_contains():
    s = intspanlist()
    assert 1 not in s
    assert 100 not in s
    assert 0 not in s

    t = intspanlist('1,10')
    assert 1 in t
    assert 10 in t
    assert 0 not in t
    assert 2 not in t

def test_equals():
    s = intspanlist('1,3,5,7,9')
    assert s == [1,3,5,7,9]

def test_copy():
    t = intspanlist('1,10,1-10')
    tt = t.copy()
    assert type(tt) == type(t)
    assert t == tt
    assert t is not tt


def test_len():
    s = intspanlist('1,2,3,5,8,13,21')
    assert len(s) == 7
    s.pop()
    assert len(s) == 6
    assert len(intspanlist()) == 0
    assert len(intspanlist('')) == 0
    assert len(intspanlist(1)) == 1
    assert len(intspanlist('1')) == 1
    assert len(intspanlist([1,4])) == 2
    assert len(intspanlist('1,4')) == 2

#def test_pop():
#    s = intspan('100-110')
#    assert s.pop() == 100
#    assert s.pop() == 101
#    assert s.pop() == 102
#    assert s.pop() == 103
#    assert s.pop() == 104
#    assert s.pop() == 105
#    assert s == intspan('106-110')
#
#    s = intspan('1-2')
#    assert s.pop() == 1
#    assert s.pop() == 2
#    with pytest.raises(KeyError):
#        s.pop()
#
def test_ranges_basic():
    assert intspanlist().ranges() == []
    assert intspanlist('2').ranges()   == [ (2,2) ]
    assert intspanlist('1-3').ranges() == [ (1,3) ]
    assert intspanlist('1-3,5-6').ranges() == [ (1,3), (5,6) ]

#def test_from_range():
#    assert intspan.from_range(1,3) == intspan('1-3')
#    assert intspan.from_range(2,44) == intspan('2-44')
#
#def test_from_ranges():
#    assert intspan.from_ranges([ (1,3), (5,6) ]) == intspan('1-3,5-6')
#    assert intspan.from_ranges([ (1,3) ]) == intspan('1-3')
#    assert intspan.from_ranges([ (2,2) ]) == intspan('2')
#    assert intspan.from_ranges([]) == intspan()
#
#def test_complement():
#    s = intspan('1,3,5-9')
#    assert s.complement() == intspan('2,4')
#    assert s.complement(high=10) == intspan('2,4,10')
#    assert s.complement(high=14) == intspan('2,4,10-14')
#    assert s.complement(low=0) == intspan('0,2,4')
#    assert s.complement(low=0, high=14) == intspan('0,2,4,10-14')
#
#    assert s.complement(-2, 5) == intspan('-2,-1,0,2,4')
#
#    items = intspan('1-3,5,7-9,10,21-24')
#    assert items.complement() == intspan('4,6,11-20')
#    assert items.complement(high=30) == intspan('4,6,11-20,25-30')
#
#    with pytest.raises(ValueError):
#        intspan().complement()
#        # cannot get the complement of an empty set
#
#def test_repr_and_str():
#    s = intspan('10-20,50-55')
#    s.add(9)
#    s.discard('15-40')
#    assert str(s) == '9-14,50-55'
#    assert repr(s) == "intspan('" + str(s) + "')"


def test_spanlist():
    assert spanlist() == []
    assert spanlist(1) == [1]
    assert spanlist([33,1,3,4]) == [33,1,3,4]
    assert spanlist([33,1,3,33,4]) == [33,1,3,4]
    assert spanlist('') == []
    assert spanlist('1') == [1]
    assert spanlist('33,1,3,4') == [33,1,3,4]
    assert spanlist('33,1,3,33,4') == [33,1,3,4]
    assert spanlist('4,1-5') == [4,1,2,3,5]
    assert spanlist('4,1-5,5') == [4,1,2,3,5]
    assert spanlist('4,1-5,5,5,1') == [4,1,2,3,5]

def test_constructor():
    assert intspanlist() == []
    assert intspanlist(1) == [1]
    assert intspanlist([33,1,3,4]) == [33,1,3,4]
    assert intspanlist([33,1,3,33,4]) == [33,1,3,4]
    assert intspanlist('') == []
    assert intspanlist('1') == [1]
    assert intspanlist('33,1,3,4') == [33,1,3,4]
    assert intspanlist('33,1,3,33,4') == [33,1,3,4]
    assert intspanlist('4,1-5') == [4,1,2,3,5]
    assert intspanlist('4,1-5,5') == [4,1,2,3,5]
    assert intspanlist('4,1-5,5,5,1') == [4,1,2,3,5]

def test_repr():
    assert repr(intspanlist()) == "intspanlist('')"
    assert repr(intspanlist(1)) == "intspanlist('1')"
    assert repr(intspanlist([33,1,3,4])) == "intspanlist('33,1,3-4')"
    assert repr(intspanlist([33,1,3,33,4])) == "intspanlist('33,1,3-4')"
    assert repr(intspanlist('')) == "intspanlist('')"
    assert repr(intspanlist('1')) == "intspanlist('1')"
    assert repr(intspanlist('33,1,3,4')) == "intspanlist('33,1,3-4')"
    assert repr(intspanlist('33,1,3,33,4')) == "intspanlist('33,1,3-4')"
    assert repr(intspanlist('4,1-5')) == "intspanlist('4,1-3,5')"
    assert repr(intspanlist('4,1-5,5')) == "intspanlist('4,1-3,5')"
    assert repr(intspanlist('4,1-5,5,5,1')) == "intspanlist('4,1-3,5')"

def test_ranges():
    assert intspanlist('').ranges() == []
    assert intspanlist('1-14').ranges() == [(1, 14)]
    assert intspanlist('9,4,1-3,5-8,10-14').ranges() == [(9, 9), (4, 4), (1, 3), (5, 8), (10, 14)]
