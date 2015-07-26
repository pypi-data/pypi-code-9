# -*- coding: utf-8 -*-
from __future__ import absolute_import

import bitstring


def bits_to_group(array, size):
    """
    Convert a bitstring.BitArray or array of individual bits to an array
    of groups of bits of a given size.

    Raises exception if the length of the array is not a multiple of the
    given group size.
    """
    # first it it's an array of bitarrays then assemble items into one bitarray
    if hasattr(array, '__iter__'):
        bits = bitstring.BitArray()
        for item in array:
            bits += item
    else:
        bits = bitstring.BitArray(array)
    # sanity checking
    if len(bits) % size != 0:
        raise ValueError('The given BitArray or array instance size is not '
                         'a multiple of the given group size.')
    result = []
    for index in range(len(bits))[::size]:
        result.append(bits[index:index+size])
    return result
