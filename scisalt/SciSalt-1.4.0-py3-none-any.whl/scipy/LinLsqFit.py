import os as _os
on_rtd = _os.environ.get('READTHEDOCS', None) == 'True'
if not on_rtd:
    import numpy as _np

from .chisquare import chisquare
import copy as _copy


class LinLsqFit(object):
    """
    Gets the linear least squares for :math:`\\beta` of a problem given :math:`X_{ij} \\beta_{i} = y_j`.

    As input, it takes *y_unweighted* as the measured :math:`y`, *X_unweighted* for :math:`X`, and *y_error* as the measurement error on :math:`y`.
    """
    _resetlist = ['_X', '_y', '_beta', '_covar', '_chisq_red', '_y_fit']

    def __init__(self, y_unweighted, X_unweighted, y_error=None):

        self._force_recalc()

        self.y_unweighted = y_unweighted
        self.y_error = y_error
        self.X_unweighted = X_unweighted

    # ======================================
    # Resets stored values for calculated
    # quantities
    # ======================================
    def _force_recalc(self):
        # self._X = None
        # self._y = None
        # self._beta = None
        # self._covar = None
        # self._chisq_red = None
        # self._emit = None
        # self._twiss=None
        for resetstr in self._resetlist:
            # print resetstr
            setattr(self, resetstr, None)

    # ======================================
    # y_unweighted
    # ======================================
    @property
    def y_unweighted(self):
        """
        The :math:`y` of the problem :math:`X_{ij} \\beta_{i} = y_j`. Setting this attribute forces a recalculation.
        """
        return self._y_unweighted

    @y_unweighted.setter
    def y_unweighted(self, val):
        self._force_recalc()
        self._y_unweighted = val

    # ======================================
    # y_error
    # ======================================
    @property
    def y_error(self):
        """
        The measured error of :math:`y` of the problem :math:`X_{ij} \\beta_{i} = y_j`. Setting this attribute forces a recalculation.
        """
        return self._y_error

    @y_error.setter
    def _set_y_error(self, val):
        self._force_recalc()
        self._y_error = val
    
    # ======================================
    # X_unweighted
    # ======================================
    @property
    def X_unweighted(self):
        """
        The :math:`X`. Setting this attribute forces a recalculation.
        """
        return self._X_unweighted

    @X_unweighted.setter
    def _set_X_unweighted(self, val):
        self._force_recalc()
        self._X_unweighted = val

    # ======================================
    # X (calculated)
    # ======================================
    @property
    def X(self):
        """
        The :math:`X` weighted properly by the errors from *y_error*
        """
        if self._X is None:
            X = _copy.deepcopy(self.X_unweighted)
            # print 'X shape is {}'.format(X.shape)
            for i, el in enumerate(X):
                X[i, :] = el/self.y_error[i]
            # print 'New X shape is {}'.format(X.shape)
            self._X = X
        return self._X

    # ======================================
    # y (calculated)
    # ======================================
    @property
    def y(self):
        """
        The :math:`X` weighted properly by the errors from *y_error*
        """
        if self._y is None:
            self._y = self.y_unweighted/self.y_error
        return self._y

    # ======================================
    # y_fit (y from fit)
    # ======================================
    @property
    def y_fit(self):
        """
        Using the result of the linear least squares, the result of :math:`X_{ij}\\beta_i`
        """
        if self._y_fit is None:
            self._y_fit = _np.dot(self.X_unweighted, self.beta)
        return self._y_fit

    # ======================================
    # beta (calculated)
    # ======================================
    @property
    def beta(self):
        """
        The result :math:`\\beta` of the linear least squares
        """
        if self._beta is None:
            # This is the linear least squares matrix formalism
            self._beta = _np.dot(_np.linalg.pinv(self.X) , self.y)
        return self._beta

    # ======================================
    # covar (calculated)
    # ======================================
    @property
    def covar(self):
        """
        The covariance matrix for the result :math:`\\beta`
        """
        if self._covar is None:
            self._covar = _np.linalg.inv(_np.dot(_np.transpose(self.X), self.X))
        return self._covar
    
    # ======================================
    # chisq_red (calculated)
    # ======================================
    @property
    def chisq_red(self):
        """
        The reduced chi-square of the linear least squares
        """
        if self._chisq_red is None:
            self._chisq_red = chisquare(self.y_unweighted.transpose(), _np.dot(self.X_unweighted, self.beta), self.y_error, ddof=3, verbose=False)
        return self._chisq_red
