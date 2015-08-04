import unittest
from double_down import double_down


class TestDoubleDownDecorator(unittest.TestCase):

    def setUp(self):
        self.arr = list(range(2))

    def test_decorator(self):
        @double_down
        def append(arr, num):
            arr.append(num)
            return arr

        result = append(self.arr, -1)
        expected = list(range(2)) + [-1, -1]

        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
