# encoding: utf-8

import unittest
import random
import string

from leetehao.leet import encoding


class EncodingTestCase(unittest.TestCase):

    def test_coding(self):

        message, encoded = 'hello world', '}{[-[_[_()  vv()[z[_|)'

        # normal case
        self.assertEqual(encoding.encode(message), encoded)
        self.assertEqual(encoding.decode(encoded), message.upper())

        # random test
        for i in range(100):
            msg = ''.join([random.choice('{a}{n} '.format(
                a=string.ascii_letters, n=string.digits)) for i in range(30)])

            self.assertEqual(encoding.decode(encoding.encode(msg)), msg.upper())

    def test_class(self):

        message, encoded = 'hello world', '}{[-[_[_()  vv()[z[_|)'

        en, de = encoding.LeetEncoder(), encoding.LeetDecoder()

        self.assertEqual(en.encode(message), encoded)
        self.assertEqual(de.decode(encoded), message.upper())

        # random test
        for i in range(100):
            msg = ''.join([random.choice('{a}{n} '.format(
                a=string.ascii_letters, n=string.digits)) for i in range(30)])

            self.assertEqual(encoding.decode(encoding.encode(msg)), msg.upper())

    def test_coding_one(self):

        message, encoded = 'hello world', '#&ll0_w02l)'

        # normal case
        self.assertEqual(
            encoding.encode(message, mapping=encoding.constants.LEET_ENCODE_ONE), encoded)
        self.assertEqual(
            encoding.decode(encoded, mapping=encoding.constants.LEET_DECODE_ONE), message.upper())

        # random test
        for i in range(100):
            msg = ''.join([random.choice('{a}{n} '.format(
                a=string.ascii_letters, n=string.digits)) for i in range(30)])

            self.assertEqual(
                encoding.decode(
                    encoding.encode(msg, mapping=encoding.constants.LEET_ENCODE_ONE),
                    mapping=encoding.constants.LEET_DECODE_ONE),
                msg.upper()
            )
