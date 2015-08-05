import numpy as _np
from .chisquare import chisquare
import copy as _copy


class LinLsqFit(object):
    _resetlist = _np.array(['_X', '_y', '_beta', '_covar', '_chisq_red', '_y_fit'])

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
    def _get_y_unweighted(self):
        return self._y_unweighted

    def _set_y_unweighted(self, val):
        self._force_recalc()
        self._y_unweighted = val
    y_unweighted = property(_get_y_unweighted, _set_y_unweighted)

    # ======================================
    # y_error
    # ======================================
    def _get_y_error(self):
        return self._y_error

    def _set_y_error(self, val):
        self._force_recalc()
        self._y_error = val
    y_error = property(_get_y_error, _set_y_error)
    
    # ======================================
    # X_unweighted
    # ======================================
    def _get_X_unweighted(self):
        return self._X_unweighted

    def _set_X_unweighted(self, val):
        self._force_recalc()
        self._X_unweighted = val
    X_unweighted = property(_get_X_unweighted, _set_X_unweighted)

    # ======================================
    # X (calculated)
    # ======================================
    def _get_X(self):
        if self._X is None:
            X = _copy.deepcopy(self.X_unweighted)
            # print 'X shape is {}'.format(X.shape)
            for i, el in enumerate(X):
                X[i, :] = el/self.y_error[i]
            # print 'New X shape is {}'.format(X.shape)
            self._X = X
        return self._X
    X = property(_get_X)

    # ======================================
    # y (calculated)
    # ======================================
    def _get_y(self):
        if self._y is None:
            self._y = self.y_unweighted/self.y_error
        return self._y
    y = property(_get_y)

    # ======================================
    # y_fit (y from fit)
    # ======================================
    def _get_y_fit(self):
        if self._y_fit is None:
            self._y_fit = _np.dot(self.X_unweighted, self.beta)
        return self._y_fit
    y_fit = property(_get_y_fit)

    # ======================================
    # beta (calculated)
    # ======================================
    def _get_beta(self):
        if self._beta is None:
            # This is the linear least squares matrix formalism
            self._beta = _np.dot(_np.linalg.pinv(self.X) , self.y)
        return self._beta
    beta = property(_get_beta)

    # ======================================
    # covar (calculated)
    # ======================================
    def _get_covar(self):
        if self._covar is None:
            self._covar = _np.linalg.inv(_np.dot(_np.transpose(self.X), self.X))
        return self._covar
    covar = property(_get_covar)
    
    # ======================================
    # chisq_red (calculated)
    # ======================================
    def _get_chisq_red(self):
        if self._chisq_red is None:
            self._chisq_red = chisquare(self.y_unweighted.transpose(), _np.dot(self.X_unweighted, self.beta), self.y_error, ddof=3, verbose=False)
        return self._chisq_red
    chisq_red = property(_get_chisq_red)
