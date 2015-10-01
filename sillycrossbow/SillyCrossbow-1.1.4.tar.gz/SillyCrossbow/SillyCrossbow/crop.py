# encoding: utf8
from PySide.QtGui import QImage

from SillyCrossbow import CropTransparent


def crop_image_from_file(filename, threshold):
    """
    Найти непрозрачную область на изображении и вырезать её
    :param image: Имя файла изображения
    :param threshold: Порог прозрачности для обрезания
    :return: cropped_image - вырезанное изображение
             x, y, width, height - координаты и размер вырезаннго прямоугольника
    """
    image = QImage(filename)
    return crop_image(image, threshold)


def crop_image(image, threshold):
    """
    Найти непрозрачную область на изображении и вырезать её
    :param image: Изображение
    :param threshold: Порог прозрачности для обрезания
    :return: cropped_image - вырезанное изображение
             x, y, width, height - координаты и размер вырезаннго прямоугольника
    """
    cropper = CropTransparent(image.width(), image.height(), threshold, str(image.constBits()))
    x = cropper.getCroppedOffsetX()
    y = cropper.getCroppedOffsetY()
    width = cropper.getCroppedWidth()
    height = cropper.getCroppedHeight()

    cropped_image = image.copy(x, y, width, height)

    return cropped_image, x, y, width, height
