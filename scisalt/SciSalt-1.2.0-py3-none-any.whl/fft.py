#!/usr/bin/env python3
import ipdb  # NOQA
import numpy as np
from .fill_missing_timestamps import fill_missing_timestamps
from . import qt
# import stability as st


def fft(values, freq=None, timestamps=None, fill_missing=False):
    # ======================================
    # Get frequency
    # ======================================
    if freq is None:
        freq = qt.getDouble(title='Fourier Analysis', text='Frequency samples taken at:', min=0, decimals=2, value=1.0)
        freq = freq.input
    
    if fill_missing:
        (t_x, x_filled) = fill_missing_timestamps(timestamps, values)
    else:
        x_filled = values
        
    num_samples = np.size(x_filled)
    xfft = np.fft.rfft(x_filled)
    
    factor = freq/num_samples
    num_fft = np.size(xfft)
    f = factor * np.linspace(1, num_fft, num_fft)
    
    xpow = np.abs(xfft*np.conj(xfft))

    # ======================================
    # No DC term
    # ======================================
    xpow = xpow[1:]
    f = f[1:]

    return (f, xpow)
