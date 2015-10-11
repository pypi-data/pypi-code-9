#!/usr/bin/env python3

import data as D
import unittest

class TestStructures(unittest.TestCase):
    def test_dedupe(self):
        self.assertEqual(D.dedupe([]), [])
        self.assertEqual(D.dedupe([0]), [0])
        self.assertEqual(D.dedupe([0, 0]), [0])
        self.assertEqual(D.dedupe([0, 1, 2, 1]), [0, 1, 2])

        self.assertEqual(D.dedupe([0, 1, 2, 1], lambda x: x), [0, 1, 2])
        self.assertEqual(D.dedupe([0, 1, 2, 1], lambda x: x - 1), [-1, 0, 1])

if __name__ == '__main__':
    unittest.main()

