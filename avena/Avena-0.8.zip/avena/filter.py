#!/usr/bin/env python

'''Spatial filtering of image arrays with the FFT'''


from functools import partial
from numpy import (
    array as _array,
    multiply as _multiply,
    real as _real,
    vectorize as _vectorize,
)
from numpy.fft import (
    fftshift as _fftshift,
    ifftshift as _ifftshift,
    irfft2 as _irfft2,
    rfft2 as _rfft2,
)

from . import image


def __in_circle(a, b, r, coords):
    x, y = coords
    d = (x - a) ** 2 + (y - b) ** 2
    if d < r ** 2:
        return 1.0
    else:
        return 0.0


def _indices_array(shape):
    m, n = shape
    indices = _array(
        [[(i, j) for j in range(n)] for i in range(m)],
        dtype=('f4,f4'),
    )
    return indices


def _low_pass_filter(shape, radius):
    m, n = shape
    indices = _indices_array(shape)
    _in_circle = partial(__in_circle, m // 2, n // 2, radius)
    _v_in_circle = _vectorize(_in_circle)
    return _v_in_circle(indices)


def _high_pass_filter(shape, radius):
    return 1.0 - _low_pass_filter(shape, radius)


def _filter(filter, array):
    X = _rfft2(array)
    X = _fftshift(X)
    _multiply(X, filter, out=X)
    X = _ifftshift(X)
    x = _irfft2(X, s=array.shape)
    x = _real(x)
    return x


def _rshape(shape):
    m, n = shape
    if n % 2 == 0:
        return (m, (n // 2) + 1)
    else:
        return (m, (n + 1) // 2)


def _lowpass(radius, array):
    rfilter = _low_pass_filter(_rshape(array.shape), radius)
    return _filter(rfilter, array)


def lowpass(img, radius):
    '''Apply a 2D low-pass filter to an image array.'''
    return image.map_to_channels(
        partial(_lowpass, radius),
        lambda shape: shape,
        img,
    )


def _highpass(radius, array):
    rfilter = _high_pass_filter(_rshape(array.shape), radius)
    return _filter(rfilter, array)


def highpass(img, radius):
    '''Apply a 2D high-pass filter to an image array.'''
    return image.map_to_channels(
        partial(_highpass, radius),
        lambda shape: shape,
        img,
    )


if __name__ == '__main__':
    pass
