import unittest

from libsousou import password


class PasswordTestCase(unittest.TestCase):

    def test_entropy_alpha(self):
        # The entropy of a raw password consisting of a single alphabetic
        # character is ~4.7.
        p = password.RawPassword('a')
        self.assertAlmostEqual(p.entropy, 4.7, 1)

    def test_entropy_numeric(self):
        # The entropy of a raw password consisting of a single alphabetic
        # character is ~3.3.
        p = password.RawPassword('1')
        self.assertAlmostEqual(p.entropy, 3.3, 1)

    def test_misc(self):
        p = password.RawPassword('a')
        str(p)
        repr(p)


if __name__ == '__main__':
    unittest.main()
