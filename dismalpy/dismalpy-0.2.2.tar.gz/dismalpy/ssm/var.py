"""
Vector Autoregression model

Author: Chad Fulton
License: Simplified-BSD
"""
from __future__ import division, absolute_import # , print_function

from warnings import warn

import numpy as np
import statsmodels.tsa.base.tsa_model as tsbase
from statsmodels.tsa.tsatools import lagmat
from statsmodels.tsa.vector_ar import var_model
from .mlemodel import MLEModel
from .tools import (
    concat
)

class VAR(MLEModel):
    r"""
    Vector Autoregression

    Parameters
    ----------
    endog : array_like
        The observed time-series process :math:`y`
    order : int
        The order of the vector autoregression
    """

    def __init__(self, endog, order=1, *args, **kwargs):
        # Initialize the generic Model
        tsbase.TimeSeriesModel.__init__(self, endog=endog, *args, **kwargs)

        # Model orders
        k_endog = self.endog.shape[1]
        self.order = order

        k_posdef = k_endog
        k_states = k_endog * self.order

        # Parameter dimensions        
        self.k_ar = self.order * k_posdef
        self.k_var = k_posdef * self.k_ar
        self.k_params = (
            k_posdef +       # state intercept
            self.k_var +        # lag polynomial
            # k_posdef**2         # state cov
            k_posdef         # state cov
        )
    
        # Initialize the statespace
        super(VAR, self).__init__(
            endog, k_states=k_states, k_posdef=k_posdef, *args, **kwargs
        )

        # Initialize known elements of the state space matrices

        # The design matrix is just an identity for the first k_endog states
        idx = np.diag_indices(self.k_endog)
        self[('design',) + idx] = 1

        # The transition matrix is in companion form
        idx = np.diag_indices(self.k_states - self.k_posdef)
        idx = idx[0] + self.k_posdef, idx[1]
        self[('transition',) + idx] = 1

        # The selection matrix selects the first k_posdef states
        idx = np.diag_indices(self.k_posdef)
        self[('selection',) + idx] = 1

        # Initialize the state space model as approximately diffuse
        self.initialize_approximate_diffuse()
        # Because of the diffuse initialization, burn first two loglikelihoods
        self.loglikelihood_burn = k_states

        # Cache some indices
        self._state_intercept_idx = np.s_['state_intercept',:3]
        self._transition_idx = np.s_['transition', :k_posdef, :]
        #self._state_cov_idx = np.s_['state_cov', :, :]
        self._state_cov_idx = ('state_cov',) + np.diag_indices(self.k_posdef)

        # Cache some slices
        self._params_intercept = np.s_[0:self.k_posdef]
        self._params_var = np.s_[self.k_posdef:self.k_posdef+self.k_var]
        self._params_variance = np.s_[self.k_posdef+self.k_var:]
        #self._params_cov = np.s_[self.k_var:self.k_var + self.k_posdef**2]

        # self._params_variance = self.k_var + np.r_[
        #     [i + i*k_posdef for i in range(k_posdef)]
        # ]

    def _get_model_names(self, latex=False):
        return np.arange(self.k_params).tolist()

    @property
    def endog_names(self):
        return np.arange(self.k_endog)

    @property
    def start_params(self):
        var_mod = var_model.VAR(self.endog.T)
        var_res = var_mod.fit(self.order, trend='c')
        params = np.array(var_res.params.T)

        #return np.r_[np.array(var_res.params.T).ravel(), np.eye(self.k_posdef).ravel()]
        return np.r_[params[:,0], params[:,1:].ravel(), [1]*self.k_posdef]

    def transform_params(self, unconstrained):
        constrained = np.copy(unconstrained)
        constrained[self._params_variance] = (
            constrained[self._params_variance]**2
        )
        return constrained

    def untransform_params(self, constrained):
        unconstrained = np.copy(constrained)
        unconstrained[self._params_variance] = (
            unconstrained[self._params_variance]**0.5
        )
        return unconstrained

    def update(self, params, *args, **kwargs):
        params = super(VAR, self).update(params, *args, **kwargs)

        self[self._state_intercept_idx] = params[self._params_intercept]
        self[self._transition_idx] = (
            params[self._params_var].reshape(self.k_posdef, self.k_states)
        )
        # self[self._state_cov_idx] = (
        #     params[self._params_cov].reshape(self.k_posdef, self.k_posdef)
        # )
        self[self._state_cov_idx] = (
            params[self._params_variance]
        )

