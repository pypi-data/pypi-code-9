# -*- coding: utf-8 -*-
from collections import Mapping
from util import parse, check_args

__author__ = 'dengjing'


class M2mMapping(Mapping):
    """
    有向多对多关系基本模式
    生成形式 mm = M2mMapping([("img/x-jpeg": "jpg"), ("img/jpeg": "jpg")])
    """
    def __init__(self, *args, **kwargs):
        check_args(*args, **kwargs)
        self._fmap = {}
        self._bmap = {}
        self._fmap = parse(args, flag=False)
        self._bmap = parse(args, flag=True)
        inv = object.__new__(self.__class__)
        inv._fmap = self._bmap
        inv._bmap = self._fmap
        inv._inv = self
        self._inv = inv

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self._fmap)

    def __getitem__(self, key):
        if key:
            return self._fmap[key]

    __str__ = __repr__

    # it will be override
    __len__ = lambda self: len(self._fmap)
    __iter__ = lambda self: iter(self._rawmap)

    def __invert__(self):
        """
        Called when the unary inverse operator (~) is applied.
        """
        return self._inv
