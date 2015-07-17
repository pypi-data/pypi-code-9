# -*- coding: utf-8 -*-
#
#   Copyright 2015 Grigoriy Kramarenko <root@rosix.ru>
#
#   This file is part of RosixDocs.
#

class AbstractClass(object):
    """
    Использование класса::

        a = AbstractClass()

        print a.test()

    """

    attr = 'атрибут класса'

    def test(self, s='test class'):
        """
        Метод печатает строку на стандартный вывод.
        """

        print(s)

    @property
    def field(self):
        """
        Возвращает свойство экземпляра.
        """

        print(self.attr)


def testfunc(s='test func'):
    """
    Функция печатает строку на стандартный вывод.
    """

    print(s)

