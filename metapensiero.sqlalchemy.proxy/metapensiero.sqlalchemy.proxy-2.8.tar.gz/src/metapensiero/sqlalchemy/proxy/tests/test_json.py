# -*- coding: utf-8 -*-
#:Progetto:  metapensiero.sqlalchemy.proxy -- Test JSON utils
#:Creato:    dom 07 apr 2013 15:22:57 CEST
#:Autore:    Lele Gaifax <lele@metapensiero.it>
#:Licenza:   GNU General Public License version 3 or later
#

from datetime import date, datetime, time
from decimal import Decimal

import pytest

from metapensiero.sqlalchemy.proxy.json import json2py, py2json


def test_date_jsonification():
    d = date(1968, 3, 18)
    assert json2py(py2json(d)) == d


def test_time_jsonification():
    t = time(10, 11, 12)
    assert json2py(py2json(t)) == t


def test_datetime_jsonification():
    dt = datetime(1968, 3, 18, 10, 10, 0)
    assert json2py(py2json(dt)) == dt


def test_decimal_jsonification():
    d = Decimal('3.1415926')
    assert json2py(py2json(d)) == d


def test_plain_strings():
    s = 'aa:bb:cc'
    assert json2py(py2json(s)) == s

    s = 'aaaa-bb-cc'
    assert json2py(py2json(s)) == s

    s = 'aaaa-bb-ccTdd:ee:ff'
    assert json2py(py2json(s)) == s


def test_unjsonable():
    class Foo(object):
        pass

    f = Foo()
    with pytest.raises(TypeError):
        py2json(f)
