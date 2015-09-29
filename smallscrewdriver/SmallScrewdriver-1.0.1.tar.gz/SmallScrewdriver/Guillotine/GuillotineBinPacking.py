# coding=utf-8
from SmallScrewdriver import (BinPacking, DEFAULT_BIN_SIZE)
from SmallScrewdriver.Guillotine import (GuillotineBin)


# noinspection PyPep8Naming,PyShadowingBuiltins
class GuillotineBinPacking(BinPacking):
    def __init__(self, bin_size=DEFAULT_BIN_SIZE, images=None, bin_parameters=None, packing_progress=None,
                 saving_progress=None):
        # Отсеиваем изображения которые больше размера контейнера
        images = filter(lambda image: image.crop.size.less(bin_size) == (True, True), images)

        BinPacking.__init__(self, bin_size=bin_size, images=images, bin_parameters=bin_parameters,
                            packing_progress=packing_progress, saving_progress=saving_progress)

    def _newBin(self, size, origin, bin_parameters):
        self.bins.append(GuillotineBin(size=size, origin=origin, bin_parameters=bin_parameters))
        return self.bins[-1]
