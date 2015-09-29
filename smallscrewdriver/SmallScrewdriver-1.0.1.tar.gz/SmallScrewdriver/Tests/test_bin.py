from unittest import TestCase
import math
from SmallScrewdriver import Bin, Size, Point, Rect, DEFAULT_BIN_SIZE


class TestBin(TestCase):

    def test_ctor(self):

        b = Bin()
        self.assertEqual(b.size, DEFAULT_BIN_SIZE)
        self.assertEqual(b.origin, Point())

        b = Bin(size=DEFAULT_BIN_SIZE, origin=Point())
        self.assertEqual(b.size, DEFAULT_BIN_SIZE)
        self.assertEqual(b.origin, Point())

        b = Bin(size=Size(512, 512), origin=Point(10, 10))
        self.assertEqual(b.size, Size(512, 512))
        self.assertEqual(b.origin, Point(10, 10))

        b = Bin(**{'size': Size(512, 512), 'origin': Point(20, 20)})
        self.assertEqual(b.size, Size(512, 512))
        self.assertEqual(b.origin, Point(20, 20))

        b = Bin(size=Size(256, 256), origin=Point(30, 30))
        self.assertEqual(b.size, Size(256, 256))
        self.assertEqual(b.origin, Point(30, 30))

    def test_append1(self):
        b = Bin(Size(256, 256), Point(0, 0))

        self.assertTrue(b.addImage(Rect(Point(0, 0), Size(10, 10))))
        self.assertEqual(len(b.images), 1)
        # area = 100

        self.assertTrue(b.addImage(Rect(Point(10, 10), Size(100, 100))))
        self.assertEqual(len(b.images), 2)
        # area == 10100

        self.assertTrue(b.addImage(Rect(Point(10, 10), Size(100, 100))))
        self.assertEqual(len(b.images), 3)
        # area == 20100

        self.assertTrue(b.addImage(Rect(Point(10, 10), Size(100, 100))))
        self.assertEqual(len(b.images), 4)
        # area == 30100

        self.assertTrue(b.addImage(Rect(Point(10, 10), Size(100, 100))))
        self.assertEqual(len(b.images), 5)
        # area == 40100

        self.assertTrue(b.addImage(Rect(Point(10, 10), Size(50, 50))))
        self.assertEqual(len(b.images), 6)
        # area == 42600

        self.assertTrue(b.addImage(Rect(Point(10, 10), Size(50, 50))))
        self.assertEqual(len(b.images), 7)
        # area == 45100

        self.assertTrue(b.addImage(Rect(Point(10, 10), Size(50, 50))))
        self.assertEqual(len(b.images), 8)
        # area == 47600

        self.assertTrue(b.addImage(Rect(Point(10, 10), Size(50, 50))))
        self.assertEqual(len(b.images), 9)
        # area == 50100

        # assert b.addImage(Rect(Point(10, 10), Size(100, 100)))
        # assert len(b.images) == 10

        self.assertFalse(b.addImage(Rect(Point(0, 0), Size(512, 512))))
        self.assertEqual(len(b.images), 9)

    def test_fillLevel(self):
        b = Bin(Size(256, 256), Point(0, 0))

        self.assertTrue(b.addImage(Rect(Point(0, 0), Size(10, 10))))
        self.assertLess(math.fabs(b.fillLevel() - (10. * 10.) / (256. * 256.)), 1e-6)

        self.assertTrue(b.addImage(Rect(Point(0, 0), Size(20, 20))))
        self.assertLess(math.fabs(b.fillLevel() - (10. * 10. + 20. * 20.) / (256. * 256.)), 1e-6)

        self.assertTrue(b.addImage(Rect(Point(0, 0), Size(40, 40))))
        self.assertLess(math.fabs(b.fillLevel() - (10. * 10. + 20. * 20. + 40. * 40.) / (256. * 256.)), 1e-6)
