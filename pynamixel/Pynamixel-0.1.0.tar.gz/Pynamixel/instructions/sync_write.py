# coding: utf8

# Copyright 2015 Vincent Jacques <vincent@vincent-jacques.net>

import itertools
import unittest


class SyncWrite(object):
    """
    @todoc
    """
    code = 0x83
    # No response_class because SyncWrite must be broadcasted

    def __init__(self, address, data):
        self.__address = address
        self.__data = data

    @property
    def parameters(self):
        length = None
        for data in self.__data.itervalues():
            # @todo Remove asserts (everywhere, not just here) and raise appropriate exceptions
            assert length is None or len(data) == length
            length = len(data)
        assert length is not None
        return [self.__address, length] + list(itertools.chain.from_iterable([ident] + data for ident, data in sorted(self.__data.iteritems())))


class SyncWriteTestCase(unittest.TestCase):
    def test_parameters(self):
        w = SyncWrite(0x1E, {0: [0x10], 1: [0x20]})
        self.assertEqual(w.parameters, [0x1E, 0x01, 0x00, 0x10, 0x01, 0x20])
