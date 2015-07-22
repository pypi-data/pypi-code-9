import numpy as _np
import scipy.optimize as _spopt
from .chisquare import chisquare as _chisquare


def curve_fit_unscaled(*args, **kwargs):
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
