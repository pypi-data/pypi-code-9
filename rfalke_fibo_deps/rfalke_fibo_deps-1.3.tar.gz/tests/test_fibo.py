import unittest

import fibo

class TestFibonacci(unittest.TestCase):
    def test_values(self):
        self.assertEqual(fibo.fib(1), 1)
        self.assertEqual(fibo.fib(2), 1)
        self.assertEqual(fibo.fib(3), 2)
        self.assertEqual(fibo.fib(4), 3)
        self.assertEqual(fibo.fib(15), 610)

if __name__ == '__main__':
    unittest.main()
