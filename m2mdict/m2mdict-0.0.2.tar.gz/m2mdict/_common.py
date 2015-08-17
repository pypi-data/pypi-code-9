# -*- coding: utf-8 -*-
from collections import Mapping
from util import parse, check_args

__author__ = 'dengjing'


class M2mMapping(Mapping):
    """
    有向多对多关系基本模式
    生成形式 mm = M2mMapping([("img/x-jpeg": "jpg"), ("img/jpeg": "jpg")])
    """
    rdefault = {}
    ldefault = {}

    def __init__(self, *args, **kwargs):
        check_args(*args, **kwargs)
        self._fmap = {}
        self._bmap = {}
        self._rawmap = args[0]
        self._rflag = False
        self._fmap = parse(args, flag=self._rflag)
        self._bmap = parse(args, flag=not self._rflag)

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self._fmap)

    def __getitem__(self, key):
        if key:
            if self._rflag:
                return self._bmap[key]
            else:
                return self._fmap[key]

    __str__ = __repr__

    # it will be override
    __len__ = lambda self: len(self._fmap)
    __iter__ = lambda self: iter(self._rawmap)

    def __invert__(self):
        """
        Called when the unary inverse operator (~) is applied.
        """
        if self._rflag:
            self._rflag = not self._rflag
            return self._bmap
        else:
            self._rflag = not self._rflag
            return self._fmap
