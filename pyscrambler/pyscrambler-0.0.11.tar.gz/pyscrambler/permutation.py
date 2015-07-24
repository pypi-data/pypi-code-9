# -*- coding: utf-8 -*-
from __future__ import absolute_import

import itertools
import math

from oset import oset


def permute(length=8, n=0, wrap_around=False):
    """
    Return an oset (ordered set) of integers representing permutation n,
    size of length.

    If wrap_around is set to True, if n is bigger than !length, then this
    function will return permutation n modulo !length
    (simulates going full circle).
    """
    # sanity-checking
    if not n >= 0:
        raise ValueError('Invalid permutation argument: ' + str(n))
    if not isinstance(length, int):
        raise ValueError('Expected integer for permutation length')
    if not isinstance(n, int):
        raise ValueError('Expected integer for permutation count')
    set_length = math.factorial(length)
    if n > (set_length - 1):
        if wrap_around:
            n %= set_length
        else:
            raise ValueError('Requested permutation number beyond the range '
                             'of this permutation set, and wrap_around is set '
                             'to False.')
    '''
    Efficiency: if n is greater than half of set_length then reverse the
    iteration list and iterate backwards:
    '''
    if n > (set_length / 2):
        # retrieve a permutation iterator of reversed array:
        p = itertools.permutations(reversed([i for i in range(0, length)]))
        # count backwards
        count = (set_length - 1)
        inc = -1
    else:
        # retrieve a permutation iterator of forwards array:
        p = itertools.permutations([i for i in range(0, length)])
        # count forwards
        count = 0
        inc = 1

    # iterate backwards or forwards until the correct permutation is found:
    for result in p:
        if count == n:
            return oset(result)
        else:
            count += inc
