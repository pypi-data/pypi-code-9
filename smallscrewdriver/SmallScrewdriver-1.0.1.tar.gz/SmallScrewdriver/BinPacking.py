# encoding: utf8
from SmallScrewdriver import DEFAULT_BIN_SIZE, Point
from abc import abstractmethod


# noinspection PyPep8Naming,PyShadowingBuiltins
class BinPacking(object):
    def __init__(self, bin_size=DEFAULT_BIN_SIZE, images=None, bin_parameters=None, packing_progress=None, saving_progress=None):
        self.bins = []

        self.packingProgress = packing_progress
        self.savingProgress = saving_progress

        # Первый контейнер
        self._newBin(size=bin_size, origin=Point(), bin_parameters=bin_parameters)

        images = [] if images is None else images

        # Проходим по всем изображениям ...
        for index, image in enumerate(images):

            # ... и по всем контейнерам ...
            for bin in self.bins:

                # ... пробуем поместить изображение в контейнер ...
                if bin.addImage(image):

                    self.__packingProgress(100 * index / len(images))

                    # ... если получилось, идём к следующему изображению ...
                    break
            else:
                # ... если не в один контейнер, поместить не получилось, создаём новый ...
                bin = self._newBin(size=bin_size, origin=Point(), bin_parameters=bin_parameters)

                # ... и пробуем поместить в него ...
                if bin.addImage(image):
                    self.__packingProgress(100 * index / len(images))
                else:
                    # ... и если не получается значит произошла ...
                    raise SystemError(u'Какая та хуйня')

        self.__packingProgress(100)

    def saveAtlases(self, directory):
        for i, b in enumerate(self.bins):
            self.__savingProgress(100 * i / len(self.bins))
            b.save(directory + '/atlas' + str(i))

        self.__savingProgress(100)

    def __packingProgress(self, progress):
        if self.packingProgress:
            self.packingProgress(progress)

    def __savingProgress(self, progress):
        if self.savingProgress:
            self.savingProgress(progress)

    @abstractmethod
    def _newBin(self, size, origin, bin_parameters):
        raise NotImplementedError
