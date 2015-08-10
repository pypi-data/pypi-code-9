# coding: utf-8
"""Similarity functions for recommendation calculations."""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

try:
    from itertools import izip
except ImportError:  # pragma: no cover
    izip = zip  # In Python 3, izip is removed because zip does the same job.

from . import vec_util


def dot_product(data_a, data_b):
    """Get the dot product between two lists."""
    all_pairs = izip(data_a, data_b)
    return sum(a * b for a, b in all_pairs)


def cosine(data_a, data_b):
    """Similarity between data_a and data_b using cosine."""
    denom = vec_util.mag(data_a) * vec_util.mag(data_b)
    if denom:
        return dot_product(data_a, data_b) / denom
    else:
        return 0


def sorensen(data_a, data_b):
    """Get the Sørensen–Dice coefficient of data_a and data_b."""
    denom = (vec_util.mag_squared(data_a) +
             vec_util.mag_squared(data_b))

    if denom != 0:
        return 2 * dot_product(data_a, data_b) / denom
    else:
        return 0
