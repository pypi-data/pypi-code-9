import os as _os
on_rtd = _os.environ.get('READTHEDOCS', None) == 'True'
if not on_rtd:
    import numpy as _np
    import matplotlib.pyplot as _plt

from .curve_fit_unscaled import curve_fit_unscaled as _curve_fit_unscaled
from ..matplotlib.figure import figure as _figure
import logging
logger = logging.getLogger(__name__)


class GaussResults(object):
    """
    Fits a gaussian to a curve specified by pairs *x* and *y*, with error on *y* of *sigma_y*.

    * *plot*: Determines whether the plot is shown
    * *p0*: Initial guess given by amplitude *amp*, mean *mu*, and standard deviation *rms*, in the form of:

      * :code:`[amp, mu, rms**2]` if *variance_bool* is true
      * :code:`[amp, mu, rms]` if *variance_bool* is false

    * *background_bool*: If true, uses a background term in the fit, with initial guess *bg*

    Returns full statistical results in the form of an instance of class :class:`GaussResults <scisalt.scipy.GaussResults>`.
    """
    def __init__(self, x, y, sigma_y=None, p0=None, variance=False, background=False):
        # ======================================
        # Store things
        # ======================================
        self._x          = x.flatten()
        self._y          = y.flatten()
        self._sigma_y    = sigma_y
        self._p0         = p0
        self._variance   = variance
        self._background = background
    
        # ======================================
        # Perform curve fit
        # ======================================
        self._popt, self._pcov, self._chisq_red = _curve_fit_unscaled(self.func, self.x, self.y, sigma=self.sigma_y, p0=self.p0)
    
        # ======================================
        # Keep sigma positive
        # ======================================
        self._popt[2] = _np.abs(self._popt[2])
    
    @property
    def popt(self):
        """
        The fit parameters for the fit function.
        """
        return self._popt

    @property
    def pcov(self):
        """
        The covariance for the fit parameters.
        """
        return self._pcov

    @property
    def chisq_red(self):
        """
        The reduced chi square.
        """
        return self._chisq_red

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def sigma_y(self):
        return self._sigma_y

    @property
    def variance(self):
        return self._variance

    @property
    def background(self):
        return self._background

    @property
    def func(self):
        # ======================================
        # Determine whether to use the variance or std dev form
        # in the gaussian equation
        # ======================================
        if self.variance:
            if self.background:
                return _gaussvar
            else:
                return _gaussvar_nobg
        else:
            if self.background:
                return _gauss
            else:
                return _gauss_nobg

    @property
    def use_error(self):
        return ( self.sigma_y is not None )

    @property
    def p0(self):
        # ======================================
        # Determine initial guesses
        # ======================================
        if (self._p0 is None):
            amp = max(self.y)
            mu  = sum(self.x * self.y) / sum(self.y)
            rms = _np.sqrt(sum((self.x-mu)**2 * self.y) / sum(self.y))

            # ======================================
            # Modify initial guess for variance
            # ======================================
            if self.variance:
                self._p0 = _np.array((amp, mu, rms**2))
            else:
                self._p0 = _np.array((amp, mu, rms))

            # ======================================
            # Modify initial guess for background
            # ======================================
            if self.background:
                self._p0 = _np.append(self._p0, min(self.y))

        return self._p0

    def plot(self):
        xmin = min(self.x)
        xmax = max(self.x)
        x_fit = _np.linspace(xmin, xmax, 1000)
        y_fit = self.func(x_fit, *self.popt)
        _figure('MYTOOLS: Gauss Fit Routine')
        if self.use_error:
            sigma_y = self.sigma_y.flatten()
            _plt.errorbar(self.x, self.y, yerr=sigma_y, fmt='o-')
            _plt.plot(x_fit, y_fit)
        else:
            _plt.plot(self.x, self.y, 'o-', x_fit, y_fit)


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
