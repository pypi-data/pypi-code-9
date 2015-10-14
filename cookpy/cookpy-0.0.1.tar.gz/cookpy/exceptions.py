# -*- coding: utf-8 -*-


class CookpyException(Exception):
    pass


class NoSourcesError(CookpyException):
    def __init__(self, target):
        self.target = target
