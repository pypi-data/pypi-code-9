# coding=utf-8

from SmallScrewdriver import Bin, DEFAULT_BIN_SIZE, Point, Rect


class GuillotineBin(Bin):
    """
    Контейнер для метода гильотины
    """

    BEST_VARIANTS = 0
    WORST_VARIANTS = 1

    AREA_FIT = 0
    SHORT_SIDE_FIT = 1
    LONG_SIDE_FIT = 2

    def __init__(self, size=DEFAULT_BIN_SIZE, origin=Point(), bin_parameters=None):
        Bin.__init__(self, size=size, origin=origin, bin_parameters=bin_parameters)

        self.select_variant = self.bin_parameters['selection_variant']
        self.select_heuristic = self.bin_parameters['selection_heuristic']
        self.split_rule = self.bin_parameters['split_rule']

        self.free_rects = [Rect(size=self.size)]

    def addImage(self, image):

        af = lambda x: x.area()
        ssf = lambda x: min(x.size.width - image.size.width, x.size.height - image.size.height)
        lsf = lambda x: max(x.size.width - image.size.width, x.size.height - image.size.height)

        # Сортируем
        rects = sorted(self.free_rects, key=[af, ssf, lsf][self.select_heuristic], reverse=bool(self.select_variant))

        # Проходим по свободным прямоугольникам
        for rect in rects:
            # Делим прямоугольник обрезанным прямоугольником из нашего изображения
            s, rs1, rs2, rotate = rect.split(image.crop, self.split_rule)

            # Если разрезание прошло успешно ...
            if s > 0:

                # ... в изображение записываем новые, смещение и поворот
                image.origin = rect.origin
                image.rotated = rotate

                # Если разрезало на 2 части ...
                if s == 2:
                    # ... удаляем текущий прямоугольник ...
                    self.free_rects.remove(rect)
                    # ... и вставляем 2 новых
                    self.free_rects += [rs1, rs2]
                    # Добавляем изображение в контейнер
                    return Bin.addImage(self, image)

                # Если отрезало одну часть
                elif s == 1:
                    # ... удаляем текущий прямоугольник ...
                    self.free_rects.remove(rect)
                    # ... добавляем новый
                    self.free_rects += [rs1]
                    # Добавляем изображение в контейнер
                    return Bin.addImage(self, image)

                # Такого не может быть ...
                else:
                    raise RuntimeError(u'Пиздёж и провокация')

        # Если мы прошли по всем свободным прямоугольникам в изображении и никуда изображение не вошло ...
        else:
            # Возвращаем False
            return False
