import os as _os
on_rtd = _os.environ.get('READTHEDOCS', None) == 'True'
if not on_rtd:
    import numpy as _np
    import matplotlib.pyplot as _plt

from .curve_fit_unscaled import curve_fit_unscaled as _curve_fit_unscaled
from ..matplotlib.figure import figure as _figure


class GaussResults(object):
    """
    A class containing the full results of :func:`gaussfit() <scisalt.scipy.gaussfit>`.
    """
    def __init__(self, x, y, sigma_y, func, popt, pcov=None, chisq_red=None):
        # Populate default info
        #: The fit values *(amp, mu, var)* where *var* is either *rms* or *rms\*\*2*
        self.popt      = popt
        #: The covariance matrix
        self.pcov      = pcov
        #: The reduced chi square value
        self.chisq_red = chisq_red
        #: The :math:`x` data points
        self.x         = x
        #: The :math:`y` data points
        self.y         = y
        #: The error on :math:`y` data points
        self.sigma_y   = sigma_y
        #: The function used to fit
        self.func      = func


def plot(self, ax, x_mult=None, **kwargs):
        """
        Plots the results to axis *ax*, with x-axis scale factor *x_mult*. *\*\*kwargs* is passed through to :meth:`matplotlib.axes.Axes.plot`.
        """
        xmin = min(self.x)
        xmax = max(self.x)
        x_fit = _np.linspace(xmin, xmax, 1000)
        y_fit = self.func(x_fit, *self.popt)
        # _figure('MYTOOLS: Gauss Fit Routine')
        if x_mult is not None:
            x     = self.x * x_mult
            x_fit = x_fit * x_mult
        else:
            x = self.x
        if self.sigma_y is not None:
            self.sigma_y = self.sigma_y.flatten()
            # ax.errorbar(x, self.y, yerr=self.sigma_y, fmt='o-')
            # ax.errorbar(x, self.y, fmt='o-')
            ax.plot(x, self.y, 'o-', **kwargs)
            ax.plot(x_fit, y_fit, **kwargs)
            ax.legend(['Data', 'Fit'])
        else:
            ax.plot(x, self.y, 'o-', x_fit, y_fit, **kwargs)


def _gauss(x, amp, mu, sigma, bg=0):
    # print 'Sigma is {}.'.format(sigma)
    return _np.abs(amp) * _np.exp( -(x - mu)**2 / (2 * sigma**2)) + bg
    # return _np.abs(amp) * _np.exp(-(x - mu)**2 / (2 * sigma**2))


def _gauss_nobg(x, amp, mu, sigma):
    return _gauss(x, amp, mu, sigma)


def _gaussvar(x, amp, mu, variance, bg=0):
    return _np.abs(amp) * _np.exp(-(x - mu)**2 / (2 * variance)) + bg
    # return _np.abs(amp) * _np.exp(-(x - mu)**2 / (2 * variance))


def _gaussvar_nobg(x, amp, mu, variance):
    return _gaussvar(x, amp, mu, variance)


def gaussfit(x, y, sigma_y=None, plot=True, p0=None, verbose=False, variance_bool=False, background_bool=False, bg=0):
    """
    Fits a gaussian to a curve specified by pairs *x* and *y*, with error on *y* of *sigma_y*.

    * *plot*: Determines whether the plot is shown
    * *p0*: Initial guess given by amplitude *amp*, mean *mu*, and standard deviation *rms*, in the form of:

      * :code:`[amp, mu, rms**2]` if *variance_bool* is true
      * :code:`[amp, mu, rms]` if *variance_bool* is false

    * *verbose*: If true, prints details to terminal
    * *background_bool*: If true, uses a background term in the fit, with initial guess *bg*

    Returns full statistical results in the form of an instance of class :class:`GaussResults <scisalt.scipy.GaussResults>`.
    """
    x       = x.flatten()
    y       = y.flatten()

    use_error = ( sigma_y is not None )

    # Determine whether to use the variance or std dev form
    # in the gaussian equation
    # print 'variance_bool is {}'.format(variance_bool)
    if variance_bool:
        if background_bool:
            func = _gaussvar
        else:
            func = _gaussvar_nobg
    else:
        if background_bool:
            func = _gauss
        else:
            func = _gauss_nobg

    # Determine initial guesses if none are input
    if (p0 is None):
        amp = max(y)
        mu  = sum(x * y) / sum(y)
        rms = _np.sqrt(sum(x**2 * y) / sum(y))
        if variance_bool:
            p0 = _np.array((amp, mu, rms**2))
        else:
            p0 = _np.array((amp, mu, rms))
        if background_bool:
            p0 = _np.append(p0, bg)
    else:
        if variance_bool:
            rms = _np.sqrt(p0[2])
        else:
            rms = p0[2]

    # print p0

    # Verbose options
    if verbose:
        if variance_bool:
            print('Using function gaussvar')
        else:
            print('Using function gauss')
        print('Initial guess is: {}'.format(p0))
        print('RMS is: {}'.format(rms))

    popt, pcov, chisq_red = _curve_fit_unscaled(func, x, y, sigma=sigma_y, p0=p0)
    # # Either with error or without
    # if use_error:
    #         if verbose: print 'With error'
    #         popt, pcov = _spopt.curve_fit(func, x, y, sigma=sigma_y, p0=p0)

    #         # Get reduced chi-square
    #         y_expect = func(x, popt[0], popt[1], popt[2], popt[3])
    #         chisq_red = _chisquare(y, y_expect, sigma_y, 3, verbose=verbose)

    #         # Correct scaled covariance matrix
    #         pcov = pcov / chisq_red
    # else:
    #         if verbose:
    #                 print 'Without error'
    #                 print 'WARNING: COVARIANCE MATRIX SCALED'
    #         popt, pcov = _spopt.curve_fit(func, x, y, p0=p0)

    popt[2] = _np.abs(popt[2])

    if verbose:
        print('Fit results are: {}'.format(popt))
        print('Covariance matrix is: {}'.format(pcov))
    if plot:
        xmin = min(x)
        xmax = max(x)
        x_fit = _np.linspace(xmin, xmax, 1000)
        if background_bool:
            y_fit = func(x_fit, popt[0], popt[1], popt[2], popt[3])
        else:
            y_fit = func(x_fit, popt[0], popt[1], popt[2])
        _figure('MYTOOLS: Gauss Fit Routine')
        if use_error:
            sigma_y = sigma_y.flatten()
            _plt.errorbar(x, y, yerr=sigma_y, fmt='o-')
            _plt.plot(x_fit, y_fit)
        else:
            _plt.plot(x, y, 'o-', x_fit, y_fit)
        # if numfigs > 0:
        #         _plt.figure(fig.number)
        
    if use_error:
        # gaussout = _col.namedtuple('gaussfit', ['popt', 'pcov', 'chisq_red'])
        # return gaussout(popt, pcov, chisq_red)
        gaussout = GaussResults(x=x, y=y, sigma_y=sigma_y, func=func, popt=popt, pcov=pcov, chisq_red=chisq_red)
        return gaussout
    else:
        # gaussout = _col.namedtuple('gaussfit', ['popt', 'pcov'])
        # return gaussout(popt, pcov)
        gaussout = GaussResults(x=x, y=y, sigma_y=sigma_y, func=func, popt=popt, pcov=pcov)
        return gaussout
