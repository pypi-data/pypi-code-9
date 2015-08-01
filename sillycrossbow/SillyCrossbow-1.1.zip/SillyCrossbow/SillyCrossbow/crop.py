# encoding: utf8
from PySide.QtGui import QImage

from SillyCrossbow import CropTransparent


# noinspection PyPep8Naming
def cropImageFromFile(filename, threshold):
    image = QImage(filename)
    return cropImage(image, threshold)


# noinspection PyPep8Naming
def cropImage(image, threshold):
    cropper = CropTransparent(image.width(), image.height(), threshold, str(image.constBits()))
    x = cropper.getCroppedOffsetX()
    y = cropper.getCroppedOffsetY()
    width = cropper.getCroppedWidth()
    height = cropper.getCroppedHeight()

    cropped_image = image.copy(x, y, width, height)

    return cropped_image, x, y, width, height
