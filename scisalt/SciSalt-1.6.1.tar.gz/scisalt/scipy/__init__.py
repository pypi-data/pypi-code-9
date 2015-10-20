"""
The :mod:`scipy <scisalt.scipy>` module contains a few convenience functions mostly designed to make fitting easier.
"""
__all__ = ['chisquare', 'curve_fit_unscaled', 'fft', 'gaussfit']
from .LinLsqFit import *                 # noqa
from .chisquare import *                 # noqa
from .curve_fit_unscaled import *        # noqa
from .fft import *                       # noqa
from .fill_missing_timestamps import *   # noqa
from .gaussfit import *                  # noqa

import os as _os
_on_rtd = _os.environ.get('READTHEDOCS', None) == 'True'
if not _on_rtd:
    import pyximport
    import numpy as _np
    pyximport.install(setup_args={"include_dirs": _np.get_include()})

    from .hough_ellipse import hough_ellipse
