import unittest
from redbeaver.exceptions import InfiniteLoopError
from formula import Formula
from calc import Calc


class MyTestCase(unittest.TestCase):
    def test_formula_fn_registry_args(self):
        f = Formula()

        @f(1)
        def a(b, c):
            return b + c

        self.assertEqual(f.get_fn_by_name('a')[f.__ARGS_KEY__][1], ['b', 'c'])

    def test_formula_fn_registry_call(self):
        f = Formula()

        @f(1)
        def a(b):
            return b ** 2

        self.assertEqual(f.get_fn_by_name('a')[f.__CALL_KEY__][1](2), 4)

    def test_fn_call_outside_formula(self):
        f = Formula()

        @f(1)
        def a(b, c):
            return b * c

        self.assertEqual(a(50, 41), 2050)

    def test_formula_param_add_when_fn_call_outside_formula(self):
        f = Formula()

        @f(1)
        def a(b, c):
            return b - c

        a(100, 98)

        self.assertEqual(f.get_params(), {'a': 2, 'b': 100, 'c': 98})

    def test_formula_num_call(self):
        f = Formula()

        @f(1)
        def a(b):
            return b ** 2

        self.assertEqual(f(1)(5), 25)

    def test_formula_set_params(self):
        f = Formula()

        f({'a': 2, 'b': 5})

        self.assertEqual(f('a'), 2)
        self.assertEqual(f.get_param('b'), 5)

    def test_calc(self):
        f = Formula()
        calc = Calc(f)

        @f(1)
        def a(b, c):
            return b + c

        @f(2)
        def b(c):
            return c * 2

        f({'c': 4})

        calc('a')

        self.assertEqual(f('a'), 12)
        self.assertEqual(f.get_param('b'), 8)

    def test_calc_loop_except(self):
        f = Formula()
        calc = Calc(f)

        @f(1)
        def a(b):
            return b * 2

        @f(2)
        def b(c):
            return c * 4

        @f(3)
        def c(a):
            return a * 2

        self.assertRaises(InfiniteLoopError, calc, *['a'])

    def test_calc_iterate_param(self):
        f = Formula()
        calc = Calc(f)

        @f(1)
        def a(b):
            return b * 2

        @f(2)
        def b(c):
            return c * 2

        f({'c': range(5)})

        calc('a', iterate_param='c')

        self.assertEqual(f('a'), [i * 4 for i in range(5)])

    def test_formula_reset_params(self):
        f = Formula()
        calc = Calc(f)

        @f(1)
        def a(b):
            return b ** 2

        f({'b': 5})

        calc('a')

        f.reset_params()

        self.assertEqual(f.get_params(), {})

if __name__ == '__main__':
    unittest.main()
