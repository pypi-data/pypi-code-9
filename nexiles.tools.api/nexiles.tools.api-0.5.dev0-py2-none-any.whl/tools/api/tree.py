# -*- coding: utf-8 -*-
#
# File: tree.py
#
# Copyright (c) nexiles GmbH
#

__author__    = """Stefan Eletzhofer <se@nexiles.de>"""
__docformat__ = 'plaintext'
__revision__  = "$Revision: $"
__version__   = '$Revision: $'[11:-2]


import logging

logger = logging.getLogger("nexiles.tools.api")

__all__ = ["Tree"]


VALID_SET = set("=()&%$§/\"'")


class Tree(dict):
    """
    A simple Tree-like object.

    https://gist.github.com/2012250
    http://stackoverflow.com/questions/6780952/how-to-change-behavior-of-dict-for-an-instance
    """

    def __valid_key__(self, key):
        if key.startswith("_"):
            return False

        if VALID_SET & set(key):
            return False

        if "=" in key:
            return False

        return True

    def __missing__(self, key):
        if key.startswith("_"):
            return
        value = self[key] = type(self)()
        return value

    def __getattr__(self, key):
        if key in self:
            item = self[key]
            if type(item) == dict:
                return type(self)(self[key])
            else:
                return item
        else:
            if self.__valid_key__(key):
                return self.__missing__(key)
            raise AttributeError(key)

    def __setattr__(self, key, value):
        if not self.__valid_key__(key):
            raise AttributeError(key)
        self[key] = value


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)

# vim: set ft=python ts=4 sw=4 expandtab :
