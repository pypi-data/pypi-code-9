import unittest

from .cpp import *


class CppTest(unittest.TestCase):
    def test_int(self):
        self.assertEqual(dumps({"x": 3}), "int x = 3;\n")

    def test_int_custom_type(self):
        self.assertEqual(dumps({"x": 3}, int_type="size_t"), "size_t x = 3;\n")

    def test_float(self):
        self.assertEqual(dumps({"x": 3.5}), "double x = 3.5;\n")

    def test_float_custom_type(self):
        self.assertEqual(dumps({"x": 3.5}, float_type="float"), "float x = 3.5;\n")

    def test_string(self):
        self.assertEqual(dumps({"x": "abc"}), 'std::string x = "abc";\n')

    def test_string_custom_type(self):
        self.assertEqual(dumps({"x": "abc"}, string_type="const char*"), 'const char* x = "abc";\n')

    def test_int_list(self):
        self.assertEqual(dumps({"x": [1, 2, 3]}), 'int x[3] = {1, 2, 3};\n')

    def test_int_tuple(self):
        self.assertEqual(dumps({"x": (1, 2, 3)}), 'int x[3] = {1, 2, 3};\n')

    def test_int_array(self):
        self.assertEqual(dumps({"x": np.array([1, 2, 3])}), 'int x[3] = {1, 2, 3};\n')

    def test_float_array(self):
        self.assertEqual(dumps({"x": np.array([1., 2.])}), 'double x[2] = {1.000000000000, 2.000000000000};\n')

    def test_float_array_precision(self):
        self.assertEqual(dumps({"x": np.array([1., 2.])}, precision=2), 'double x[2] = {1.00, 2.00};\n')

    def test_2d_array(self):
        expected = """
int x[2][3] = {{0, 1, 2},
               {3, 4, 5}};
"""
        self.assertEqual(dumps({"x": np.arange(6).reshape((2, 3))}), expected[1:])

    def test_multidim_array(self):
        expected = """
int x[2][2][3] = {{{0, 1, 2},
                   {3, 4, 5}},
                  {{6, 7, 8},
                   {9, 10, 11}}};
"""
        self.assertEqual(dumps({"x": np.arange(12).reshape((2, 2, 3))}), expected[1:])

    def test_namespace(self):
        expected = """
namespace Foo {
    int x = 1;
}
"""
        self.assertEqual(dumps({"x": 1}, namespace="Foo"), expected[1:])