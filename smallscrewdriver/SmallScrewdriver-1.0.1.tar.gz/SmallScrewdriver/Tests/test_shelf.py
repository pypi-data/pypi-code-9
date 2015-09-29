# encoding: utf8

from unittest import TestCase

from SmallScrewdriver import Size, Image, Point
from SmallScrewdriver.Shelf import Shelf


class TestShelf(TestCase):
    def test_addImage(self):
        im1 = Image('../resources', 'fire.png')
        # print im1
        im2 = Image('../resources', 'start.png')
        # print im2
        im3 = Image('../resources', 'win_again.png')
        # print im3
        im4 = Image('../resources', 'fail_again.png')
        # print im4

        # shelf 1
        shelf = Shelf(Size(1024, 1024), Point(0, 300))
        self.assertEqual(shelf.maxSize, Size(1024, 1024))
        self.assertEqual(shelf.size, Size())

        self.assertTrue(shelf.addImage(im1))
        self.assertEqual(shelf.size, Size(226, 226))
        self.assertEqual(len(shelf.images), 1)
        self.assertEqual(im1.origin, Point(0, 300))

        self.assertTrue(shelf.addImage(im2))
        self.assertEqual(shelf.size, Size(226 + 397, 226))
        self.assertEqual(len(shelf.images), 2)
        self.assertEqual(im2.origin, Point(im1.crop.size.width, 300))

        self.assertFalse(shelf.addImage(im3))
        self.assertEqual(len(shelf.images), 2)

        self.assertFalse(shelf.addImage(im4))
        self.assertEqual(len(shelf.images), 2)

        # shelf 2
        shelf2 = Shelf(Size(2048, 2048), Point(0, 200))
        self.assertEqual(shelf2.maxSize, Size(2048, 2048))
        self.assertEqual(shelf2.size, Size())

        self.assertTrue(shelf2.addImage(im1))
        self.assertEqual(shelf2.size, Size(im1.crop.size.width, im1.crop.size.height))
        self.assertEqual(im1.origin, Point(0, 200))

        self.assertTrue(shelf2.addImage(im2))
        self.assertEqual(shelf2.size, Size(im1.crop.size.width + im2.crop.size.width,
                                           max(im1.crop.size.height, im2.crop.size.height)))
        self.assertEqual(im2.origin, Point(im1.crop.size.width, 200))

        self.assertTrue(shelf2.addImage(im3))
        self.assertEqual(shelf2.size, Size(im1.crop.size.width +
                                           im2.crop.size.width +
                                           im3.crop.size.width,
                                           max(im1.crop.size.height,
                                               im2.crop.size.height,
                                               im3.crop.size.height)))
        self.assertEqual(im3.origin, Point(im1.crop.size.width +
                                           im2.crop.size.width, 200))

        self.assertTrue(shelf2.addImage(im4))
        self.assertEqual(shelf2.size, Size(im1.crop.size.width +
                                           im2.crop.size.width +
                                           im3.crop.size.width +
                                           im4.crop.size.width,
                                           max(im1.crop.size.height,
                                               im2.crop.size.height,
                                               im3.crop.size.height,
                                               im4.crop.size.height)))
        self.assertEqual(im4.origin, Point(im1.crop.size.width +
                                           im2.crop.size.width +
                                           im3.crop.size.width, 200))

        # shelf 3
        shelf3 = Shelf(Size(2048, 100))
        self.assertFalse(shelf3.addImage(im1))

        # shelf 4
        im3.rotated = True
        im4.rotated = True

        shelf4 = Shelf(Size(2048, 512))
        self.assertTrue(shelf4.addImage(im3))
        self.assertEqual(shelf4.size, Size(im3.crop.size.height, im3.crop.size.width))

        self.assertTrue(shelf4.addImage(im4))
        self.assertEqual(shelf4.size, Size(im3.crop.size.height + im4.crop.size.height,
                                           max(im3.crop.size.width, im4.crop.size.width)))
