# encoding: utf8
from PySide.QtCore import (QPoint, Qt, QDir)
from PySide.QtGui import (QImage, QTransform)

from SmallScrewdriver import (Rect, Size, Point)
from SillyCrossbow import (crop_image)


# noinspection PyPep8Naming,PyUnusedLocal
class Image(Rect):
    """
    self.origin - показывает положение в атласе
    self.size   - оригинальный размер изображения
    self.crop   - область изображения взятого из оригинала после обрезания прозрачных краёв
    """

    def __init__(self, directory, filename):
        self.directory = directory
        self.filename = filename

        image = QImage(self.directory + QDir.separator() + self.filename)

        Rect.__init__(self, Point(), Size(image.width(), image.height()))

        self.image, x, y, width, height = crop_image(image, 50)
        self.crop = Rect(Point(x, y), Size(width, height))

        self.rotated = False

    def area(self):
        return self.crop.area()

    def draw(self, painter, offset=Point()):
        origin_offset = QPoint(self.origin.x + offset.x, self.origin.y + offset.y)

        if self.rotated:
            old_transform = QTransform(painter.transform())
            painter.setTransform(painter.transform().translate(origin_offset.x() + self.crop.size.height,
                                                               origin_offset.y()).rotate(90, Qt.ZAxis))
            painter.drawImage(0, 0, self.image)
            painter.setTransform(old_transform)
        else:
            painter.drawImage(origin_offset, self.image)
        # Rect(self.origin, self.crop.size).draw(painter, offset)

    def toJson(self):
        return {
            'offset': {
                'x': self.origin.x,
                'y': self.origin.y
            },
            'original_size': {
                'width': self.size.width,
                'height': self.size.height
            },
            'crop': {
                'origin': {
                    'x': self.crop.origin.x,
                    'y': self.crop.origin.y
                },
                'size': {
                    'width': self.crop.size.width,
                    'height': self.crop.size.height
                }
            },
            'rotated': self.rotated,
            'filename': self.filename
        }

    # noinspection PyUnreachableCode
    def __str__(self):
        return '{klass}({file}, {origin}, {size}, {crop}, {rotated})'.format(klass=self.__class__.__name__,
                                                                             file=self.filename,
                                                                             crop=self.crop,
                                                                             origin=self.origin,
                                                                             size=self.size,
                                                                             rotated=self.rotated)

    def __repr__(self):
        return self.__str__()
