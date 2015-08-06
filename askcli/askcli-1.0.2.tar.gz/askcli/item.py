# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

class Item(object):

    key = ''
    txt = ''
    activate = False

    def __init__(self, key, txt, activate=False):
        """
        :param str key: clef de l'item.
        :param str txt: text de l'item
        """
        self.key = str(key)
        self.txt = str(txt)
        self.activate = bool(activate)

    def __repr__(self):
        """
        :rtype: str
        :return: representation de l'objet
        """
        return "<askcli.Item : {0} - {1}>".format(self.key, self.txt)

    def __str__(self):
        """
        :rtype: str
        :return: représentaion to string de l'objet
        """

        ret = "{0} - {1}".format(self.key, self.txt)
        if (self.activate):
            return ">{0}".format(ret)
        else:
            return " {0}".format(ret)

    def __eq__(self, other):
        """
        :param all other: objet à tester

        :return: si les objet sont égale. c'est à dire que les key sont égale
        :rtype: bool
        """


        try:
            return (str(self.key) == str(other.key))
        except Exception:
            return False


# english
 
YES = Item('Y', 'Yes')
NO = Item('N', 'No')

# french

OUI = Item('O', 'Oui')
NON = Item('N', 'Non')