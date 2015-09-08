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
        self.assertEqual(eq.eq_registry['add']['fn'](1, 5), 6)
        self.assertEqual(add(1, 6), 7)

    def test_eq_id(self):
        @eq(1)
        def a():
            return 1

        self.assertEqual(eq.id[1]['fn'](), 1)

        @eq(2)
        def a():
            return 2

        self.assertEqual(eq.id[1]['fn'](), 1)
        self.assertEqual(eq.id[2]['fn'](), 2)

        eq.eq_registry['a']['args'] = ['b']
        self.assertEqual(eq.eq_registry['a']['args'], eq.id[2]['args'])

        eq.id[2]['fn'] = lambda x: x ** 2
        self.assertEqual(eq.eq_registry['a']['fn'], eq.id[2]['fn'])

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
