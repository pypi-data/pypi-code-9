# encoding: utf8

from unittest import TestCase
from SmallScrewdriver import Size


class TestSize(TestCase):
    def test_area(self):
        size = Size(100, 100)
        self.assertEqual(size.area(), 10000)

        size = Size(10, 10)
        self.assertEqual(size.area(), 100)

        size = Size(20, 20)
        self.assertEqual(size.area(), 400)

    def test_eq(self):
        # TODO больше тестов !!!!
        s1 = Size(10, 10)
        s2 = Size(20, 20)
        s3 = Size(10, 20)
        s4 = Size(10, 10)

        self.assertEqual(s1, s4)
        self.assertNotEquals(s1, s2)
        self.assertNotEqual(s1, s3)

    def test_ne(self):
        s1 = Size(10, 10)
        s2 = Size(20, 20)
        s3 = Size(10, 20)
        s4 = Size(10, 10)

        self.assertNotEquals(s1, s2)
        self.assertNotEqual(s1, s3)

        self.assertNotEqual(s2, s3)
        self.assertNotEqual(s2, s4)

        self.assertNotEqual(s3, s4)

    def test_lt(self):
        s1 = Size(8, 6)
        s2 = Size(20, 20)
        s3 = Size(7, 20)
        s4 = Size(11, 9)

        self.assertLess(s1, s2)
        self.assertLess(s4, s2)
        self.assertFalse(s3 < s2)

    def test_is_inscribed(self):
        s1 = Size(10, 10)
        s2 = Size(20, 20)
        s3 = Size(8, 20)
        s4 = Size(40, 5)
        s5 = Size(4, 4)

        self.assertFalse(s1.canInscribe(s2))
        self.assertFalse(s1.canInscribe(s3))
        self.assertFalse(s1.canInscribe(s4))
        self.assertTrue(s1.canInscribe(s5))

        self.assertTrue(s2.canInscribe(s1))
        self.assertFalse(s2.canInscribe(s3))
        self.assertFalse(s2.canInscribe(s4))
        self.assertTrue(s2.canInscribe(s5))

        self.assertFalse(s3.canInscribe(s1))
        self.assertFalse(s3.canInscribe(s2))
        self.assertFalse(s3.canInscribe(s4))
        self.assertTrue(s3.canInscribe(s5))

        self.assertFalse(s4.canInscribe(s1))
        self.assertFalse(s4.canInscribe(s2))
        self.assertFalse(s4.canInscribe(s3))
        self.assertFalse(s4.canInscribe(s3))

        self.assertFalse(s5.canInscribe(s2))
        self.assertFalse(s5.canInscribe(s3))
        self.assertFalse(s5.canInscribe(s1))
        self.assertFalse(s5.canInscribe(s3))

    def test_less(self):
        s1 = Size(10, 10)
        s2 = Size(20, 20)
        s3 = Size(8, 20)
        s4 = Size(40, 5)
        s5 = Size(4, 4)

        self.assertEqual(s1.less(s1), (False, False))
        self.assertEqual(s1.less(s2), (True, True))
        self.assertEqual(s1.less(s3), (False, True))
        self.assertEqual(s1.less(s4), (True, False))
        self.assertEqual(s1.less(s5), (False, False))

        self.assertEqual(s2.less(s1), (False, False))
        self.assertEqual(s2.less(s2), (False, False))
        self.assertEqual(s2.less(s3), (False, False))
        self.assertEqual(s2.less(s4), (True, False))
        self.assertEqual(s2.less(s5), (False, False))

        self.assertEqual(s3.less(s1), (True, False))
        self.assertEqual(s3.less(s2), (True, False))
        self.assertEqual(s3.less(s3), (False, False))
        self.assertEqual(s3.less(s4), (True, False))
        self.assertEqual(s3.less(s5), (False, False))

        self.assertEqual(s4.less(s1), (False, True))
        self.assertEqual(s4.less(s2), (False, True))
        self.assertEqual(s4.less(s3), (False, True))
        self.assertEqual(s4.less(s4), (False, False))
        self.assertEqual(s4.less(s5), (False, False))

        self.assertEqual(s5.less(s1), (True, True))
        self.assertEqual(s5.less(s2), (True, True))
        self.assertEqual(s5.less(s3), (True, True))
        self.assertEqual(s5.less(s4), (True, True))
        self.assertEqual(s5.less(s5), (False, False))

    def test_equal(self):
        s1 = Size(10, 10)
        s2 = Size(20, 20)
        s3 = Size(8, 20)
        s4 = Size(40, 5)
        s5 = Size(4, 4)

        self.assertEqual(s1.equal(s1), (True, True))
        self.assertEqual(s1.equal(s2), (False, False))
        self.assertEqual(s1.equal(s3), (False, False))
        self.assertEqual(s1.equal(s4), (False, False))
        self.assertEqual(s1.equal(s5), (False, False))

        self.assertEqual(s2.equal(s1), (False, False))
        self.assertEqual(s2.equal(s2), (True, True))
        self.assertEqual(s2.equal(s3), (False, True))
        self.assertEqual(s2.equal(s4), (False, False))
        self.assertEqual(s2.equal(s5), (False, False))

        self.assertEqual(s3.equal(s1), (False, False))
        self.assertEqual(s3.equal(s2), (False, True))
        self.assertEqual(s3.equal(s3), (True, True))
        self.assertEqual(s3.equal(s4), (False, False))
        self.assertEqual(s3.equal(s5), (False, False))

        self.assertEqual(s4.equal(s1), (False, False))
        self.assertEqual(s4.equal(s2), (False, False))
        self.assertEqual(s4.equal(s3), (False, False))
        self.assertEqual(s4.equal(s4), (True, True))
        self.assertEqual(s4.equal(s5), (False, False))

        self.assertEqual(s5.equal(s1), (False, False))
        self.assertEqual(s5.equal(s2), (False, False))
        self.assertEqual(s5.equal(s3), (False, False))
        self.assertEqual(s5.equal(s4), (False, False))
        self.assertEqual(s5.equal(s5), (True, True))
