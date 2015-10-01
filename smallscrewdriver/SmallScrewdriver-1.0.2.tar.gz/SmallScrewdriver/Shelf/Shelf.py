# encoding: utf8


# noinspection PyPep8Naming
from SmallScrewdriver import Point, Size, Rect


class Shelf(Rect):
    def __init__(self, max_size, origin=Point()):
        Rect.__init__(self, origin, Size())
        self.maxSize = max_size
        self.images = []

    def addImage(self, image):
        """
        Добавить изображение на полку
        :param image: добавляемое изображение
        :return: True если изображение может быть добавлено
                 False если не может
        """
        free_size = Size(self.maxSize.width - self.size.width, self.maxSize.height)
        image_size = Size(image.crop.size.height, image.crop.size.width) if image.rotated else image.crop.size
        if image_size < free_size:  # >= image_size

            image.origin = Point(self.size.width, self.origin.y)
            self.images.append(image)

            self.size.width += image_size.width
            if image_size.height > self.size.height:
                self.size.height += image_size.height
            return True
        else:
            return False
