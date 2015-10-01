# encoding: utf8
from SmallScrewdriver import Bin, Point, DEFAULT_BIN_SIZE
from SmallScrewdriver.Shelf import (ShelfBin)


# noinspection PyPep8Naming
class FirstFitShelfBin(ShelfBin):

    BEST_VARIANTS = 0
    WORST_VARIANTS = 1

    AREA_FIT = 0
    SHORT_SIDE_FIT = 1
    LONG_SIDE_FIT = 2
    FLOOR_CEILING = 3
    WASTE_MAP_IMPROVEMENT = 4

    def __init__(self, size=DEFAULT_BIN_SIZE, origin=Point(0, 0), bin_parameters=None):
        ShelfBin.__init__(self, size=size, origin=origin, bin_parameters=bin_parameters)

    def addImage(self, image):

        # Проходим по каждой полке ...
        for shelf in self.shelfs:

            # ... и пробуем добавить изображение ...
            if shelf.addImage(image):
                # ... если получается добавляем изображение в контейнер ...
                return Bin.addImage(self, image)
        else:
            # Если не в одну полку изображение не вошло создаём новую полку и добавляем изображение в
            # контейнер если изображение входит в эту полку, в противном случае, оно не
            # входит в контейнер
            return Bin.addImage(self, image) if self._newShelf().addImage(image) else False
