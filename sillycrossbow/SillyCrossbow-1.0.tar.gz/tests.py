# encoding: utf8

import unittest
from PIL import Image
from SillyCrossbow import CropTransparent, CropRect

class SillyCrossbow(unittest.TestCase):
    def test_imagecrop4x4(self):

        width = 4
        height = 4
        threshold = 50

        data = str(bytearray([
            1, 1, 1, 10,   1, 1, 1, 10,   1, 1, 1, 10,   1, 1, 1, 10,
            1, 1, 1, 10,   1, 1, 1, 100,   1, 1, 1, 100,   1, 1, 1, 10,
            1, 1, 1, 10,   1, 1, 1, 100,   1, 1, 1, 100,   1, 1, 1, 10,
            1, 1, 1, 10,   1, 1, 1, 10,   1, 1, 1, 10,   1, 1, 1, 10,
        ]))

        cropper = CropTransparent(width, height, threshold, data)

        assert cropper.getCroppedHeight() == 2
        assert cropper.getCroppedWidth() == 2
        assert cropper.getCroppedOffsetX() == 1
        assert cropper.getCroppedOffsetY() == 1

        crop_rect = cropper.getRect()

        assert crop_rect.x == 1
        assert crop_rect.y == 1
        assert crop_rect.width == 2
        assert crop_rect.height == 2


    def test_imagecrop4x4(self):

        width = 6
        height = 6
        threshold = 50

        data = str(bytearray([
            1, 1, 1, 10 ,   1, 1, 1, 10 ,   1, 1, 1, 10 ,   1, 1, 1, 10 ,   1, 1, 1, 10 ,   1, 1, 1, 10 ,
            1, 1, 1, 10 ,   1, 1, 1, 10 ,   1, 1, 1, 10 ,   1, 1, 1, 10 ,   1, 1, 1, 10 ,   1, 1, 1, 10 ,
            1, 1, 1, 10 ,   1, 1, 1, 10 ,   1, 1, 1, 100,   1, 1, 1, 100,   1, 1, 1, 100,   1, 1, 1, 10 ,
            1, 1, 1, 10 ,   1, 1, 1, 10 ,   1, 1, 1, 100,   1, 1, 1, 100,   1, 1, 1, 100,   1, 1, 1, 10 ,
            1, 1, 1, 10 ,   1, 1, 1, 10 ,   1, 1, 1, 100,   1, 1, 1, 100,   1, 1, 1, 100,   1, 1, 1, 10 ,
            1, 1, 1, 10 ,   1, 1, 1, 10 ,   1, 1, 1, 10 ,   1, 1, 1, 10 ,   1, 1, 1, 10 ,   1, 1, 1, 10 ,
        ]))

        cropper = CropTransparent(width, height, threshold, data)

        assert cropper.getCroppedHeight() == 3
        assert cropper.getCroppedWidth() == 3
        assert cropper.getCroppedOffsetX() == 2
        assert cropper.getCroppedOffsetY() == 2

        crop_rect = cropper.getRect()

        assert crop_rect.x == 2
        assert crop_rect.y == 2
        assert crop_rect.width == 3
        assert crop_rect.height == 3

    def test_fire_png(self):

        fire = Image.open('data/fire.png')
        cropper = CropTransparent(fire.width, fire.height, 50, fire.tostring())

        assert cropper.getCroppedOffsetX() == 16
        assert cropper.getCroppedOffsetY() == 15
        assert cropper.getCroppedHeight() == 226
        assert cropper.getCroppedWidth() == 226

        crop_rect = cropper.getRect()

        assert crop_rect.x == 16
        assert crop_rect.y == 15
        assert crop_rect.width == 226
        assert crop_rect.height == 226

