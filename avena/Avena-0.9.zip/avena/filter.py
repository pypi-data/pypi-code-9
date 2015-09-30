#!/usr/bin/env python

'''Spatial filtering of image arrays with the FFT'''


from functools import partial
from numpy import (
    float32 as _float32,
    indices as _indices,
    multiply as _multiply,
)
from numpy.fft import (
    fftshift as _fftshift,
    ifftshift as _ifftshift,
    irfft2 as _irfft2,
    rfft2 as _rfft2,
)

from . import image


def _low_pass_filter(shape, radius):
    m, n = shape
    a, b = m // 2, n // 2
    i = _indices((m, n), dtype=_float32)
    rows, columns = i[0, :], i[1, :]
    d = (rows - a) ** 2 + (columns - b) ** 2
    d[d < radius ** 2] = 1.0
    d[d >= radius ** 2] = 0.0
    return d


def _high_pass_filter(shape, radius):
    return 1.0 - _low_pass_filter(shape, radius)


def _filter(filter, array):
    X = _rfft2(array)
    X = _fftshift(X)
    _multiply(X, filter, out=X)
    X = _ifftshift(X)
    x = _irfft2(X, s=array.shape)
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
