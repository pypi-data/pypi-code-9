import unittest

import libsousou


class CoverageTestCase(unittest.TestCase):

    def test_get_version(self):
        libsousou.get_version()


if __name__ == '__main__':
    unitest.main()
