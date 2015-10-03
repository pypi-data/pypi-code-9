#!/usr/bin/env python

from numpy import (
    argmax as _argmax,
    around as _around,
    empty as _empty,
    mean as _mean,
    std as _std,
    unravel_index as _unravel_index,
)
from numpy import (
    int8 as _int8,
    int16 as _int16,
    int32 as _int32,
    int64 as _int64,
    uint8 as _uint8,
    uint16 as _uint16,
    uint32 as _uint32,
    uint64 as _uint64,
    float32 as _float32,
    float64 as _float64,
)
from sys import float_info as _float_info


_eps = 10.0 * _float_info.epsilon

# Map of NumPy array type strings to types
_np_dtypes = {
    'int8':     _int8,
    'int16':    _int16,
    'int32':    _int32,
    'int64':    _int64,
    'uint8':    _uint8,
    'uint16':   _uint16,
    'uint32':   _uint32,
    'uint64':   _uint64,
    'float32':  _float32,
    'float64':  _float64,
}


_dtype_bounds = {
    'float32':  (0.0, 1.0),
    'float64':  (0.0, 1.0),
    'uint8':    (0, 255),
}


def from_uint8(array):
    float_array = array.astype(_float32)
    float_array *= 1.0 / 256.0
    return float_array


def to_uint8(array):
    uint8_array = _empty(array.shape, dtype=_uint8)
    _around(array * 255, out=uint8_array)
    return uint8_array


def clip(array, bounds):
    '''Clip the values of an array to the given interval.'''
    (min, max) = bounds
    x = array < min + _eps
    y = array > max - _eps
    array[x] = min
    array[y] = max
    return


def normalize(array):
    '''Normalize an array to the interval [0,1].'''
    mu = _mean(array)
    rho2 = _std(array)
    min = mu - 1.5 * rho2
    max = mu + 1.5 * rho2
    array -= min
    if max - min > _eps:
        array /= max - min
    return


def peak(array):
    '''Return the index of the peak value of an array.'''
    return _unravel_index(_argmax(array), array.shape)


if __name__ == '__main__':
    pass
