# encoding: utf8

import unittest

from PySide.QtGui import QImage

from SillyCrossbow import CropTransparent


class SillyCrossbow(unittest.TestCase):
    def test_imagecrop4x4(self):
        width = 4
        height = 4
        threshold = 50

        data = str(bytearray([
            1, 1, 1, 10, 1, 1, 1, 10, 1, 1, 1, 10, 1, 1, 1, 10,
            1, 1, 1, 10, 1, 1, 1, 100, 1, 1, 1, 100, 1, 1, 1, 10,
            1, 1, 1, 10, 1, 1, 1, 100, 1, 1, 1, 100, 1, 1, 1, 10,
            1, 1, 1, 10, 1, 1, 1, 10, 1, 1, 1, 10, 1, 1, 1, 10,
        ]))

        cropper = CropTransparent(width, height, threshold, data)

        self.assertEqual(cropper.getCroppedHeight(), 2)
        self.assertEqual(cropper.getCroppedWidth(), 2)
        self.assertEqual(cropper.getCroppedOffsetX(), 1)
        self.assertEqual(cropper.getCroppedOffsetY(), 1)

        crop_rect = cropper.getRect()

        self.assertEqual(crop_rect.x, 1)
        self.assertEqual(crop_rect.y, 1)
        self.assertEqual(crop_rect.width, 2)
        self.assertEqual(crop_rect.height, 2)

    def test_imagecrop4x4(self):
        width = 6
        height = 6
        threshold = 50

        data = str(bytearray([
            1, 1, 1, 10, 1, 1, 1, 10, 1, 1, 1, 10, 1, 1, 1, 10, 1, 1, 1, 10, 1, 1, 1, 10,
            1, 1, 1, 10, 1, 1, 1, 10, 1, 1, 1, 10, 1, 1, 1, 10, 1, 1, 1, 10, 1, 1, 1, 10,
            1, 1, 1, 10, 1, 1, 1, 10, 1, 1, 1, 100, 1, 1, 1, 100, 1, 1, 1, 100, 1, 1, 1, 10,
            1, 1, 1, 10, 1, 1, 1, 10, 1, 1, 1, 100, 1, 1, 1, 100, 1, 1, 1, 100, 1, 1, 1, 10,
            1, 1, 1, 10, 1, 1, 1, 10, 1, 1, 1, 100, 1, 1, 1, 100, 1, 1, 1, 100, 1, 1, 1, 10,
            1, 1, 1, 10, 1, 1, 1, 10, 1, 1, 1, 10, 1, 1, 1, 10, 1, 1, 1, 10, 1, 1, 1, 10,
        ]))

        cropper = CropTransparent(width, height, threshold, data)

        self.assertEqual(cropper.getCroppedHeight(), 3)
        self.assertEqual(cropper.getCroppedWidth(), 3)
        self.assertEqual(cropper.getCroppedOffsetX(), 2)
        self.assertEqual(cropper.getCroppedOffsetY(), 2)

        crop_rect = cropper.getRect()

        self.assertEqual(crop_rect.x, 2)
        self.assertEqual(crop_rect.y, 2)
        self.assertEqual(crop_rect.width, 3)
        self.assertEqual(crop_rect.height, 3)

    def test_fire_png(self):
        fire = QImage('data/fire.png')

        cropper = CropTransparent(fire.width(), fire.height(), 50, str(fire.constBits()))

        self.assertEqual(cropper.getCroppedOffsetX(), 16)
        self.assertEqual(cropper.getCroppedOffsetY(), 15)
        self.assertEqual(cropper.getCroppedHeight(), 226)
        self.assertEqual(cropper.getCroppedWidth(), 226)

        crop_rect = cropper.getRect()

        self.assertEqual(crop_rect.x, 16)
        self.assertEqual(crop_rect.y, 15)
        self.assertEqual(crop_rect.width, 226)
        self.assertEqual(crop_rect.height, 226)
