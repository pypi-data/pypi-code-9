#!/usr/bin/env python

'''Cross-correlation of image arrays'''


from numpy import (
    multiply as _multiply,
    ones as _ones,
    sqrt as _sqrt,
    zeros as _zeros,
)
from numpy.fft import (
    fftshift as _fftshift,
    ifftshift as _ifftshift,
    rfft2 as _rfft2,
    irfft2 as _irfft2,
)

from . import filter, image, tile


_DETREND_FACTOR = 0.10


def _detrend_filter(array):
    m, n = array.shape
    r = int(_sqrt(m * n) * _DETREND_FACTOR)
    f = filter._high_pass_filter((m, n), r)
    _multiply(array, f, out=array)


def _zeropad(array, size):
    m, n = array.shape
    p, q = size
    z = _zeros((p, q), dtype=array.dtype)
    z[:m, :n] = array
    return z


def _xcor2_shape(shapes):
    shape1, shape2 = shapes
    a, b = shape1
    c, d = shape2
    return (a + c, b + d)


def _center(array, shape):
    m, n = array.shape
    a, b = shape
    i, j = (m - a) // 2, (n - b) // 2
    return array[i:(i + a), j:(j + b)]


def _xcor2(array1, array2):
    x = tile.tile9_periodic(array1)
    a, b = x.shape
    y = array2[::-1, ::-1]
    c, d = y.shape
    m, n = _xcor2_shape(((a, b), (c, d)))
    x = _zeropad(x, (m, n))
    y = _zeropad(y, (m, n))
    X = _rfft2(x)
    Y = _rfft2(y)
    X = _fftshift(X)
    Y = _fftshift(Y)
    _detrend_filter(X)
    _detrend_filter(Y)
    _multiply(X, Y, out=X)
    X = _ifftshift(X)
    x = _irfft2(X, s=(m, n))
    z = _center(x, (a // 3 + c, b // 3 + d))
    z = _center(z, (a // 3, b // 3))
    return z


def xcor2(array1, array2):
    '''Compute the cross-correlation of two image arrays.'''
    z = _ones(array1.shape[:2])
    channel_pairs = list(zip(
        image.get_channels(array1),
        image.get_channels(array2),
    ))
    for (xi, yi) in channel_pairs:
        xcori = _xcor2(xi, yi)
        _multiply(z, xcori, out=z)
    return z


if __name__ == '__main__':
    pass
