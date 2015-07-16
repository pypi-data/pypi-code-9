# Tests for the transforms init module
import unittest
from Products.PortalTransforms.data import datastream
from psj.policy.transforms import OOOTransformBase


class FakeContext(object):
    some_key = 'foo'


class OOOTransformBaseTests(unittest.TestCase):

    def test_get_cache_key(self):
        # OOOTransformBase instances can get cache keys
        base = OOOTransformBase()
        context = FakeContext()
        stream = datastream('mystream')
        stream.context = context
        result = base.get_cache_key('some_key', stream)
        assert result == 'foo'

    def test_get_cache_key_no_context(self):
        # objects w/o context are ignored
        base = OOOTransformBase()
        result = base.get_cache_key('invalid-key', None)
        assert result is None

    def test_get_cache_key_no_key(self):
        # contexts w/o given key result in ``None``
        base = OOOTransformBase()
        context = FakeContext()
        stream = datastream('mystream')
        stream.context = context
        result = base.get_cache_key('invalid-key', stream)
        assert result is None
