#!usr/bin/env python
"""A set of utility functions for the planners.
"""
import numpy as np


def is_shape(s):
    # If it's not a tuple, it's not a shape
    if not isinstance(s, tuple):
        return False

    # If any value is not an int, it's not a shape
    for dimension in s:
        if not dimension == int(dimension):
            return False

    # Otherwise it's a shape
    return True


def get_shape(a):
    # If it's already a shape, just return it
    if is_shape(a):
        return a

    # If it's a numpy array, it's simple
    try:
        return a.shape
    except AttributeError:
        pass

    # If not, let's see if it's a number
    try:
        # noinspection PyRedundantParentheses
        return (int(a),)
    except (ValueError, TypeError):
        pass

    # Finally, let's try to make it an array
    return np.asarray(a).shape


def get_segment_axis(shape, axis, s_axis):
    axis = len(shape) + axis if axis < 0 else axis
    s_axis = len(shape) + s_axis if s_axis < 0 else s_axis
    if s_axis < axis:
        return axis - 1
    else:
        return axis


def compute_nfft(n_filter, n_signal):
    # Verify that n_filter and n_signal are positive numbers
    n_ok = type(n_filter) in (int, float) and n_filter > 0
    n_x_ok = type(n_signal) in (int, float) and n_signal > 0
    if not (n_ok and n_x_ok):
        raise ValueError("n_filter and n_signal must be positive numbers")
    if n_filter > n_signal:
        return 2**np.ceil(np.log2(n_filter+n_signal-1))
    else:
        fft_flops = np.array([18, 59, 138, 303, 660, 1441, 3150, 6875,
                              14952, 32373, 69762, 149647, 319644, 680105,
                              1441974, 3047619, 6422736, 13500637,
                              28311786, 59244791])
        # noinspection PyTypeChecker
        nfft_list = np.power(2, np.arange(np.ceil(np.log2(n_filter)), 21))
        # noinspection PyTypeChecker
        fft_flops = fft_flops[-len(nfft_list):]
        l_list = nfft_list - (n_filter - 1)
        min_idx = np.argmin(np.ceil(n_signal/l_list) * fft_flops)
        return int(nfft_list[min_idx])


def pad_array(a, shape):
    pads = [(0, x - y) for x, y in zip(shape, a.shape)]
    return np.pad(a, pads, mode='constant', constant_values=0)


def expand_me(a, axis, ndim):
    # Validate axis and make it absolute if needed
    if axis >= ndim:
        raise ValueError("Target axis must be within dimensions.")
    elif axis < 0:
        axis += ndim

    # Add leading dimensions
    for k in range(axis):
        a = np.expand_dims(a, 0)

    # Add trailing dimensions
    for k in range(axis+1, ndim):
        a = np.expand_dims(a, -1)

    return a
