import unittest

from libsousou import iana


class PrivateEnterpriseNumberTestCase(unittest.TestCase):

    def test_pack_pen_value(self):
        # Create a PrivateEnterpriseNumber instance and pack an
        # identifier.
        pen = iana.PrivateEnterpriseNumber(1)
        ident1 = 2
        value = pen.pack(ident1)

        # Unpack the value.
        unpacked_pen, ident2 = iana.PrivateEnterpriseNumber.unpack(value)
        self.assertEqual(ident1, ident2)
        self.assertEqual(pen, unpacked_pen)


if __name__ == '__main__':
    unittest.main()
