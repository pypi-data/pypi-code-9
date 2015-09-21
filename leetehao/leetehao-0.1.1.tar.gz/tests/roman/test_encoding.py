# encoding: utf-8

import unittest

from leetehao.roman import encoding


class EncodingTestCase(unittest.TestCase):

    def test_coding(self):

        value, numerials = 2549, 'MMDXLIX'

        # normal case
        self.assertEqual(encoding.encode(value), numerials)
        self.assertEqual(encoding.decode(numerials), value)

        # exception
        self.assertRaises(encoding.RomanEncodeError, encoding.encode, 4999)
        self.assertRaises(encoding.RomanDecodeError, encoding.decode, "ABCDE")
