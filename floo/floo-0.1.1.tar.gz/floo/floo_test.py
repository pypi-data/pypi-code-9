import unittest
from floo import FlooBase, Floo

class TestFlooBase(unittest.TestCase):

    def setUp(self):
        self.floo = FlooBase("abc")

    def test_get_zero(self):
        floo = self.floo
        i = floo.initial()
        self.assertEqual(i, "a")

    def test_get_twenty_seven(self):
        floo = self.floo
        i = floo.encode(27)
        self.assertEqual(i, "baaa")

    def test_get_aaab(self):
        floo = self.floo
        f = floo.decode("baaa")
        self.assertEqual(f, 27)

class TestFloo(unittest.TestCase):

    def setUp(self):
        self.floo = Floo("abc")

    def test_sum_one_plus_one(self):
        r = self.floo.sum("a", "b")
        self.assertEqual(r, "b")

    def test_multiply_two_by_three(self):
        r = self.floo.mul("c", "ba")
        self.assertEqual(r, "ca")

    def test_increment(self):
        r = self.floo.inc("cc")
        self.assertEqual(r, "baa")

    def test_increment(self):
        r = self.floo.dec("ba")
        self.assertEqual(r, "c")

if __name__ == "__main__":
    unittest.main()
