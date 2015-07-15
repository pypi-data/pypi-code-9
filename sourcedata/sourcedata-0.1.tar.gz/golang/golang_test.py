import unittest

from .golang import *


class GolangTest(unittest.TestCase):
    def test_int(self):
        self.assertEqual(dumps({"x": 3}), "var x int = 3\n")

    def test_int_custom_type(self):
        self.assertEqual(dumps({"x": 3}, int_type="int64"), "var x int64 = 3\n")

    def test_float(self):
        self.assertEqual(dumps({"x": 3.5}), "var x float64 = 3.5\n")

    def test_float_custom_type(self):
        self.assertEqual(dumps({"x": 3.5}, float_type="float32"), "var x float32 = 3.5\n")

    def test_string(self):
        self.assertEqual(dumps({"x": "abc"}), 'var x = `abc`\n')

    def test_int_list(self):
        self.assertEqual(dumps({"x": [1, 2, 3]}), 'var x = []int{1, 2, 3}\n')

    def test_int_tuple(self):
        self.assertEqual(dumps({"x": (1, 2, 3)}), 'var x = []int{1, 2, 3}\n')

    def test_int_array(self):
        self.assertEqual(dumps({"x": np.array([1, 2, 3])}), 'var x = []int{1, 2, 3}\n')

    def test_float_array(self):
        self.assertEqual(dumps({"x": np.array([1., 2.])}), 'var x = []float64{1.000000000000, 2.000000000000}\n')

    def test_float_array_precision(self):
        self.assertEqual(dumps({"x": np.array([1., 2.])}, precision=2), 'var x = []float64{1.00, 2.00}\n')

    @unittest.skip
    def test_2d_array(self):
        expected = """
var x = [][]int{{0, 1, 2},
                {3, 4, 5}}
"""
        self.assertEqual(dumps({"x": np.arange(6).reshape((2, 3))}), expected[1:])

    @unittest.skip
    def test_multidim_array(self):
        expected = """
var x = [][][]int{{{0, 1, 2},
                   {3, 4, 5}},
                  {{6, 7, 8},
                   {9, 10, 11}}}
"""
        self.assertEqual(dumps({"x": np.arange(12).reshape((2, 2, 3))}), expected[1:])

    def test_package(self):
        expected = """
package foo

var x int = 1
"""
        self.assertEqual(dumps({"x": 1}, package="foo"), expected[1:])
