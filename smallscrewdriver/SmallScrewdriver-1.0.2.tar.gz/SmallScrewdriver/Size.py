# encoding: utf8


# noinspection PyPep8Naming
class Size(object):
    def __init__(self, width=0, height=0):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def __eq__(self, other):
        return self.width == other.width and self.height == other.height

    def __ne__(self, other):
        return self.width != other.width or self.height != other.height

    def __lt__(self, other):
        return self.width < other.width and self.height < other.height

    def __le__(self, other):
        raise TypeError("can not have less then equal operator")
        # return self.width <= other.width and self.height <= other.height

    def __gt__(self, other):
        raise TypeError("can not have greater operator")
        # return self.width > other.width and self.height > other.height

    def __ge__(self, other):
        raise TypeError("can not have greater then equal operator")
        # return self.width >= other.width or self.height >= other.height

    def canInscribe(self, other):
        """
        Моежт ли этот размер вписать другой под 0 градусов или 90 градусов
        :param other: проверяемый размер
        :return: True если может
        False если нет
        """
        return other.less(self) == (True, True) or other.less(Size(self.height, self.width)) == (True, True)

    def less(self, other):
        """
        Определяет меньше для каждой из двух сторон
        :rtype : bool
        """
        return self.width < other.width, self.height < other.height

    def equal(self, other):
        return self.width == other.width, self.height == other.height

    def rotate(self):
        return Size(self.height, self.width)

    def __str__(self):
        return '{}({}, {})'.format(self.__class__.__name__, self.width, self.height)

    def __repr__(self):
        return self.__str__()
