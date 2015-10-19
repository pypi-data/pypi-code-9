#!/usr/bin/env python

import pytest

from pygcrypt.types.sexpression import SExpression

def test_init(context):
    s_expr = SExpression(b'(test (a "123"))')
    assert repr(s_expr) == '(test \n (a "123")\n )\n'
    s_expr = SExpression(b'(test (a %d)(b %s)(c %b))', 10, 'Hello World', 3, b'123')
    assert repr(s_expr) == '(test \n (a "10")\n (b "Hello World")\n (c "123")\n )\n'
    s_expr2 = SExpression(s_expr.sexp)
    assert repr(s_expr2) == '(test \n (a "10")\n (b "Hello World")\n (c "123")\n )\n'

def test_getitem(context):
    s_expr = SExpression(b'(a "hello World")')
    assert print(s_expr['a']) == print("(hello World)")
    assert print(s_expr[0]) == print("(a)")
    assert print(s_expr[0:1]) == print(b'(a "hello World")')
    with pytest.raises(IndexError):
        s_expr[4]
        s_expr[-1]
        s_expr[3:5]

def test_carcdr(context):
    s_expr = SExpression(b'(tests (test1 "123") (test2 "456"))')
    assert str(s_expr.car) == '(tests)\n'
    assert str(s_expr.cdr) == '(\n (test1 "123")\n )\n'
    assert str(s_expr.cdr.car.car) == '(test1)\n'

def test_extract(context):
    s_expr = SExpression(b'(test (a "123") (b "-123"))')
    ret = s_expr.extract('a')
    assert ret['a'] == 3224115
    ret = s_expr.extract('-b', b'test')
    assert ret['b'] == 758198835
