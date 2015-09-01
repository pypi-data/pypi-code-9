import os as _os
_on_rtd = _os.environ.get('READTHEDOCS', None) == 'True'
if not _on_rtd:
    import numpy as _np


def gaussian(x, mu, sigma):
    """
    .. versionadded:: 1.5

    Gaussian function of the form :math:`\\frac{1}{\\sqrt{2 \\pi}\\sigma} e^{-\\frac{(x-\\mu)^2}{2\\sigma^2}}`.
    """
    return _np.exp(-(x-mu)**2/(2*sigma**2)) / (_np.sqrt(2*_np.pi) * sigma)
