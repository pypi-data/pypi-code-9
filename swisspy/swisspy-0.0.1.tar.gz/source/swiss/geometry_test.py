#!/usr/bin/env python3

import geometry as G
import unittest

class TestStructures(unittest.TestCase):
    def test_calculate_change(self):
        self.assertEqual(G.calculate_change((1, 1), (1, 1)), (0, 0))

    def test_calculate_distance(self):
        self.assertEqual(G.calculate_distance((1, 1), (1, 1)), 0.0)

    def test_calculate_slope(self):
        self.assertEqual(G.calculate_slope((1, 1), (1, 1)), None)

    def test_is_in_circle(self):
        self.assertEqual(G.is_in_circle((1, 1), (0, 0), 1.5), True)

    def test_is_in_range(self):
        self.assertEqual(G.is_in_range((1, 1), (0, 0), 1.5), True)

    def test_rotate_point(self):
        self.assertEqual(G.rotate_point((0, 0), (1, 1), 1), 
                         (-0.30116867893975674, 1.3817732906760363))

    def test_sort_clockwis(self):
        self.assertEqual(G.sort_clockwise((0, 0), [(1,1), (-1, -1), (-1, 1), (1, -1)]),
                         [(-1, 1), (1, 1), (1, -1), (-1, -1)])

    def test_translate_point(self):
        self.assertEqual(G.translate_point(1, (1, 1), (0, 0)),
                         (0.7071067811865475, 0.7071067811865475))

if __name__ == '__main__':
    unittest.main()

