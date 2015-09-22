"""
Univariate structural time series models

Author: Chad Fulton
License: Simplified-BSD
"""
from __future__ import division, absolute_import#, print_function

from warnings import warn
from collections import OrderedDict

import numpy as np
from .mlemodel import MLEModel
from scipy.linalg import solve_discrete_lyapunov
from .tools import companion_matrix, constrain_stationary_univariate, unconstrain_stationary_univariate

class Seasonal(MLEModel):
    
    def __init__(self, endog, k_seasons=4):
        # Model parameters
        self.k_seasons = k_seasons
        k_states = k_seasons-1
        k_posdef = 1

        super(Seasonal, self).__init__(endog, k_states, k_posdef=k_posdef)

        # Initialize the matrices
        self['design', 0, 0] = 1
        self['transition', :, :] = companion_matrix(np.r_[1, [1]*k_states]).T
        self['selection', 0, 0] = 1

    @property
    def start_params(self):
        return [0.1, 0.1]

    def transform_params(self, params):
        return params**2

    def update(self, params, **kwargs):
        params = super(Seasonal, self).update(params, **kwargs)

        self['obs_cov', 0, 0] = params[0]
        self['state_cov', 0, 0] = params[1]

class Cycle(MLEModel):
    
    def __init__(self, endog):
        # Model parameters
        k_states = 2
        k_posdef = 2

        super(Cycle, self).__init__(endog, k_states, k_posdef=k_posdef)

        # Initialize the matrices
        self['design', 0, 0] = 1
        self['selection'] = np.eye(k_states)

        idx = np.diag_indices(k_states)
        self._idx_state_cov = ('state_cov', idx[0], idx[1])

    @property
    def start_params(self):
        return [0.1, 1, 0.1]

    def transform_params(self, params):
        params[:1] = params[:1]**2
        params[2:] = params[2:]**2
        return params

    def update(self, params, **kwargs):
        params = super(Cycle, self).update(params, **kwargs)

        self['obs_cov', 0, 0] = params[0]
        cos = np.cos(params[1])
        sin = np.sin(params[1])
        self['transition', :, :] = np.array([[cos, sin],
                                            [-sin, cos]])
        self[self._idx_state_cov] = params[2]

class LocalLinearTrend(MLEModel):
    r"""
    Local Linear Trend model

    ..math::

        y_t & = \mu_t + \varepsilon_t \qquad & \varepsilon_t \sim
            N(0, \sigma_\varepsilon^2) \\
        \mu_{t+1} & = \mu_t + \nu_t + \xi_t & \xi_t \sim N(0, \sigma_\xi^2) \\
        \nu_{t+1} & = \nu_t + \zeta_t & \zeta_t \sim N(0, \sigma_\zeta^2)

    """
    def __init__(self, endog, stochastic_level=True, stochastic_trend=True,
                 *args, **kwargs):
        # Model parameters
        self.stochastic_level = stochastic_level
        self.stochastic_trend = stochastic_trend

        # Model order
        k_states = 2
        k_posdef = int(stochastic_level + stochastic_trend)

        # Initialize the statespace
        super(LocalLinearTrend, self).__init__(
            endog, k_states=k_states, k_posdef=k_posdef, *args, **kwargs
        )

        # Initialize the matrices
        self.design = np.r_[1, 0]
        self.transition = np.array([[1, 1],
                                    [0, 1]])
        if self.stochastic_level and self.stochastic_trend:
            self.selection = np.eye(k_states)
        elif self.stochastic_level:
            self.selection = np.array([1, 0]).reshape((2, 1))
        elif self.stochastic_trend:
            self.selection = np.array([0, 1]).reshape((2, 1))

        # Cache some indices
        self._obs_cov_idx = np.diag_indices(k_posdef)

        # Initialize diffuse
        self.initialize_approximate_diffuse()
        self.loglikelihood_burn = self.k_states

    def _get_model_names(self, latex=False):
        names = []

        if latex:
            template = '$\\sigma_%s^2$'
            names.append(template % '\\varepsilon')
            if self.stochastic_level:
                names.append(template % '\\xi')
            if self.stochastic_trend:
                names.append(template % '\\zeta')
        else:
            template = 'sigma2.%s'
            names.append(template % 'measurement')
            if self.stochastic_level:
                names.append(template % 'level')
            if self.stochastic_trend:
                names.append(template % 'trend')
        return names

    @property
    def start_params(self):
        # There are up to three parameters: sigma2_eps, sigma2_xi, and
        # sigma2_zeta
        measurement_variance = [1]
        level_variance = [1] if self.stochastic_level else []
        trend_variance = [1] if self.stochastic_trend else []
        return np.r_[measurement_variance, level_variance, trend_variance]

    def transform_params(self, unconstrained):
        # Parameters must all be positive for likelihood evaluation
        return unconstrained**2

    def untransform_params(self, constrained):
        return constrained**0.5

    def update(self, params, *args, **kwargs):
        params = super(LocalLinearTrend, self).update(params, *args, **kwargs)

        idx = 0
        measurement_variance = params[idx]
        idx += 1
        if self.stochastic_level:
            level_variance = params[idx]
            idx += 1
        if self.stochastic_trend:
            trend_variance = params[idx]
            idx += 1

        # Observation covariance
        if self.obs_cov.dtype == params.dtype:
            self.obs_cov[0] = measurement_variance
        else:
            obs_cov = self.obs_cov.real.astype(params.dtype)
            obs_cov[0] = measurement_variance
            self.obs_cov = obs_cov

        # State covariance
        if self.stochastic_level or self.stochastic_trend:
            state_cov = self.state_cov.real.astype(params.dtype)
            if self.stochastic_level and self.stochastic_trend:
                state_cov_diagonal = np.array(
                    [level_variance, trend_variance]
                ).reshape((2, 1))
            elif self.stochastic_level:
                state_cov_diagonal = np.array([level_variance]).reshape((1, 1))
            elif self.stochastic_trend:
                state_cov_diagonal = np.array([trend_variance]).reshape((1, 1))
            state_cov[self._obs_cov_idx] = state_cov_diagonal
            self.state_cov = state_cov


class StructuralTimeSeries(MLEModel):
    r"""
    Univariate structural time series model

    These are also known as unobserved components models, and decompose a
    (univariate) time series into trend, seasonal, cyclical, and irregular
    components.

    Parameters
    ----------

    level : bool, optional
        Whether or not to include a level component. Default is False.
    trend : bool, optional
        Whether or not to include a trend component. Default is False. If True,
        `level` must also be True.
    seasonal_period : int or None, optional
        The period of the seasonal component. Default is None.
    cycle : bool, optional
        Whether or not to include a cycle component. Default is False.
    ar : int or None, optional
        The order of the autoregressive component. Default is None.
    exog : array_like or None, optional
        Exoenous variables.
    irregular : bool, optional
        Whether or not to include an irregular component. Default is True
    stochastic_level : bool, optional
        Whether or not any level component is stochastic. Default is True.
    stochastic_trend : bool, optional
        Whether or not any trend component is stochastic. Default is True.
    stochastic_seasonal : bool, optional
        Whether or not any seasonal component is stochastic. Default is True.
    stochastic_cycle : bool, optional
        Whether or not any cycle component is stochastic. Default is True.
    damped_cycle : bool, optional
        Whether or not the cycle component is damped. Default is False.

    Notes
    -----

    Thse models take the general form (see [1]_ Chapter 3.2 for all details)

    .. math::

        y_t = \mu_t + \gamma_t + c_t + \varepsilon_t

    where :math:`y_t` refers to the observation vector at time :math:`t`,
    :math:`\mu_t` refers to the trend component, :math:`\gamma_t` refers to the
    seasonal component, :math:`c_t` refers to the cycle, and
    :math:`\varepsilon_t` is the irregular. The modeling details of these
    components are given below.

    **Trend**

    The trend is modeled either as a *local linear trend* model or as an
    *integrated random walk* model.

    The local linear trend is specified as:

    .. math::

        \mu_t = \mu_{t-1} + \nu_{t-1} + \xi_{t-1} \\
        \nu_t = \nu_{t-1} + \zeta_{t-1}

    with :math:`\xi_t \sim N(0, \sigma_\xi^2)` and
    :math:`\zeta_t \sim N(0, \sigma_\zeta^2)`.

    The integrated random walk model of order `r` is specified as:

    .. math::

        \Delta^r \mu_t = \xi_{t-1} \\

    This component results in two parameters to be selected via maximum
    likelihood: :math:`\sigma_\xi^2` and :math:`\sigma_\zeta^2`.

    In the case of the integrated random walk model, the parameter
    :math:`\sigma_\xi^2` is constrained to be zero, but the parameter `r` (the
    order of integration) must be chosen (it is not estimated by MLE).

    **Seasonal**

    The seasonal component is modeled as:

    .. math::

        \gamma_t = - \sum_{j=1}^{s-1} \gamma_{t+1-j} + \omega_t \\
        \omega_t \sim N(0, \sigma_\omega^2)

    where s is the number of seasons and :math:`\omega_t` is an error term that
    allows the seasonal constants to change over time (if this is not desired,
    :math:`\sigma_\omega^2` can be set to zero).

    This component results in one parameter to be selected via maximum
    likelihood: :math:`\sigma_\omega^2`, and one parameter to be chosen, the
    number of seasons `s`.

    **Cycle**

    The cyclical component is modeled as

    .. math::

        c_{t+1} = \rho_c (\tilde c_t \cos \lambda_c t
                + \tilde c_t^* \sin \lambda_c) +
                \tilde \omega_t \\
        c_{t+1}^* = \rho_c (- \tilde c_t \sin \lambda_c  t +
                \tilde c_t^* \cos \lambda_c) +
                \tilde \omega_t^* \\

    where :math:`\omega_t, \tilde \omega_t iid N(0, \sigma_{\tilde \omega}^2)`

    This component results in three parameters to be selected via maximum
    likelihood: :math:`\sigma_{\tilde \omega}^2`, :math:`\rho_c`, and
    :math:`\lambda_c`.

    **Irregular**

    The irregular components are independent and identically distributed (iid):

    .. math::

        \varepsilon_t \sim N(0, \sigma_\varepsilon^2)

    TODO
    ----

    - Make sure cycle is economically interpretable (add damping, check period)
    - Check results in Stata for price series

    References
    ----------

    .. [1] Durbin, James, and Siem Jan Koopman. 2012.
       Time Series Analysis by State Space Methods: Second Edition.
       Oxford University Press.
    """

    def __init__(self, endog, level=False, trend=False, seasonal=None,
                 cycle=False, ar=None, exog=None, irregular=True,
                 stochastic_level=True, stochastic_trend=True,
                 stochastic_seasonal=True, stochastic_cycle=True,
                 damped_cycle=False, mle_regression=False,
                 **kwargs):

        # Model options
        self.level = level
        self.trend = trend
        self.seasonal_period = seasonal if seasonal is not None else 0
        self.seasonal = seasonal > 0
        self.cycle = cycle
        self.ar_order = ar if ar is not None else 0
        self.ar = self.ar_order > 0
        self.irregular = irregular

        self.stochastic_level = stochastic_level
        self.stochastic_trend = stochastic_trend
        self.stochastic_seasonal = stochastic_seasonal
        self.stochastic_cycle = stochastic_cycle

        self.damped_cycle = damped_cycle
        self.mle_regression = mle_regression

        if trend and not level:
            warn("Trend component specified without level component;"
                 " level component added.")
            self.level = True

        # Exogenous component
        self.k_exog = 0
        if exog is not None:
            exog = np.array(exog)
            self.k_exog = exog.shape[1]
        self.regression = self.k_exog > 0

        # Model parameters
        k_states = (
            self.level + self.trend +
            (self.seasonal_period - 1) * self.seasonal +
            self.cycle * 2 +
            self.ar_order + 
            (not self.mle_regression) * self.k_exog
        )
        k_posdef = (
            self.stochastic_level * self.level +
            self.stochastic_trend * self.trend +
            self.stochastic_seasonal * self.seasonal +
            self.stochastic_cycle * (self.cycle * 2) +
            self.ar
        )

        # We can still estimate the model with just the irregular component,
        # just need to have one state that does nothing.
        loglikelihood_burn = k_states - self.ar_order
        if k_states == 0:
            if not irregular:
                raise ValueError('Model has no components specified.')
            k_states = 1
        if k_posdef == 0:
            k_posdef = 1

        # Setup the representation
        super(StructuralTimeSeries, self).__init__(
            endog, k_states, k_posdef=k_posdef, exog=exog, **kwargs
        )
        self.setup()

        # Initialize the model
        self.loglikelihood_burn = loglikelihood_burn

        # Need to reset the MLE names (since when they were first set, `setup`
        # had not been run (and could not have been at that point))
        self.data.param_names = self.param_names
 
    def setup(self):
        """
        Setup the structural time series representation
        """
        # TODO fix this
        # (if we don't set it here, each instance shares a single dictionary)
        self._start_params = {
            'irregular_var': 0.1,
            'level_var': 0.1,
            'trend_var': 0.1,
            'seasonal_var': 0.1,
            'cycle_freq': 0.1,
            'cycle_var': 0.1,
            'cycle_damp': 0.1,
            'ar_coeff': 0,
            'ar_var': 0.1,
            'reg_coeff': 0,
        }
        self._param_names = {
            'irregular_var': 'sigma2.irregular',
            'level_var': 'sigma2.level',
            'trend_var': 'sigma2.trend',
            'seasonal_var': 'sigma2.seasonal',
            'cycle_var': 'sigma2.cycle',
            'cycle_freq': 'frequency.cycle',
            'cycle_damp': 'damping.cycle',
            'ar_coeff': 'ar.L%d',
            'ar_var': 'sigma2.ar',
            'reg_coeff': 'beta.%d',
        }

        # Initialize the ordered sets of parameters
        self.parameters = OrderedDict()
        self.parameters_obs_intercept = OrderedDict()
        self.parameters_obs_cov = OrderedDict()
        self.parameters_transition = OrderedDict()
        self.parameters_state_cov = OrderedDict()

        # Initialize the fixed components of the state space matrices,
        i = 0  # state offset
        j = 0  # state covariance offset

        if self.irregular:
            self.parameters_obs_cov['irregular_var'] = 1
        if self.level:
            self['design', 0, i] = 1.
            self['transition', i, i] = 1.
            if self.trend:
                self['transition', i, i+1] = 1.
            if self.stochastic_level:
                self['selection', i, j] = 1.
                self.parameters_state_cov['level_var'] = 1
                j += 1
            i += 1
        if self.trend:
            self['transition', i, i] = 1.
            if self.stochastic_trend:
                self['selection', i, j] = 1.
                self.parameters_state_cov['trend_var'] = 1
                j += 1
            i += 1
        if self.seasonal:
            n = self.seasonal_period - 1
            self['design', 0, i] = 1.
            self['transition', i:i + n, i:i + n] = (
                companion_matrix(np.r_[1, [1] * n]).transpose()
            )
            if self.stochastic_seasonal:
                self['selection', i, j] = 1.
                self.parameters_state_cov['seasonal_var'] = 1
                j += 1
            i += n
        if self.cycle:
            self['design', 0, i] = 1.
            self.parameters_transition['cycle_freq'] = 1
            if self.damped_cycle:
                self.parameters_transition['cycle_damp'] = 1
            if self.stochastic_cycle:
                self['selection', i:i+2, j:j+2] = np.eye(2)
                self.parameters_state_cov['cycle_var'] = 1
                j += 1
            self._idx_cycle_transition = np.s_['transition', i:i+2, i:i+2]
            i += 2
        if self.ar:
            self['design', 0, i] = 1.
            self.parameters_transition['ar_coeff'] = self.ar_order
            self.parameters_state_cov['ar_var'] = 1
            self['selection', i, j] = 1
            self['transition', i:i+self.ar_order, i:i+self.ar_order] = (
                companion_matrix(self.ar_order).T
            )
            self._idx_ar_transition = (
                np.s_['transition', i, i:i+self.ar_order]
            )
            self._start_params['ar_coeff'] = (
                [self._start_params['ar_coeff']] * self.ar_order
            )
            self._param_names['ar_coeff'] = [
                self._param_names['ar_coeff'] % k
                for k in range(1, self.ar_order+1)
            ]
            j += 1
            i += self.ar_order
        if self.regression:
            if self.mle_regression:
                self.parameters_obs_intercept['reg_coeff'] = self.k_exog
                self._start_params['reg_coeff'] = (
                    [self._start_params['reg_coeff']] * self.k_exog
                )
                self._param_names['reg_coeff'] = [
                    self._param_names['reg_coeff'] % k
                    for k in range(1, self.k_exog+1)
                ]
            else:
                design = np.repeat(self['design', :, :, 0], self.nobs, axis=0)
                self['design'] = design.transpose()[np.newaxis, :, :]
                self['design', 0, i:i+self.k_exog, :] = self.exog.transpose()
                self['transition', i:i+self.k_exog, i:i+self.k_exog] = (
                    np.eye(self.k_exog)
                )

                i += self.k_exog


        # Update to get the actual parameter set
        self.parameters.update(self.parameters_obs_cov)
        self.parameters.update(self.parameters_state_cov)
        self.parameters.update(self.parameters_transition)  # ordered last
        self.parameters.update(self.parameters_obs_intercept)

        self.k_obs_intercept = sum(self.parameters_obs_intercept.values())
        self.k_obs_cov = sum(self.parameters_obs_cov.values())
        self.k_transition = sum(self.parameters_transition.values())
        self.k_state_cov = sum(self.parameters_state_cov.values())
        self.k_params = sum(self.parameters.values())

        # Other indices
        idx = np.diag_indices(self.k_posdef)
        self._idx_state_cov = ('state_cov', idx[0], idx[1])

    def initialize_state(self):
        # Initialize the AR component as stationary, the rest as approximately
        # diffuse
        initial_state = np.zeros(self.k_states)
        initial_state_cov = (
            np.eye(self.k_states, dtype=self.transition.dtype) *
            self.initial_variance
        )

        if self.ar:

            start = (
                self.level + self.trend +
                (self.seasonal_period - 1) * self.seasonal +
                self.cycle * 2
            )
            end = start + self.ar_order
            selection_stationary = self.selection[start:end, :, 0]
            selected_state_cov_stationary = np.dot(
                np.dot(selection_stationary, self.state_cov[:, :, 0]),
                selection_stationary.T
            )
            try:
                initial_state_cov_stationary = solve_discrete_lyapunov(
                    self.transition[start:end, start:end, 0],
                    selected_state_cov_stationary
                )
            except:
                initial_state_cov_stationary = solve_discrete_lyapunov(
                    self.transition[start:end, start:end, 0],
                    selected_state_cov_stationary,
                    method='direct'
                )

            initial_state_cov[start:end, start:end] = (
                initial_state_cov_stationary
            )

        self.initialize_known(initial_state, initial_state_cov)

    _start_params = {
        'irregular_var': 0.1,
        'level_var': 0.1,
        'trend_var': 0.1,
        'seasonal_var': 0.1,
        'cycle_freq': 0.1,
        'cycle_var': 0.1,
        'cycle_damp': 0.1,
        'ar_coeff': 0,
        'ar_var': 0.1,
        'reg_coeff': 0,
    }

    @property
    def start_params(self):
        if not hasattr(self, 'parameters'):
            return []
        start_params = []
        for key in self.parameters.keys():
            if np.isscalar(self._start_params[key]):
                start_params.append(self._start_params[key])
            else:
                start_params += self._start_params[key]
        return start_params

    _param_names = {
        'irregular_var': 'sigma2.irregular',
        'level_var': 'sigma2.level',
        'trend_var': 'sigma2.trend',
        'seasonal_var': 'sigma2.seasonal',
        'cycle_var': 'sigma2.cycle',
        'cycle_freq': 'frequency.cycle',
        'cycle_damp': 'damping.cycle',
        'ar_coeff': 'ar.L%d',
        'ar_var': 'sigma2.ar',
        'reg_coeff': 'beta.%d',
    }

    @property
    def param_names(self):
        if not hasattr(self, 'parameters'):
            return []
        param_names = []
        for key in self.parameters.keys():
            if np.isscalar(self._param_names[key]):
                param_names.append(self._param_names[key])
            else:
                param_names += self._param_names[key]
        return param_names

    def transform_params(self, unconstrained):
        """
        Transform unconstrained parameters used by the optimizer to constrained
        parameters used in likelihood evaluation
        """
        constrained = np.zeros(unconstrained.shape, dtype=unconstrained.dtype)

        # Positive parameters: obs_cov, state_cov, and first transition
        # parameter (which is cycle_freq)
        offset = self.k_obs_cov + self.k_state_cov + self.cycle
        constrained[:offset] = unconstrained[:offset]**2

        # Cycle damping (if present) must be between 0 and 1
        if self.damped_cycle:
            constrained[offset] = (
                1 / (1 + np.exp(-unconstrained[offset]))
            )
            offset += 1

        # Autoregressive coefficients must be stationary
        if self.ar:
            constrained[offset:offset + self.ar_order] = (
                constrain_stationary_univariate(unconstrained[offset:offset + self.ar_order])
            )
            offset += self.ar_order

        # Nothing to do with betas
        constrained[offset:offset + self.k_exog] = unconstrained[offset:offset + self.k_exog] 

        return constrained

    def untransform_params(self, constrained):
        """
        Reverse the transformation
        """
        unconstrained = np.zeros(constrained.shape, dtype=constrained.dtype)

        # Positive parameters: obs_cov, state_cov, and first transition
        # parameter (which is cycle_freq)
        offset = self.k_obs_cov + self.k_state_cov + self.cycle
        unconstrained[:offset] = constrained[:offset]**0.5

        # Cycle damping (if present) must be between 0 and 1
        if self.damped_cycle:
            unconstrained[offset] = np.log(
                unconstrained[offset] / (1 - unconstrained[offset])
            )
            offset += 1

        # Autoregressive coefficients must be stationary
        if self.ar:
            unconstrained[offset:offset + self.ar_order] = (
                unconstrain_stationary_univariate(constrained[offset:offset + self.ar_order])
            )
            offset += self.ar_order

        # Nothing to do with betas
        unconstrained[offset:offset + self.k_exog] = constrained[offset:offset + self.k_exog] 

        return unconstrained

    def update(self, params, **kwargs):
        params = super(StructuralTimeSeries, self).update(params, **kwargs)

        offset = 0

        # Observation covariance
        if self.irregular:
            self['obs_cov', 0, 0] = params[offset]
            offset += 1

        # State covariance
        if self.k_state_cov > 0:
            variances = params[offset:offset+self.k_state_cov]
            if self.stochastic_cycle and self.cycle:
                if self.ar:
                    variances = np.r_[variances[:-1], variances[-2:]]
                else:
                    variances = np.r_[variances, variances[-1]]
            self[self._idx_state_cov] = variances
            offset += self.k_state_cov

        # Cycle transition
        if self.cycle:
            cos_freq = np.cos(params[offset])
            sin_freq = np.sin(params[offset])
            cycle_transition = np.array(
                [[cos_freq, sin_freq],
                 [-sin_freq, cos_freq]]
            )
            if self.damped_cycle:
                offset += 1
                cycle_transition *= params[offset]
            self[self._idx_cycle_transition] = cycle_transition
            offset += 1

        # AR transition
        if self.ar:
            self[self._idx_ar_transition] = params[offset:offset+self.ar_order]
            offset += self.ar_order

        # Beta observation intercept
        if self.regression:
            if self.mle_regression:
                self['obs_intercept'] = np.dot(self.exog, params[offset:offset+self.k_exog])[None, :]
            offset += self.k_exog

        # Initialize the state
        self.initialize_state()
