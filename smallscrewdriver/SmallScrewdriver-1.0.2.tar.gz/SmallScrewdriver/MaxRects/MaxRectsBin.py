# coding: utf-8
from SmallScrewdriver import Bin, DEFAULT_BIN_SIZE, Point, Rect


class MaxRectsBin(Bin):
    """
    Контейнер для метода максимальных прямоугольников
    """

    # Эвристики выбора
    HEURISTIC_BL = 0
    HEURISTIC_BAF = 1
    HEURISTIC_BSSF = 2
    HEURISTIC_BLSF = 3

    def __init__(self, size=DEFAULT_BIN_SIZE, origin=Point(), bin_parameters=None):
        Bin.__init__(self, size=size, origin=origin, bin_parameters=bin_parameters)

        self.free_rect = [Rect(size=self.size)]

    def addImage(self, image):

        fr = sorted(self.free_rect, key=lambda rect: rect.area())
        print fr

        fr = filter(lambda rect: rect.area() > image.crop.area(), fr)
        print fr

        for rect in fr:
            s, r1, r2, rotate = rect.split(image.crop, Rect.RULE_PICK_BOTH)

            if s > 0:
                image.origin = rect.origin
                image.rotated = rotate

                if s == 1:
                    del fr[rect]
                    fr += [r1]
                    return Bin.addImage(self, image=image)

                elif s == 2:
                    del fr[rect]
                    fr += [r1, r2]
                    return Bin.addImage(self, image=image)

                else:
                    raise SystemError('Error')

        return False
