# coding: utf8

# Copyright 2015 Vincent Jacques <vincent@vincent-jacques.net>

import unittest


class WriteDataResponse(object):
    """
    @todoc
    """
    def __init__(self, parameters):
        assert len(parameters) == 0


class WriteData(object):
    """
    @todoc
    """
    code = 0x03
    response_class = WriteDataResponse

    def __init__(self, address, data):
        self.__address = address
        if isinstance(data, int):
            data = [data]
        self.__data = data

    @property
    def parameters(self):
        return [self.__address] + self.__data


class WriteDataTestCase(unittest.TestCase):
    def test_parameters_with_array_data(self):
        w = WriteData(0, [1, 2, 3])
        self.assertEqual(w.parameters, [0, 1, 2, 3])

    def test_parameters_with_int_data(self):
        w = WriteData(0, 1)
        self.assertEqual(w.parameters, [0, 1])
