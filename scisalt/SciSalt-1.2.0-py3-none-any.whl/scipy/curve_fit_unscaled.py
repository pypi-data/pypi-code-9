import os as _os
on_rtd = _os.environ.get('READTHEDOCS', None) == 'True'
if not on_rtd:
    import numpy as _np
    import scipy.optimize as _spopt
from .chisquare import chisquare as _chisquare


def curve_fit_unscaled(*args, **kwargs):
    """
    Use the reduced chi square to unscale :mod:`scipy`'s scaled :func:`scipy.optimize.curve_fit`. *\*args* and *\*\*kwargs* are passed through to :func:`scipy.optimize.curve_fit`. The tuple *popt, pcov, chisq_red* is returned, where *popt* is the optimal values for the parameters, *pcov* is the estimated covariance of *popt*, and *chisq_red* is the reduced chi square. See http://docs.scipy.org/doc/scipy-0.15.1/reference/generated/scipy.optimize.curve_fit.html.
    """
    # Extract verbosity
    verbose = kwargs.pop('verbose', False)

    # Do initial fit
    popt, pcov = _spopt.curve_fit(*args, **kwargs)

    # Expand positional arguments
    func = args[0]
    x    = args[1]
    y    = args[2]

    ddof = len(popt)

    # Try to use sigma to unscale pcov
    try:
        sigma = kwargs['sigma']
        if sigma is None:
            sigma = _np.ones(len(y))
        # Get reduced chi-square
        y_expect = func(x, *popt)
        chisq_red = _chisquare(y, y_expect, sigma, ddof, verbose=verbose)

        # Correct scaled covariance matrix
        pcov = pcov / chisq_red
        return popt, pcov, chisq_red
    except ValueError:
        print('hello')
# popt, pcov = _spopt.curve_fit(func, x, y, sigma=sigma_y, p0=p0)

# # Get reduced chi-square
# y_expect = func(x, popt[0], popt[1], popt[2], popt[3])
# chisq_red = _chisquare(y, y_expect, sigma_y, 3, verbose=verbose)

# # Correct scaled covariance matrix
# pcov = pcov/chisq_red
