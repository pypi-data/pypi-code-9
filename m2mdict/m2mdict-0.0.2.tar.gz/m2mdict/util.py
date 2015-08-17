# -*- coding: utf-8 -*-
from collections import defaultdict

__author__ = 'dengjing'


iteritems = lambda x: iter(x)


def parse(args, flag=False):
    """
    将参数装换到（k --> set(v)）的形式 d.items()
    [('blue', set([2, 4])), ('red', set([1])), ('yellow', set([1, 3]))]
    """
    args = args[0]
    if isinstance(args, list):
        d = defaultdict(set)
        if not flag:
            for k, v in args:
                d[k].add(v)
        else:
            for k, v in args:
                d[v].add(k)
        return d
    else:
        raise TypeError('expected the argument is list')


def check_args(*args, **kwargs):
    if kwargs:
        raise TypeError('there is no need to get kw')
    if args:
        l = len(args)
        if l != 1:
            raise TypeError('expected at most 1 argument, got %d' % l)
        list_or_err = args[0]
        if isinstance(list_or_err, list):
            pass
        else:
            raise TypeError('expected the argument is list')


def reverse(args):
    if isinstance(args, list):
        for (k, v) in args:
            yield (v, k)