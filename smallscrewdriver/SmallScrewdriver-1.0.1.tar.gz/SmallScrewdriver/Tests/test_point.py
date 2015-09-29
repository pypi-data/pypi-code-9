from unittest import TestCase
from SmallScrewdriver import Point

__author__ = 'Pavel'


class TestPoint(TestCase):
    def setUp(self):
        self.p1 = Point(10, 10)
        self.p2 = Point(20, 20)
        self.p3 = Point(10, 10)
        self.p4 = Point(10, 20)
        self.p5 = Point(20, 10)

    def tearDown(self):
        super(TestPoint, self).tearDown()

    def test_eq(self):
        self.assertEqual(self.p1, self.p3)
        self.assertNotEqual(self.p1, self.p2)
        self.assertNotEqual(self.p1, self.p4)
        self.assertNotEqual(self.p1, self.p5)
        self.assertNotEqual(self.p2, self.p3)
        self.assertNotEqual(self.p3, self.p4)
        self.assertNotEqual(self.p4, self.p5)

    def test_add(self):
        self.assertEqual(self.p1 + self.p2, Point(30, 30))
        self.assertEqual(self.p1 + self.p3, Point(20, 20))
        self.assertEqual(self.p2 + self.p3, Point(30, 30))

    def test_iadd(self):
        self.p1 += self.p1
        self.assertEqual(self.p1, Point(20, 20))

        self.p1 += self.p2
        self.assertEqual(self.p1, Point(40, 40))

        self.p1 += self.p3
        self.assertEqual(self.p1, Point(50, 50))

    def test_str(self):
        self.assertEqual(str(self.p1), 'Point(10, 10)')
        self.assertEqual(str(self.p2), 'Point(20, 20)')
        self.assertEqual(str(self.p3), 'Point(10, 10)')
        self.assertEqual(str(self.p4), 'Point(10, 20)')
        self.assertEqual(str(self.p5), 'Point(20, 10)')
