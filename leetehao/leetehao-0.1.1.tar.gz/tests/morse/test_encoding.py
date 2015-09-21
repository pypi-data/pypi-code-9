# encoding: utf-8

import unittest
import random
import string

from leetehao.morse import encoding


class EncodingTestCase(unittest.TestCase):

    def test_coding(self):

        message, encoded = 'hello world', '.... . .-.. .-.. --- / .-- --- .-. .-.. -..'

        # normal case
        self.assertEqual(encoding.encode(message), encoded)
        self.assertEqual(encoding.decode(encoded), message.upper())

        # encode error
        msg = '錯'
        self.assertRaises(encoding.MorseEncodeError, encoding.encode, msg)

        # decode error
        msg = '.--------------.'
        self.assertRaises(encoding.MorseDecodeError, encoding.decode, msg)

        # mass random test
        for i in range(100):
            msg = ''.join([random.choice('{a}{d}'.format(
                a=string.ascii_letters, d=string.digits)) for i in range(30)]
            )
            self.assertEqual(encoding.decode(encoding.encode(msg)), msg.upper())

    def test_class(self):

        message, encoded = 'hello world', '.... . .-.. .-.. --- / .-- --- .-. .-.. -..'
        en, de = encoding.MorseEncoder(), encoding.MorseDecoder()

        # normal case
        self.assertEqual(en.encode(message), encoded)
        self.assertEqual(de.decode(encoded), message.upper())
