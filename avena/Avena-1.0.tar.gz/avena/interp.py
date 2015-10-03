#!/usr/bin/env python

'''Interpolation of image arrays in the frequency domain'''


from functools import partial
from numpy import (
    ceil as _ceil,
    complex64 as _complex64,
    multiply as _multiply,
    real as _real,
    sqrt as _sqrt,
    zeros as _zeros,
)
from numpy.fft import (
    fft2 as _fft2,
    ifft2 as _ifft2,
    fftshift as _fftshift,
    ifftshift as _ifftshift,
)

from . import filter, image, tile


def _interp2_shape(factor, shape):
    m, n = shape
    p, q = int(m * factor), int(n * factor)
    return (p, q)


def _mirror(array):
    m, n = array.shape
    r = int(_ceil(_sqrt((m / 2.0) ** 2 + (n / 2.0) ** 2)))
    x = tile._tile9_periodic(array)
    f = filter._low_pass_filter(x.shape, r)
    _multiply(x, f, out=x)
    i, j = (3 * m - 2 * r) // 2, (3 * n - 2 * r) // 2
    z = x[i:(i + 2 * r), j:(j + 2 * r)]
    return z


def _interp2(factor, array):
    x = _mirror(array)
    m, n = x.shape
    p, q = _interp2_shape(factor, (m, n))
    X = _fft2(x)
    X = _fftshift(X)
    Z = _zeros((p, q), dtype=_complex64)
    i, j = (p - m) // 2, (q - n) // 2
    Z[i:(i + m), j:(j + n)] = X[:, :]
    Z = _ifftshift(Z)
    z = _ifft2(Z, s=(p, q))
    z = _real(z)
    m, n = _interp2_shape(factor, array.shape)
    i, j = int(_ceil((p - m) / 2.0)), int(_ceil((q - n) / 2.0))
    z = z[i:(i + m), j:(j + n)]
    return z


def interp2(img, factor):
    '''Interpolate a 2D image array by a given factor.'''
    return image.map_to_channels(
        partial(_interp2, factor),
        lambda shape: _interp2_shape(factor, shape),
        img,
    )


if '__main__' in __name__:
    pass
