import numpy as _np


def frexp10(x):
    expon = _np.int(_np.floor(_np.log10(_np.abs(x))))
    mant = x/_np.power(10, expon)
    return (mant, expon)
