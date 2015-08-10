# coding: utf-8
"""Utilities for vector computation."""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import math


def mag_squared(vals):
    """Get the magnitude squared of the given iterable.

    In other words, get the sum of the squares of all values in vals.

    """
    return sum(v**2 for v in vals)


def mag(vals):
    """Get the magnitude of the given iterable."""
    return math.sqrt(mag_squared(vals))
