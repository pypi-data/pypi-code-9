import unittest
from redbeaver.exceptions import InfiniteLoopError
from eq import Eq as eq
from calc import calc


class MyTestCase(unittest.TestCase):
    def test_eq(self):
        @eq(1)
        def add(a, b):
            return a + b

        self.assertEqual(eq.eq_registry['add']['args'], ['a', 'b'])
        self.assertEqual(eq.id[1], 'add')
        self.assertEqual(eq.eq_registry['add']['fn'](1, 5), 6)
        self.assertEqual(add(1, 6), 7)

    def test_calc(self):
        @eq(1)
        def add(a, b):
            return a + b

        @eq(2)
        def a(b):
            return b * 2

        eq.params['b'] = 4

        calc('add', eq)

        self.assertEqual(eq.params['add'], 12)

    def test_calc_loop_except(self):
        @eq(1)
        def a(b):
            return b * 2

        @eq(2)
        def b(c):
            return c * 4

        @eq(3)
        def c(a):
            return a * 2

        self.assertRaises(InfiniteLoopError, calc, *['a', eq])


if __name__ == '__main__':
    unittest.main()
