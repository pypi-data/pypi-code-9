import os as _os
_on_rtd = _os.environ.get('READTHEDOCS', None) == 'True'
if not _on_rtd:
    import numpy as _np


def frexp10(x):
    """
    Finds the *mantissa* :math:`m` and *exponent* :math:`e` of a number *x* such that :math:`x = m 10^e`

    Returns the list :code:`(mantissa, exponent)`.
    """
    expon = _np.int(_np.floor(_np.log10(_np.abs(x))))
    mant = x/_np.power(10, expon)
    return (mant, expon)
