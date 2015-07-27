# -*- encoding: utf-8 -*-
import unittest
import six
from any2 import recursive_getattr


class Foo(object):
    def __init__(self, value):
        self.field1 = 'foo1_%s' % value
        self.field2 = 'foo2_%s' % value

class Bar(object):
    def __init__(self, value):
        self.field1 = 'bar1_%s' % value
        self.field2 = 'bar2_%s' % value
        self.foo = Foo(value)

class Dummy(object):
    def __init__(self, value):
        self.field1 = 'dummy1_%s' % value
        self.field2 = 'dummy2_%s' % value
        self.bar = Bar(value)


class TestAny2(unittest.TestCase):

    def test_001_firstlevel_field(self):
        dummy = Dummy('r1')
        res1 = recursive_getattr(dummy, 'field1')
        res2 = recursive_getattr(dummy, 'field2')

        assert res1 == 'dummy1_r1'
        assert res2 == 'dummy2_r1'

    def test_002_secondlevel_field(self):
        dummy = Dummy('r2')
        res1 = recursive_getattr(dummy, 'bar.field1')
        res2 = recursive_getattr(dummy, 'bar.field2')

        assert res1 == 'bar1_r2'
        assert res2 == 'bar2_r2'

    def test_003_thirdlevel_field(self):
        dummy = Dummy('r3')
        res1 = recursive_getattr(dummy, 'bar.foo.field1')
        res2 = recursive_getattr(dummy, 'bar.foo.field2')

        assert res1 == 'foo1_r3'
        assert res2 == 'foo2_r3'

    def test_004_missing_field_wdot(self):
        dummy = Dummy('r3')
        res1 = recursive_getattr(dummy, 'bar.foo.field1')
        res2 = recursive_getattr(dummy, 'bar.foo.XX.field2', default_value=42)

        assert res1 == 'foo1_r3'
        assert res2 == 42

    def test_004_missing_field_wodot(self):
        dummy = Dummy('r3')
        res1 = recursive_getattr(dummy, 'bar.foo.field1')
        res2 = recursive_getattr(dummy, 'XX', default_value=56)

        assert res1 == 'foo1_r3'
        assert res2 == 56
