# encoding: utf8

from SmallScrewdriver import BinPacking, DEFAULT_BIN_SIZE
from SmallScrewdriver.Shelf import NextFitShelfBin


# noinspection PyPep8Naming
class NextFitShelfBinPacking(BinPacking):
    def __init__(self, bin_size=DEFAULT_BIN_SIZE, images=None, bin_parameters=None, packing_progress=None,
                 saving_progress=None):
        # TODO выкинуть все изображения размер которых больше размера контейнера
        self.images = sorted(images, key=lambda image: image.crop.size.width, reverse=True)

        BinPacking.__init__(self, bin_size=bin_size, images=images, bin_parameters=bin_parameters,
                            packing_progress=packing_progress, saving_progress=saving_progress)

    def _newBin(self, size, origin, bin_parameters):
        self.bins.append(NextFitShelfBin(size=size, origin=origin, bin_parameters=bin_parameters))
        return self.bins[-1]
