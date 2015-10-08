#!usr/bin/env python
"""This module contains planner functions for fast FFT and other FFT-based
computations with pyFFTW.
"""

# Future improvements: Neater firfilter using the fft planners
#                      IIR filtering?
#                      Convolution (same as correlate just without reversing y)
#                      Pwelch

import pyfftw
import numpy as np

from . import _utils


def fft(a, nfft=None, axis=-1, fft_pair=False, crop_ifft=False):
    """Returns a planned function that computes the 1-D DFT of a sequence or
    array.

    Parameters
    ----------
        a : number, shape or array-like
            An input array, its shape or length.
        nfft : Optional[int]
            Number of FFT points. Default is input size along specified axis
        axis : Optional[int]
            Axis along which to perform the fft. Default is -1.
        fft_pair : Optional[boolean]
            Indicates Whether or not to also return an ifft function. Default
            is False.
        crop_ifft : Optional[boolean]
            Indicates whether the planned ifft function should crop its output
            to match input size. Default is False.

    Returns
    -------
        planned_fft(x)
            Planned fft function.
        planned_ifft(x)
            Planned ifft function. Returned if fft_pair is True.
    """
    # Get shape
    shape = _utils.get_shape(a)
    n = shape[axis]

    # Set up slices and pyfftw shapes
    n_dim = len(shape)
    slices = [slice(None)] * n_dim

    if nfft is None:
        nfft = shape[axis]
    else:
        shape = list(shape)
        shape[axis] = nfft

    # Set data type
    if np.asarray(a).dtype.name in ('float32', 'int32'):
        dtype = 'complex64'
    else:
        dtype = 'complex128'

    # Set up input and output arrays and FFT object
    u = pyfftw.n_byte_align_empty(shape, 16, dtype)
    v = pyfftw.n_byte_align_empty(shape, 16, dtype)
    fft_obj = pyfftw.FFTW(u, v, direction='FFTW_FORWARD', axes=(axis,))

    # Define fft function
    if n == nfft:
        def planned_fft(x):
            u[:] = x
            return fft_obj().copy()

    elif n < nfft:
        def planned_fft(x):
            u[:] = _utils.pad_array(x, shape)
            return fft_obj().copy()

    else:
        slices[axis] = slice(0, nfft)

        def planned_fft(x):
            u[:] = x[slices]
            return fft_obj().copy()

    # Define ifft function
    if fft_pair is True:
        ifft_obj = pyfftw.FFTW(v, u, direction='FFTW_BACKWARD', axes=(axis,))

        if n > nfft:
            raise ValueError("NFFT must be at least equal to signal length "
                             "when returning an FFT pair.")

        elif n < nfft and crop_ifft:
            slices[axis] = slice(None, n)

            def planned_ifft(x):
                v[:] = x
                return ifft_obj().copy()[slices]

        else:
            def planned_ifft(x):
                v[:] = x
                return ifft_obj().copy()

        return planned_fft, planned_ifft

    else:
        return planned_fft


def rfft(a, nfft=None, axis=-1, fft_pair=False, crop_ifft=False):
    """Returns a planned function that computes the 1-D DFT of a real-valued
    sequence or array.

    Parameters
    ----------
        a : number, shape or array-like
            An input array, its shape or length.
        nfft : Optional[int]
            Number of FFT points. Default is input size along specified axis
        axis : Optional[int]
            Axis along which to perform the fft. Default is -1.
        fft_pair : Optional[boolean]
            Indicates Whether or not to also return an ifft function. Default
            is False.
        crop_ifft : Optional[boolean]
            Indicates whether the planned ifft function should crop its output
            to match input size. Default is False.

    Returns
    -------
        planned_rfft(x)
            Planned fft function.
        planned_irfft(x)
            Planned ifft function. Returned if fft_pair is True.
    """
    # Get shape
    a_shape = _utils.get_shape(a)
    n = a_shape[axis]

    # Set up slices and pyfftw shapes
    n_dim = len(a_shape)
    slices = [slice(None)] * n_dim

    if nfft is None:
        nfft = a_shape[axis]

    u_shape = list(a_shape)
    v_shape = list(a_shape)
    u_shape[axis] = nfft
    v_shape[axis] = nfft//2 + 1

    # Set data types
    if np.asarray(a).dtype.name == 'float32':
        dtype = 'float32'
        fft_dtype = 'complex64'
    else:
        dtype = 'float64'
        fft_dtype = 'complex128'

    u = pyfftw.n_byte_align_empty(u_shape, 16, dtype)
    v = pyfftw.n_byte_align_empty(v_shape, 16, fft_dtype)
    fft_obj = pyfftw.FFTW(u, v, direction='FFTW_FORWARD', axes=(axis,))

    # Define fft function
    if n == nfft:
        def planned_rfft(x):
            u[:] = x
            return fft_obj().copy()

    elif n < nfft:
        def planned_rfft(x):
            u[:] = _utils.pad_array(x, u_shape)
            return fft_obj().copy()

    else:
        slices[axis] = slice(0, nfft)

        def planned_rfft(x):
            u[:] = x[slices]
            return fft_obj().copy()

    # Define ifft function
    if fft_pair is True:
        ifft_obj = pyfftw.FFTW(v, u, direction='FFTW_BACKWARD', axes=(axis,))

        if n > nfft:
            raise ValueError("NFFT must be at least equal to signal length "
                             "when returning an FFT pair.")

        elif n < nfft and crop_ifft:
            slices[axis] = slice(None, n)

            def planned_irfft(x):
                v[:] = x
                return ifft_obj().copy()[slices]

        else:
            def planned_irfft(x):
                v[:] = x
                return ifft_obj().copy()

        return planned_rfft, planned_irfft

    else:
        return planned_rfft


def fftn(a, shape=None, axes=None, fft_pair=False, crop_ifft=False):
    """Returns a planned function that computes the N-D DFT of an array.

    Parameters
    ----------
        a : array-like or shape
            An input array or its shape
        nfft : Optional[sequence of ints]
            Number of FFT points. Default is input size along specified axes
        axes : Optional[sequence of ints]
            Axes along which to perform the fft. Default is all axes.
        fft_pair : Optional[boolean]
            Indicates Whether or not to also return an ifft function. Default
            is False.
        crop_ifft : Optional[boolean]
            Indicates whether the planned ifft function should crop its output
            to match input size. Default is False.

    Returns
    -------
        planned_fftn(x)
            Planned fft function.
        planned_ifftn(x)
            Planned ifft function. Returned if fft_pair is True.
    """
    # Get shape of input
    a_shape = _utils.get_shape(a)
    n_dim = len(a_shape)

    if shape is None:
        if axes is None:
            shape = a_shape
        else:
            shape = [a_shape[axis] for axis in axes]

    if axes is None:
        n_dim_s = len(shape)
        dim_diff = n_dim - n_dim_s
        axes = [k + dim_diff for k in range(n_dim_s)]

    # Make sure axes and shape are iterable
    if np.asarray(axes).ndim == 0:
        axes = (axes,)
    if np.asarray(shape).ndim == 0:
        shape = (shape,)

    # Compute FFTW shape
    fft_shape = list(a_shape)
    for n, axis in zip(range(len(axes)), axes):
        fft_shape[axis] = shape[n]

    # Set up slices
    slices = [slice(None)] * n_dim
    for axis in axes:
        slices[axis] = slice(0, fft_shape[axis])

    # Set data type
    if np.asarray(a).dtype.name in ('float32', 'int32'):
        dtype = 'complex64'
    else:
        dtype = 'complex128'

    print(fft_shape)

    u = pyfftw.n_byte_align_empty(fft_shape, 16, dtype)
    v = pyfftw.n_byte_align_empty(fft_shape, 16, dtype)
    fft_obj = pyfftw.FFTW(u, v, direction="FFTW_FORWARD", axes=axes)

    has_smaller_axis = any(s1 < s2 for s1, s2 in zip(a_shape, fft_shape))
    has_larger_axis = any(s1 > s2 for s1, s2 in zip(a_shape, fft_shape))

    # Define fft function
    if has_smaller_axis and has_larger_axis:
        def planned_fftn(x):
            u[:] = _utils.pad_array(x[slices], fft_shape)
            return fft_obj().copy()

    elif has_larger_axis:
        def planned_fftn(x):
            u[:] = x[slices]
            return fft_obj().copy()

    elif has_smaller_axis:
        def planned_fftn(x):
            u[:] = _utils.pad_array(x, fft_shape)
            return fft_obj().copy()

    else:
        def planned_fftn(x):
            u[:] = x
            return fft_obj().copy()

    # Define ifftn function
    if fft_pair is True:
        ifft_obj = pyfftw.FFTW(v, u, direction='FFTW_BACKWARD', axes=axes)

        if has_larger_axis:
            raise ValueError("Number of FFT points must be equal to or greater"
                             "than the signal length for each axis when "
                             "returning an FFT pair")

        elif has_smaller_axis and crop_ifft:
            for axis in axes:
                slices[axis] = slice(0, a_shape[axis])

            def planned_ifftn(x):
                v[:] = x
                return ifft_obj().copy()[slices]
        else:
            def planned_ifftn(x):
                v[:] = x
                return ifft_obj().copy()

        return planned_fftn, planned_ifftn

    else:
        return planned_fftn


def rfftn(a, shape=None, axes=None, fft_pair=False, crop_ifft=False):
    """Returns a planned function that computes the N-D DFT of a real-valued
    array.

    Parameters
    ----------
        a : array-like or shape
            An input array or its shape.
        nfft : Optional[sequence of ints]
            Number of FFT points. Default is input size along specified axes
        axes : Optional[sequence of ints]
            Axes along which to perform the fft. Default is all axes.
        fft_pair : Optional[boolean]
            Indicates Whether or not to also return an ifft function. Default
            is False.
        crop_ifft : Optional[boolean]
            Indicates whether the planned ifft function should crop its output
            to match input size. Default is False.

    Returns
    -------
        planned_rfftn(x)
            Planned fft function.
        planned_irfftn(x)
            Planned ifft function. Returned if fft_pair is True.
    """
    # Get shape of input
    a_shape = _utils.get_shape(a)
    n_dim = len(a_shape)

    if shape is None:
        if axes is None:
            shape = a_shape
        else:
            shape = [a_shape[axis] for axis in axes]

    if axes is None:
        n_dim_s = len(shape)
        dim_diff = n_dim - n_dim_s
        axes = [k + dim_diff for k in range(n_dim_s)]

    # Make sure axes and shape are iterable
    if np.asarray(axes).ndim == 0:
        axes = (axes,)
    if np.asarray(shape).ndim == 0:
        shape = (shape,)

    # Compute FFTW shape
    u_shape = list(a_shape)
    v_shape = list(a_shape)

    for n, axis in zip(range(len(axes)), axes):
        u_shape[axis] = shape[n]
        v_shape[axis] = shape[n]

    v_shape[axes[-1]] = v_shape[axes[-1]]//2 + 1

    # Set up slices
    slices = [slice(None)] * n_dim
    for axis in axes:
        slices[axis] = slice(0, u_shape[axis])

    # Set data type
    if np.asarray(a).dtype.name in ('float32', 'int32'):
        dtype = 'float32'
        fft_dtype = 'complex64'
    else:
        dtype = 'float64'
        fft_dtype = 'complex128'

    u = pyfftw.n_byte_align_empty(u_shape, 16, dtype)
    v = pyfftw.n_byte_align_empty(v_shape, 16, fft_dtype)

    fft_obj = pyfftw.FFTW(u, v, direction="FFTW_FORWARD", axes=axes)

    has_smaller_axis = any(s1 < s2 for s1, s2 in zip(a_shape, u_shape))
    has_larger_axis = any(s1 > s2 for s1, s2 in zip(a_shape, u_shape))

    # Define fft function
    if has_smaller_axis and has_larger_axis:
        def planned_rfftn(x):
            u[:] = _utils.pad_array(x[slices], u_shape)
            return fft_obj().copy()

    elif has_larger_axis:
        def planned_rfftn(x):
            u[:] = x[slices]
            return fft_obj().copy()

    elif has_smaller_axis:
        def planned_rfftn(x):
            u[:] = _utils.pad_array(x, u_shape)
            return fft_obj().copy()

    else:
        def planned_rfftn(x):
            u[:] = x
            return fft_obj().copy()

    # Define ifftn function
    if fft_pair is True:
        ifft_obj = pyfftw.FFTW(v, u, direction='FFTW_BACKWARD', axes=axes)

        if has_larger_axis:
            raise ValueError("Number of FFT points must be equal to or greater"
                             "than the signal length for each axis when "
                             "returning an FFT pair")

        elif has_smaller_axis and crop_ifft:
            for axis in axes:
                slices[axis] = slice(0, a_shape[axis])

            def planned_irfftn(x):
                v[:] = x
                return ifft_obj().copy()[slices]
        else:
            def planned_irfftn(x):
                v[:] = x
                return ifft_obj().copy()

        return planned_rfftn, planned_irfftn

    else:
        return planned_rfftn


def ifft(a, nfft=None, axis=-1, fft_pair=False):
    """Returns a planned function that computes the 1-D inverse DFT of a
    sequence or array.

    Parameters
    ----------
        a : number, shape or array-like
            An input array, its shape or length.
        nfft : Optional[int]
            Number of FFT points. Default is input size along specified axis
        axis : Optional[int]
            Axis along which to perform the fft. Default is -1.
        fft_pair : Optional[boolean]
            Indicates Whether or not to also return an ifft function. Default
            is False.

    Returns
    -------
        planned_ifft(x)
            Planned ifft function.
        planned_fft(x)
            Planned fft function. Returned if fft_pair is True.
    """
    # Get shape
    shape = _utils.get_shape(a)
    n = shape[axis]

    # Set up slices and pyfftw shapes
    n_dim = len(shape)
    slices = [slice(None)] * n_dim

    if nfft is None:
        nfft = shape[axis]
    else:
        shape = list(shape)
        shape[axis] = nfft

    # Set data type
    if np.asarray(a).dtype.name in ('float32', 'int32', 'complex64'):
        dtype = 'complex64'
    else:
        dtype = 'complex128'

    # Set up input and output arrays and FFT object
    u = pyfftw.n_byte_align_empty(shape, 16, dtype)
    v = pyfftw.n_byte_align_empty(shape, 16, dtype)
    ifft_obj = pyfftw.FFTW(v, u, direction='FFTW_BACKWARD', axes=(axis,))

    # Define fft function
    if n == nfft:
        def planned_ifft(x):
            v[:] = x
            return ifft_obj().copy()

    elif n < nfft:
        def planned_ifft(x):
            v[:] = _utils.pad_array(x, shape)
            return ifft_obj().copy()

    else:
        slices[axis] = slice(0, nfft)

        def planned_ifft(x):
            v[:] = x[slices]
            return ifft_obj().copy()

    # Define fft function
    if fft_pair is True:
        fft_obj = pyfftw.FFTW(u, v, direction='FFTW_FORWARD', axes=(axis,))

        if n == nfft:
            def planned_fft(x):
                u[:] = x
                return fft_obj().copy()

        elif n < nfft:
            slices[axis] = n

            def planned_fft(x):
                u[:] = x
                return fft_obj().copy()[slices]

        else:
            raise ValueError("NFFT must be at least equal to signal length "
                             "when returning an FFT pair.")

        return planned_ifft, planned_fft

    else:
        return planned_ifft


def irfft(a, nfft=None, axis=-1, fft_pair=False):
    """Returns a planned function that computes the real-valued 1-D inverse DFT
    of a sequence or array.

    Parameters
    ----------
        a : number, shape or array-like
            An input array, its shape or length.
        nfft : Optional[int]
            Number of FFT points. Default is input size along specified axis
        axis : Optional[int]
            Axis along which to perform the fft. Default is -1.
        fft_pair : Optional[boolean]
            Indicates Whether or not to also return an ifft function. Default
            is False.

    Returns
    -------
        planned_irfft(x)
            Planned ifft function.
        planned_rfft(x)
            Planned fft function. Returned if fft_pair is True.
    """
    # Get shape
    shape = _utils.get_shape(a)
    n = 2*(shape[axis] - 1)

    # Set up slices and pyfftw shapes
    n_dim = len(shape)
    slices = [slice(None)] * n_dim

    if nfft is None:
        nfft = n

    nfft_complex = nfft//2 + 1

    u_shape = list(shape)
    v_shape = list(shape)
    u_shape[axis] = nfft
    v_shape[axis] = nfft_complex

    # Set data types
    if np.asarray(a).dtype.name in ('float32', 'int32', 'complex64'):
        dtype = 'float32'
        fft_dtype = 'complex64'
    else:
        dtype = 'float64'
        fft_dtype = 'complex128'

    # print(out_shape)
    # print(shape)
    u = pyfftw.n_byte_align_empty(u_shape, 16, dtype)
    v = pyfftw.n_byte_align_empty(v_shape, 16, fft_dtype)
    ifft_obj = pyfftw.FFTW(v, u, direction='FFTW_BACKWARD', axes=(axis,))

    # Define fft function
    if n == nfft:
        def planned_irfft(x):
            v[:] = x
            return ifft_obj().copy()

    elif n < nfft:
        def planned_irfft(x):
            v[:] = _utils.pad_array(x, v_shape)
            return ifft_obj().copy()

    else:
        slices[axis] = slice(0, nfft_complex)

        def planned_irfft(x):
            v[:] = x[slices]
            return ifft_obj().copy()

    # Define ifft function
    if fft_pair is True:
        fft_obj = pyfftw.FFTW(u, v, direction='FFTW_FORWARD', axes=(axis,))

        if n == nfft:
            def planned_rfft(x):
                u[:] = x
                return fft_obj().copy()

        elif n < nfft:
            slices[axis] = n

            def planned_rfft(x):
                u[:] = x
                return fft_obj().copy()[slices]

        else:
            raise ValueError("NFFT must be at least equal to signal length "
                             "when returning an FFT pair.")

        return planned_irfft, planned_rfft

    else:
        return planned_irfft


def ifftn(a, shape=None, axes=None, fft_pair=False):
    """Returns a planned function that computes the N-D DFT of an array.

    Parameters
    ----------
        a : array-like or shape
            An input array or its shape
        nfft : Optional[sequence of ints]
            Number of FFT points. Default is input size along specified axes
        axes : Optional[sequence of ints]
            Axes along which to perform the fft. Default is all axes.
        fft_pair : Optional[boolean]
            Indicates Whether or not to also return an ifft function. Default
            is False.

    Returns
    -------
        planned_fftn(x)
            Planned fft function.
        planned_ifftn(x)
            Planned ifft function. Returned if fft_pair is True.
    """
    # Get shape of input
    a_shape = _utils.get_shape(a)
    n_dim = len(a_shape)

    if shape is None:
        if axes is None:
            shape = a_shape
        else:
            shape = [a_shape[axis] for axis in axes]

    if axes is None:
        n_dim_s = len(shape)
        dim_diff = n_dim - n_dim_s
        axes = [k + dim_diff for k in range(n_dim_s)]

    # Make sure axes and shape are iterable
    if np.asarray(axes).ndim == 0:
        axes = (axes,)
    if np.asarray(shape).ndim == 0:
        shape = (shape,)

    # Compute FFTW shape
    fft_shape = list(a_shape)
    for n, axis in zip(range(len(axes)), axes):
        fft_shape[axis] = shape[n]

    # Set up slices
    slices = [slice(None)] * n_dim
    for axis in axes:
        slices[axis] = slice(0, fft_shape[axis])

    # Set data type
    if np.asarray(a).dtype.name in ('float32', 'int32', 'complex64'):
        dtype = 'complex64'
    else:
        dtype = 'complex128'

    print(fft_shape)

    u = pyfftw.n_byte_align_empty(fft_shape, 16, dtype)
    v = pyfftw.n_byte_align_empty(fft_shape, 16, dtype)
    ifft_obj = pyfftw.FFTW(v, u, direction='FFTW_BACKWARD', axes=axes)

    has_smaller_axis = any(s1 < s2 for s1, s2 in zip(a_shape, fft_shape))
    has_larger_axis = any(s1 > s2 for s1, s2 in zip(a_shape, fft_shape))

    # Define ifft function
    if has_smaller_axis and has_larger_axis:
        def planned_ifftn(x):
            v[:] = _utils.pad_array(x[slices], fft_shape)
            return ifft_obj().copy()

    elif has_larger_axis:
        def planned_ifftn(x):
            v[:] = x[slices]
            return ifft_obj().copy()

    elif has_smaller_axis:
        def planned_ifftn(x):
            v[:] = _utils.pad_array(x, fft_shape)
            return ifft_obj().copy()

    else:
        def planned_ifftn(x):
            v[:] = x
            return ifft_obj().copy()

    # Define fftn function
    if fft_pair is True:
        fft_obj = pyfftw.FFTW(u, v, direction="FFTW_FORWARD", axes=axes)

        if has_larger_axis:
            raise ValueError("Number of FFT points must be equal to or greater"
                             "than the signal length for each axis when "
                             "returning an FFT pair.")

        else:
            def planned_fftn(x):
                u[:] = x
                return fft_obj().copy()

        return planned_ifftn, planned_fftn

    else:
        return planned_ifftn


def irfftn(a, shape=None, axes=None, fft_pair=False):
    """Returns a planned function that computes the N-D DFT of a real-valued
    array.

    Parameters
    ----------
        a : array-like or shape
            An input array or its shape.
        nfft : Optional[sequence of ints]
            Number of FFT points. Default is input size along specified axes
        axes : Optional[sequence of ints]
            Axes along which to perform the fft. Default is all axes.
        fft_pair : Optional[boolean]
            Indicates Whether or not to also return an ifft function. Default
            is False.

    Returns
    -------
        planned_rfftn(x)
            Planned fft function.
        planned_irfftn(x)
            Planned ifft function. Returned if fft_pair is True.
    """
    # Get shape of input
    a_shape = _utils.get_shape(a)
    n_dim = len(a_shape)

    print(shape)
    print(axes)
    print(a_shape)
    if shape is None:
        if axes is None:
            shape = [n for n in a_shape]
            shape[-1] = 2*(shape[-1] - 1)
        else:
            shape = [a_shape[axis] for axis in axes]
            shape[axes[-1]] = 2*(shape[axes[-1]] - 1)
    else:
        shape = list(shape)

    if axes is None:
        n_dim_s = len(shape)
        dim_diff = n_dim - n_dim_s
        axes = [k + dim_diff for k in range(n_dim_s)]

    # Make sure axes and shape are iterable
    if np.asarray(axes).ndim == 0:
        axes = (axes,)
    if np.asarray(shape).ndim == 0:
        shape = (shape,)

    # Compute FFTW shape
    u_shape = list(a_shape)
    v_shape = list(a_shape)

    for n, axis in zip(range(len(axes)), axes):
        u_shape[axis] = shape[n]
        v_shape[axis] = shape[n]

    v_shape[axes[-1]] = v_shape[axes[-1]]//2 + 1

    # Set up slices
    slices = [slice(None)] * n_dim
    for axis in axes:
        slices[axis] = slice(0, v_shape[axis])

    # Set data types
    if np.asarray(a).dtype.name in ('float32', 'int32', 'complex64'):
        dtype = 'float32'
        fft_dtype = 'complex64'
    else:
        dtype = 'float64'
        fft_dtype = 'complex128'

    u = pyfftw.n_byte_align_empty(u_shape, 16, dtype)
    v = pyfftw.n_byte_align_empty(v_shape, 16, fft_dtype)
    ifft_obj = pyfftw.FFTW(v, u, direction='FFTW_BACKWARD', axes=axes)

    has_smaller_axis = any(s1 < s2 for s1, s2 in zip(a_shape, v_shape))
    has_larger_axis = any(s1 > s2 for s1, s2 in zip(a_shape, v_shape))

    # Define ifft function
    if has_smaller_axis and has_larger_axis:
        def planned_irfftn(x):
            v[:] = _utils.pad_array(x[slices], v_shape)
            return ifft_obj().copy()

    elif has_larger_axis:
        def planned_irfftn(x):
            v[:] = x[slices]
            return ifft_obj().copy()

    elif has_smaller_axis:
        def planned_irfftn(x):
            v[:] = _utils.pad_array(x, v_shape)
            return ifft_obj().copy()

    else:
        def planned_irfftn(x):
            v[:] = x
            return ifft_obj().copy()

    # Define ifftn function
    if fft_pair is True:
        fft_obj = pyfftw.FFTW(u, v, direction="FFTW_FORWARD", axes=axes)

        if has_larger_axis:
            raise ValueError("Number of FFT points must be equal to or greater"
                             "than the signal length for each axis when "
                             "returning an FFT pair")

        else:
            def planned_rfftn(x):
                u[:] = x
                return fft_obj().copy()

        return planned_irfftn, planned_rfftn

    else:
        return planned_irfftn


def firfilter(plan_b,
              plan_x,
              axis=-1,
              nfft=None,
              constant_signal=False,
              constant_filter=False,
              x_segmented=False,
              segments_axis=0):
    """Returns a planned function that filters a signal using the frequency
    domain overlap-and-add method with pyfftw.

    Parameters
    ----------
        plan_b : integer, shape or array-like
            A filter vector or its length or shape.
        plan_x : integer, shape or array-like
            A signal vector or its length or shape.
        axis : optional[int]
            Axis in plan_x along which the filter is applied.
        nfft : optional[int]
            FFT size. Default is selected for fastest computation based on
            signal and filter shapes.
        constant_signal : optional[boolean]
            Set to True if the signal is constant over all function calls and
            only the filter will change. Default is False.
        constant_filter : optional[boolean]
            Set to True if the filter is constant over all function calls and
            only the signal will change. Default is False.
        x_segmented : optional[boolean]
            Set to True if the signal is divided into segments along some axis
            and each segment is filtered on it's own multiple times. Default
            is False.
        segments_axis : optional[boolean]
            Axis along which segments are located. Default is 0.

    Returns
    -------
        function
            A planned FIR-filtering function.

    Raises
    ------
        ValueError
            If filter has more than one dimensions.
            If signal and filter are both constant.
            If signal is constant but not array-like.
            If filter is constant but not array-like.
            If signal is segmented but not constant.
    """

    # Get dimensions
    b_shape = _utils.get_shape(plan_b)
    x_shape = _utils.get_shape(plan_x)
    b_ndim = len(b_shape)
    x_ndim = len(x_shape)
    n_filter = b_shape[-1]
    n_signal = x_shape[axis]
    n_of_segments = x_shape[segments_axis]

    # ### Validate input
    # Check that plan_b has no more than one dimension
    if b_ndim > 2:
        raise ValueError("plan_b cannot have more than one dimension")
    elif b_ndim == 2 and not b_shape[0] == 1:
            raise ValueError("plan_b cannot have more than one dimension")

    # Having both a constant signal and a constant filter makes no sense
    if constant_signal and constant_filter:
        raise ValueError("signal and filter cannot both be constant.")

    # If signal is constant, plan_x must be actual data
    if constant_signal:
        # Make sure plan_x is a numpy array
        if not isinstance(plan_x, np.ndarray):
            try:
                plan_x = np.array(plan_x, dtype='float64')
            except ValueError:
                raise ValueError("plan_x must be array-like if constant_signal "
                                 "is True")

    # If filter is constant, plan_b must be an actual filter vector
    if constant_filter:
        # Make sure plan_b is a numpy array
        if not isinstance(plan_b, np.ndarray):
            try:
                plan_b = np.array(plan_b, dtype='float64')
            except ValueError:
                raise ValueError("plan_b must be array-like if constant_filter "
                                 "is True")

    # If plan_x is segmented, make sure plan_x has at least two dimensions
    if x_segmented:
        if x_ndim < 2:
            raise ValueError("A segmented signal must have at least two "
                             "dimensions")
        if not constant_signal:         # Should constant_signal be implied?
            raise ValueError("A segmented signal should also be constant.")

    # ### Find use_case
    if x_segmented:
        if x_ndim > 2:
            use_case = '3b'
        else:
            use_case = '3a'
    elif x_ndim > 1:
        if constant_filter:
            use_case = '2c'
        elif constant_signal:
            use_case = '2b'
        else:
            use_case = '2a'
    else:
        if constant_filter:
            use_case = '1c'
        elif constant_signal:
            use_case = '1b'
        else:
            use_case = '1a'

    # ### Compute nfft if not explicitly given
    try:
        nfft = int(nfft)
    except TypeError:
        nfft = _utils.compute_nfft(n_filter, n_signal)

    nfft_complex = nfft//2 + 1

    # ### Make pyfftw plans
    # define shapes
    u_shape = list(x_shape)
    v_shape = list(x_shape)
    y_shape = list(x_shape)
    u_shape[axis] = nfft
    v_shape[axis] = nfft_complex

    # Reduce by one dimension if plan_x contains segments
    if x_segmented:
        u_shape.pop(segments_axis)
        v_shape.pop(segments_axis)
        y_shape.pop(segments_axis)
        axis = _utils.get_segment_axis(x_shape, axis, segments_axis)

    # Create the arrays and objects
    u = pyfftw.n_byte_align_empty(u_shape, 16, 'float64')
    v = pyfftw.n_byte_align_empty(v_shape, 16, 'complex128')
    fft_obj = pyfftw.FFTW(u, v, direction='FFTW_FORWARD', axes=(axis,))
    ifft_obj = pyfftw.FFTW(v, u, direction='FFTW_BACKWARD', axes=(axis,))

    # ### Common preparations for multiple cases
    l = nfft - n_filter + 1

    t = list(range(len(u_shape)))
    t[axis], t[-1] = t[-1], t[axis]

    filter_expander = np.ones(u_shape).transpose(t)

    if use_case == '3b':
        slices = [slice(None)] * (x_ndim - 1)
    else:
        slices = [slice(None)] * x_ndim

    # ### Case 1a: 1-d signal
    if use_case == '1a':
        def planned_firfilter(b, x):
            """Filter data with a FIR filter.

            Parameters
            ----------
                b : array-like
                    A one-dimensional FIR filter array
                x : array-like
                    A one-dimensional input array

            Returns
            -------
                numpy.array
                    Filter output
            """
            # nfft-point FFT of filter once
            u[:] = np.hstack((b, np.zeros(nfft - n_filter)))
            b_fft = fft_obj().copy()

            y = np.zeros(y_shape)
            for k in range(0, n_signal, l):
                k_to = np.min((k + l, n_signal))
                u[:] = np.hstack((x[k:k_to], np.zeros(nfft - (k_to - k))))
                x_fft = fft_obj().copy()
                v[:] = x_fft * b_fft
                y_fft = ifft_obj().copy()
                y_to = np.min((n_signal, k + nfft))
                y[k:y_to] = y[k:y_to] + y_fft[:y_to - k].real

            return y

    # ### Case 1b: 1-d signal, constant signal
    elif use_case == '1b':
        # Pre-compute partial FFTs of x
        x_fft_list = []
        for k_0 in range(0, n_signal, l):
            k_0_to = np.min((k_0 + l, n_signal))
            u[:] = np.hstack((plan_x[k_0:k_0_to],
                              np.zeros(nfft - (k_0_to - k_0))))
            x_fft_list.append(fft_obj().copy())

        def planned_firfilter(b):
            """Filter constant data with a FIR filter.

            Parameters
            ----------
                b : array-like
                    A one-dimensional FIR filter array.

            Returns
            -------
                numpy.array
                    Filter output
            """
            # nfft-point FFT of filter once
            u[:] = np.hstack((b, np.zeros(nfft - n_filter)))
            b_fft = fft_obj().copy()

            y = np.zeros(y_shape)
            list_idx = 0
            for k in range(0, n_signal, l):
                v[:] = x_fft_list[list_idx] * b_fft
                y_fft = ifft_obj().copy()
                y_to = np.min((n_signal, k + nfft))
                y[k:y_to] = y[k:y_to] + y_fft[:y_to - k].real
                list_idx += 1

            return y

    # ### Case 1c: 1-d signal, constant filter
    elif use_case == '1c':
        u[:] = np.hstack((plan_b, np.zeros(nfft - n_filter)))
        bb_fft = fft_obj().copy()

        def planned_firfilter(x):
            """Filter data with a constant FIR filter.

            Parameters
            ----------
                x : array-like
                    A one-dimensional input array

            Returns
            -------
                numpy.array
                    Filter output
            """
            y = np.zeros(y_shape)
            for k in range(0, n_signal, l):
                k_to = np.min((k + l, n_signal))
                u[:] = np.hstack((x[k:k_to], np.zeros(nfft - (k_to - k))))
                x_fft = fft_obj().copy()
                v[:] = x_fft * bb_fft
                y_fft = ifft_obj().copy()
                y_to = np.min((n_signal, k + nfft))
                y[k:y_to] = y[k:y_to] + y_fft[:y_to - k].real

            return y

    # ### Case 2a: N-d signal
    elif use_case == '2a':
        def planned_firfilter(b, x):
            """Filter data with a FIR filter.

            Parameters
            ----------
                b : array-like
                    A one-dimensional FIR filter array
                x : array-like
                    An N-dimensional input array

            Returns
            -------
                numpy.array
                    Filter output
            """
            # nfft-point FFT of filter once
            b_padded = np.hstack((b, np.zeros(nfft - n_filter)))
            u[:] = (b_padded*filter_expander).transpose(t)
            b_fft = fft_obj().copy()

            y = np.zeros(y_shape)
            for k in range(0, n_signal, l):
                k_to = np.min((k + l, n_signal))
                slices[axis] = slice(k, k_to)
                u[:] = _utils.pad_array(x[slices], u_shape)
                x_fft = fft_obj().copy()
                v[:] = x_fft * b_fft
                y_to = np.min((n_signal, k + nfft))
                # noinspection PyTypeChecker
                slices[axis] = slice(None, y_to - k)
                y_fft = ifft_obj().copy()[slices]
                slices[axis] = slice(k, y_to)
                y[slices] = y[slices] + y_fft.real

            return y

    # ### Case 2b: N-d signal, constant signal
    elif use_case == '2b':
        # Pre-compute partial FFTs of x
        x_fft_list = []
        for k_0 in range(0, n_signal, l):
                k_0_to = np.min((k_0 + l, n_signal))
                slices[axis] = slice(k_0, k_0_to)
                u[:] = _utils.pad_array(plan_x[slices], u_shape)
                x_fft_list.append(fft_obj().copy())

        def planned_firfilter(b):
            """Filter static data with a FIR filter.

            Parameters
            ----------
                b : array-like
                    A one-dimensional FIR filter array.

            Returns
            -------
                numpy.array
                    Filter output
            """
            # nfft-point FFT of filter once
            b_padded = np.hstack((b, np.zeros(nfft - n_filter)))
            u[:] = (b_padded*filter_expander).transpose(t)
            b_fft = fft_obj().copy()

            y = np.zeros(y_shape)
            list_idx = 0
            for k in range(0, n_signal, l):
                v[:] = x_fft_list[list_idx] * b_fft
                y_to = np.min((n_signal, k + nfft))
                # noinspection PyTypeChecker
                slices[axis] = slice(None, y_to - k)
                y_fft = ifft_obj().copy()[slices]
                slices[axis] = slice(k, y_to)
                y[slices] = y[slices] + y_fft.real
                list_idx += 1

            return y

    # ### Case 2c: N-d signal, constant filter
    elif use_case == '2c':
        bb_padded = np.hstack((plan_b, np.zeros(nfft - n_filter)))
        u[:] = (bb_padded*filter_expander).transpose(t)
        bb_fft = fft_obj().copy()

        def planned_firfilter(x):
            """Filter data with a constant FIR filter.

            Parameters
            ----------
                b : array-like
                    A one-dimensional FIR filter array
                x : array-like
                    An N-dimensional input array

            Returns
            -------
                numpy.array
                    Filter output
            """
            y = np.zeros(y_shape)
            for k in range(0, n_signal, l):
                k_to = np.min((k + l, n_signal))
                slices[axis] = slice(k, k_to)
                u[:] = _utils.pad_array(x[slices], u_shape)
                x_fft = fft_obj().copy()
                v[:] = x_fft * bb_fft
                y_to = np.min((n_signal, k + nfft))
                # noinspection PyTypeChecker
                slices[axis] = slice(None, y_to - k)
                y_fft = ifft_obj().copy()[slices]
                slices[axis] = slice(k, y_to)
                y[slices] = y[slices] + y_fft.real

            return y

    # ### Case 3a: 1-d signal segments, constant signal
    elif use_case == '3a':
        # Pre-compute partial FFTs of x segments
        x_fft_list = []
        segment_slices = [slice(None)] * x_ndim
        for k_s in range(n_of_segments):
            segment_slices[segments_axis] = slice(k_s, k_s + 1)
            x_segment = np.squeeze(plan_x[segment_slices])
            this_x_fft_list = []
            for k_p in range(0, n_signal, l):
                k_p_to = np.min((k_p + l, n_signal))
                u[:] = _utils.pad_array(x_segment[k_p:k_p_to], u_shape)
                this_x_fft_list.append(fft_obj().copy())
            x_fft_list.append(this_x_fft_list)

        def planned_firfilter(b, segment_no):
            """Filter constant data with a FIR filter.

            Parameters
            ----------
                b : array-like
                    A one-dimensional FIR filter array.
                segment_no : int
                    Segment number

            Returns
            -------
                numpy.array
                    Filter output
            """
            # nfft-point FFT of filter once
            u[:] = np.hstack((b, np.zeros(nfft - n_filter)))
            b_fft = fft_obj().copy()

            y = np.zeros(y_shape)
            list_idx = 0
            for k in range(0, n_signal, l):
                v[:] = x_fft_list[segment_no][list_idx] * b_fft
                y_fft = ifft_obj().copy()
                y_to = np.min((n_signal, k + nfft))
                y[k:y_to] = y[k:y_to] + y_fft[:y_to - k].real
                list_idx += 1

            return y

    # ### Case 3b: 2-d signal segments, constant signal
    else:
        # Pre-compute partial FFTs of x segments
        segment_slices = [slice(None)] * x_ndim
        x_fft_list = []
        for k_s in range(n_of_segments):
            segment_slices[segments_axis] = slice(k_s, k_s + 1)
            x_segment = np.squeeze(plan_x[segment_slices])
            this_x_fft_list = []
            for k_p in range(0, n_signal, l):
                k_p_to = np.min((k_p + l, n_signal))
                slices[axis] = slice(k_p, k_p_to)
                u[:] = _utils.pad_array(x_segment[slices], u_shape)   #
                this_x_fft_list.append(fft_obj().copy())
            x_fft_list.append(this_x_fft_list)

        def planned_firfilter(b, segment_no):
            """Filter static data with a FIR filter.

            Parameters
            ----------
                b : array-like
                    A one-dimensional FIR filter array.

            Returns
            -------
                numpy.array
                    Filter output
            """
            # nfft-point FFT of filter once
            b_padded = np.hstack((b, np.zeros(nfft - n_filter)))
            u[:] = (b_padded*filter_expander).transpose(t)
            b_fft = fft_obj().copy()

            y = np.zeros(y_shape)
            list_idx = 0
            for k in range(0, n_signal, l):
                v[:] = x_fft_list[segment_no][list_idx] * b_fft
                y_to = np.min((n_signal, k + nfft))
                # noinspection PyTypeChecker
                slices[axis] = slice(None, y_to - k)
                y_fft = ifft_obj().copy()[slices]
                slices[axis] = slice(k, y_to)
                y[slices] = y[slices] + y_fft.real
                list_idx += 1

            return y

    return planned_firfilter


def correlate(plan_x,
              plan_y,
              mode='full',
              axes=None,
              constant_x=False,
              constant_y=False,
              x_segmented=False):
    """Returns a planned function for computing the cross-correlation of two
    sequences or arrays.

    The planner distinguishes between several different use cases:

        1. 1-D correlation of 1-D sequences or along single axis in N-D arrays
        2. M-D correlation of N-D sequences
        3. 1-D correlation along single axis in N-D array with 1-D sequence
        4. 1-D correlation of 1-D sequence along single axis in N-D array
        5. Special cases of 1, 2 and 3 where the first input is segmented

        The shapes of the two inputs are usually sufficient to determine which
        case should be used. However, to get 1-D correlation along single axis
        in N-D arrays, 'axes' must be a single integer or a length 1 sequence.
        In addition, x_segmented must be True for case 5.

    Parameters
    ----------
        plan_x : integer, shape or array-like
            First input sequence, it's shape or length.
        plan_y : integer, shape or array-like
            Second input sequence, it's shape or length.
        mode : Optional[str]
            A string indicating the output size.

            'full'
                The output is the full discrete linear cross-correlation of the
                inputs. (Default)
            'valid'
                The output consists only of those elements that do not rely on
                zero-padding.
            'same'
                The output is the same size as plan_x, centered with respect to
                the 'full' output.
        axes : Optional[int or sequence of ints]
            The axis or axes along which the cross-correlation is computed.
            Default is the last N axes of the highest-rank input where N is the
            rank of the lowest-rank input.
        constant_x : Optional[boolean]
            Indicates that the first input will be constant over all uses of
            the function. If True, plan_x must be array-like.
        constant_y : Optional[boolean]
            Indicates that the second input will be constant over all uses of
            the function. If True, plan_y must be array-like.
        x_segmented : Optional[boolean]
            Indicates that the first axis of plan_x contains segments that will
            be individually used multiple times.

    Returns
    -------
        function
            Planned correlation function.

    Raises
    ------
        ValueError
            If no function can be planned for the given arguments.
    """

    # Validate arguments
    if mode not in ("valid", "same", "full"):
        raise ValueError("parameter mode must be 'valid', 'same' or 'full'.")

    # Get dimensions
    x_shape = _utils.get_shape(plan_x)
    y_shape = _utils.get_shape(plan_y)
    x_ndim = len(x_shape)
    y_ndim = len(y_shape)

    if axes is None:
        axes = [k for k in range(x_segmented, x_ndim)]

    # Make sure axes is iterable
        if np.asarray(axes).ndim == 0:
            axes = (axes,)

    n_axes = len(axes)

    # ### Find use case
    if x_segmented:
        if x_ndim == 2 and y_ndim == 1:
            base_case = '5a'    # Correlate 1-D segments with 1-D sequences

        elif x_ndim - y_ndim == 1:
            if n_axes == 1:
                base_case = '5a'
            else:
                base_case = '5b'

        elif x_ndim > 2 and y_ndim == 1:
            base_case = '5c'

        else:
            raise ValueError("Could not plan a function with segmented x for "
                             "the given inputs.")

    elif x_ndim == 1 and y_ndim == 1:
        base_case = '1'         # Correlate 1-D sequences

    elif x_ndim == y_ndim:
        if n_axes == 1:
            base_case = '1'     # Correlate single axes in N-D sequences
        else:
            base_case = '2'     # Correlate multiple axes in N-D sequences

    elif x_ndim > 1 and y_ndim == 1:
        base_case = '3'         # Correlate single axis in N-D seq. with 1-D

        if n_axes > 1:
            raise ValueError("Cannot correlate over more axes than the least "
                             "number of dimensions in x or y.")

    elif y_ndim > 1 and x_ndim == 1:
        base_case = '4'         # Correlate 1-D seq. with single axis in N-D

        if n_axes > 1:
            raise ValueError("Cannot correlate over more axes than the least "
                             "number of dimensions in x or y.")

    else:
        raise ValueError("Could not plan a function for the given inputs.")

    if constant_x and constant_y:
        raise ValueError("A planned function does not make sense for two "
                         "constant inputs.")
    elif constant_x:
        use_case = base_case + 'b'
    elif constant_y:
        use_case = base_case + 'c'
    else:
        use_case = base_case + 'a'

    # ### Define function
    # 1-D correlation in 1-D or N-D sequences
    if base_case == '1':
        axes = axes[0]
        x_len = x_shape[axes]
        y_len = y_shape[axes]
        l = np.max((x_len, y_len))
        nfft = int(np.power(2, np.ceil(np.log2(2*l-1))))
        planned_rfft, planned_irfft = rfft(x_shape,
                                           nfft,
                                           axis=axes,
                                           fft_pair=True)

        rev_slices = [slice(None)] * x_ndim
        rev_slices[axes] = slice(None, None, -1)
        out_slices = [slice(None)] * x_ndim

        if mode == 'valid':
            if x_len < y_len:
                raise ValueError("x should have at least the same length as y "
                                 "for 'valid' mode")
            else:
                out_slices[axes] = slice(y_len - 1, x_len)

        elif mode == 'same':
            out_slices[axes] = slice((y_len - 1)//2, (y_len - 1)//2 + x_len)

        else:
            out_slices[axes] = slice(0, x_len + y_len - 1)

        if use_case == '1b':
            x_fft_0 = planned_rfft(plan_x)

            def planned_correlate(y):
                y_fft = planned_rfft(y[rev_slices])
                return planned_irfft(x_fft_0 * y_fft)[out_slices]

        elif use_case == '1c':
            y_fft_0 = planned_rfft(plan_y[rev_slices])

            def planned_correlate(x):
                x_fft = planned_rfft(x)
                return planned_irfft(x_fft * y_fft_0)[out_slices]

        else:
            def planned_correlate(x, y):
                x_fft = planned_rfft(x)
                y_fft = planned_rfft(y[rev_slices])
                print(planned_irfft(x_fft * y_fft).shape)
                return planned_irfft(x_fft * y_fft)[out_slices]

    # M-D correlation in N-D sequences
    elif base_case == '2':
        # Define shapes and slices
        rev_slices = [slice(None, None, -1)] * y_ndim
        shape_max = np.max((x_shape, y_shape), axis=0)
        shape_max_p2 = np.power(2, np.ceil(np.log2(2*shape_max-1)))
        # noinspection PyUnresolvedReferences

        fft_shape = list(x_shape)
        for k in range(x_ndim):
            if k in axes:
                # noinspection PyUnresolvedReferences
                fft_shape[k] = shape_max_p2.astype(int)[k]

        # Plan rfftn and irfftn functions
        planned_rfftn, planned_irfftn = rfftn(tuple(shape_max),
                                              tuple(fft_shape),
                                              axes=axes,
                                              fft_pair=True)

        out_slices = [slice(None)] * x_ndim
        for k, x_n, y_n in zip(range(x_ndim), x_shape, y_shape):
            if mode == 'valid':
                if x_n < y_n:
                    raise ValueError("x should have at least the same "
                                     "length as y in all axes for 'valid' "
                                     "mode.")
                out_slices[k] = slice(y_n - 1, x_n)
            elif mode == 'same':
                out_slices[k] = slice((y_n - 1)//2, x_n + (y_n - 1)//2)
            else:
                out_slices[k] = slice(0, x_n + y_n - 1)

        if use_case == '2b':
            x_fft_0 = planned_rfftn(plan_x)

            def planned_correlate(y):
                y_fft = planned_rfftn(y[rev_slices])
                return planned_irfftn(x_fft_0 * y_fft)[out_slices]

        elif use_case == '2c':
            y_fft_0 = planned_rfftn(plan_y[rev_slices])

            def planned_correlate(x):
                x_fft = planned_rfftn(x)
                return planned_irfftn(x_fft * y_fft_0)[out_slices]

        else:
            def planned_correlate(x, y):
                x_fft = planned_rfftn(x)
                y_fft = planned_rfftn(y[rev_slices])
                r = planned_irfftn(x_fft * y_fft)[out_slices]
                return r
                # return planned_irfftn(x_fft * y_fft)[out_slices]

    # 1-D correlation of axis in N-D sequence with 1-D sequence
    elif base_case == '3':
        axes = axes[0]
        x_len = x_shape[axes]
        y_len = y_shape[0]
        l = np.max((x_len, y_len))
        nfft = int(np.power(2, np.ceil(np.log2(2*l-1))))
        planned_rfft, planned_irfft = rfft(x_shape,
                                           nfft,
                                           axis=axes,
                                           fft_pair=True)

        out_slices = [slice(None)] * x_ndim

        if mode == 'valid':
            if x_len < y_len:
                raise ValueError("x should have at least the same length as y "
                                 "for 'valid' mode")
            else:
                out_slices[axes] = slice(y_len - 1, x_len)

        elif mode == 'same':
            out_slices[axes] = slice((y_len - 1)//2, (y_len - 1)//2 + x_len)

        else:
            out_slices[axes] = slice(0, x_len + y_len - 1)

        # If x is constant
        if use_case == '3b':
            x_fft_0 = planned_rfft(plan_x)
            planned_rfft_2 = rfft(y_shape, nfft)

            def planned_correlate(y):
                y_fft = _utils.expand_me(planned_rfft_2(y[::-1]), axes, x_ndim)
                return planned_irfft(x_fft_0 * y_fft)[out_slices]

        # If y is constant
        elif use_case == '3c':
            y_fft_0 = _utils.expand_me(np.fft.rfft(plan_y[::-1]), axes, x_ndim)

            def planned_correlate(x):
                x_fft = planned_rfft(x)
                return planned_irfft(x_fft * y_fft_0)[out_slices]

        # If neither x nor y are constant
        else:
            planned_rfft_2 = rfft(y_shape, nfft)

            def planned_correlate(x, y):
                x_fft = planned_rfft(x)
                y_fft = _utils.expand_me(planned_rfft_2(y[::-1]), axes, x_ndim)
                return planned_irfft(x_fft * y_fft)[out_slices]

    # 1-D Correlation of 1-D sequence with axis in N-D sequence
    elif base_case == '4':
        axes = axes[0]
        x_len = x_shape[0]
        y_len = y_shape[axes]
        l = np.max((x_len, y_len))
        nfft = int(np.power(2, np.ceil(np.log2(2*l-1))))
        planned_rfft, planned_irfft = rfft(y_shape,
                                           nfft,
                                           axis=axes,
                                           fft_pair=True)

        rev_slices = [slice(None)] * y_ndim
        rev_slices[axes] = slice(None, None, -1)
        out_slices = [slice(None)] * y_ndim

        if mode == 'valid':
            if x_len < y_len:
                raise ValueError("x should have at least the same length as y "
                                 "for 'valid' mode")
            else:
                out_slices[axes] = slice(y_len - 1, x_len)

        elif mode == 'same':
            out_slices[axes] = slice((y_len - 1)//2, (y_len - 1)//2 + x_len)

        else:
            out_slices[axes] = slice(0, x_len + y_len - 1)

        # If x is constant
        if use_case == '4b':
            x_fft_0 = _utils.expand_me(np.fft.rfft(plan_x, nfft), axes, y_ndim)

            def planned_correlate(y):
                y_fft = planned_rfft(y[rev_slices])
                return planned_irfft(x_fft_0 * y_fft)[out_slices]

        # If y is constant
        elif use_case == '4c':
            y_fft_0 = np.fft.rfft(plan_y[rev_slices])
            planned_rfft_2 = rfft(x_shape, nfft)

            def planned_correlate(x):
                x_fft = _utils.expand_me(planned_rfft_2(x), axes, y_ndim)
                return planned_irfft(x_fft * y_fft_0)[out_slices]

        # If neither x nor y are constant
        else:
            planned_rfft_2 = rfft(x_shape, nfft)

            def planned_correlate(x, y):
                x_fft = _utils.expand_me(planned_rfft_2(x), axes, y_ndim)
                y_fft = planned_rfft(y[rev_slices])
                return planned_irfft(x_fft * y_fft)[out_slices]

    # X is segmented
    else:
        x_shape = x_shape[1:]
        x_ndim -= 1

        if base_case == '5a':
            axes = axes[0]
            if axes > 0:
                axes -= 1

            # Plan FFT
            x_len = x_shape[axes]
            y_len = y_shape[axes]
            l = np.max((x_len, y_len))
            nfft = int(np.power(2, np.ceil(np.log2(2*l-1))))
            planned_rfft, planned_irfft = rfft(x_shape,
                                               nfft,
                                               axis=axes,
                                               fft_pair=True)

            # Define slices
            rev_slices = [slice(None)] * x_ndim
            rev_slices[axes] = slice(None, None, -1)
            out_slices = [slice(None)] * x_ndim

            if mode == 'valid':
                if x_len < y_len:
                    raise ValueError("x should have at least the same length "
                                     "as y for 'valid' mode")
                else:
                    out_slices[axes] = slice(y_len - 1, x_len)

            elif mode == 'same':
                out_slices[axes] = slice((y_len - 1)//2, (y_len - 1)//2 + x_len)

            else:
                out_slices[axes] = slice(0, x_len + y_len - 1)

            # Pre-compute FFT for all segments of x
            x_fft_0 = []
            for segment in plan_x:
                x_fft_0.append(planned_rfft(segment))

            def planned_correlate(n, y):
                y_fft = planned_rfft(y[rev_slices])
                return planned_irfft(x_fft_0[n] * y_fft)[out_slices]

        elif base_case == '5b':
            axes = [axis - 1 if axis > 0 else axis for axis in axes]

            # Compute shapes
            shape_max = np.max((x_shape, y_shape), axis=0)
            shape_max_p2 = np.power(2, np.ceil(np.log2(2*shape_max-1)))

            fft_shape = list(x_shape)
            for k in range(x_ndim):
                if k in axes:
                    # noinspection PyUnresolvedReferences
                    fft_shape[k] = shape_max_p2.astype(int)[k]

            # Plan rfftn and irfftn functions
            planned_rfftn, planned_irfftn = rfftn(tuple(shape_max),
                                                  tuple(fft_shape),
                                                  axes=axes,
                                                  fft_pair=True)

            # Define slices
            rev_slices = [slice(None, None, -1)] * y_ndim
            out_slices = [slice(None)] * x_ndim
            for k, x_n, y_n in zip(range(x_ndim), x_shape, y_shape):
                if mode == 'valid':
                    if x_n < y_n:
                        raise ValueError("x should have at least the same "
                                         "length as y in all axes for 'valid' "
                                         "mode.")
                    out_slices[k] = slice(y_n - 1, x_n)
                elif mode == 'same':
                    out_slices[k] = slice((y_n - 1)//2, x_n + (y_n - 1)//2)
                else:
                    out_slices[k] = slice(0, x_n + y_n - 1)

            x_fft_0 = []
            for segment in plan_x:
                x_fft_0.append(planned_rfftn(segment))

            def planned_correlate(n, y):
                y_fft = planned_rfftn(y[rev_slices])
                return planned_irfftn(x_fft_0[n] * y_fft)[out_slices]

        else:
            axes = axes[0]
            if axes > 0:
                axes -= 1

            x_len = x_shape[axes]
            y_len = y_shape[0]
            l = np.max((x_len, y_len))
            nfft = int(np.power(2, np.ceil(np.log2(2*l-1))))
            planned_rfft, planned_irfft = rfft(x_shape,
                                               nfft,
                                               axis=axes,
                                               fft_pair=True)
            planned_rfft_2 = rfft(y_shape, nfft)

            out_slices = [slice(None)] * x_ndim

            if mode == 'valid':
                if x_len < y_len:
                    raise ValueError("x should have at least the same length "
                                     "as y for 'valid' mode")
                else:
                    out_slices[axes] = slice(y_len - 1, x_len)

            elif mode == 'same':
                out_slices[axes] = slice((y_len - 1)//2, (y_len - 1)//2 + x_len)

            else:
                out_slices[axes] = slice(0, x_len + y_len - 1)

            x_fft_0 = planned_rfft(plan_x)

            def planned_correlate(n, y):
                y_fft = _utils.expand_me(planned_rfft_2(y[::-1]), axes, x_ndim)
                return planned_irfft(x_fft_0[n] * y_fft)[out_slices]

    return planned_correlate
