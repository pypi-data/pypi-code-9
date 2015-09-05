# coding: utf8

# Copyright 2015 Vincent Jacques <vincent@vincent-jacques.net>

import unittest


class ReadDataResponse(object):
    """
    @todoc
    """
    def __init__(self, parameters):
        self.data = parameters


class ReadData(object):
    """
    @todoc
    """
    code = 0x02
    response_class = ReadDataResponse

    def __init__(self, address, length=1):
        self.__address = address
        self.__length = length

    @property
    def parameters(self):
        return [self.__address, self.__length]


class ReadDataTestCase(unittest.TestCase):
    def test_parameters_without_length(self):
        r = ReadData(42)
        self.assertEqual(r.parameters, [42, 1])

    def test_parameters_with_length(self):
        r = ReadData(42, 3)
        self.assertEqual(r.parameters, [42, 3])

    def test_response(self):
        r = ReadDataResponse([34, 56])
        self.assertEqual(r.data, [34, 56])
