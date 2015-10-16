#!/usr/bin/env python

"""Translation of image arrays."""


from functools import partial
from numpy import zeros as _zeros

from . import image


def _translate(coords, array):
    m, n = array.shape
    a, b = coords
    p, q = m - abs(a), n - abs(b)
    z = _zeros((m, n), dtype=array.dtype)
    i, j = max(0, a), max(0, b)
    dst = z[i:(i + p), j:(j + q)]
    i, j = max(0, -a), max(0, -b)
    src = array[i:(i + p), j:(j + q)]
    dst[:] = src[:]
    return z


def translate(img, coords):
    """Translate an image array by the given coordinates."""
    return image.map_to_channels(
        partial(_translate, coords),
        lambda shape: shape,
        img,
    )


if __name__ == '__main__':
    pass
