from unittest import TestCase
from SmallScrewdriver import Image, Rect, Size, Point


class TestImage(TestCase):
    def test_bg_image(self):
        image = Image('../resources', 'bg.png')

        self.assertEqual(image.size.width, 1024)
        self.assertEqual(image.size.height, 1024)

        self.assertEqual(image.area(), 1024 * 1024)

        self.assertEqual(image.crop, Rect(Point(0, 0), Size(1024, 1024)))

    def test_fire(self):
        fire = Image('../resources', 'fire.png')

        self.assertEqual(fire.size.width, 256)
        self.assertEqual(fire.size.height, 256)

        self.assertEqual(fire.area(), Rect(Point(16, 15), Size(226, 226)).area())

        self.assertEqual(fire.crop, Rect(Point(16, 15), Size(226, 226)))

    def test_cropImage(self):
        fire = Image('../resources', 'fire.png')

        self.assertEqual(fire.crop.size.width, 226)
        self.assertEqual(fire.crop.size.height, 226)
