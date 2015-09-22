"""
Tests for ssm package

Test against
- Kim and Nelson (1999)
- MATLAB
- MATLAB ssm toolbox
- Stata
- R (KFAS)
- SSFPack

---------------------------------------

Model types
- Large observation vector
- Missing data

Model options
- ???

Filter options
- filter_method
    - FILTER_CONVENTIONAL
    - FILTER_CONVENTIONAL | FILTER_COLLAPSED
    - FILTER_UNIVARIATE
    - FILTER_UNIVARIATE | FILTER_COLLAPSED
    - other (error)
- inversion_method
    - INVERSE_UNIVARIATE
    - SOLVE_LU
    - INVERT_LU
    - SOLVE_CHOLESKY
    - INVERT_CHOLESKY
    - other (error)
- stability_method
    - None
    - STABILITY_FORCE_SYMMETRY
    - other (error)
- conserve_memory
    - MEMORY_STORE_ALL
    - MEMORY_NO_FORECAST
    - MEMORY_NO_PREDICTED
    - MEMORY_NO_FILTERED
    - MEMORY_NO_LIKELIHOOD
    - MEMORY_NO_GAIN
    - MEMORY_NO_SMOOTHING
    - MEMORY_CONSERVE
    - other (error)
- loglikelihood_burn
    - Negative (error)
    - 0
    - Positive
    - >nobs (error)
- tolerance

Smoothing options
- smoothing_output
    - SMOOTHER_STATE
    - SMOOTHER_STATE_COV
    - SMOOTHER_DISTURBANCE
    - SMOOTHER_DISTURBANCE_COV
    - SMOOTHER_ALL
    - other (error)

Simulation smoothing options
- simulation_output
    - SIMULATION_STATE
    - SIMULATION_DISTURBANCE
    - SIMULATION_ALL
    - other (error)

---------------------------------------

General
- Dimensions
- Setting matrices
    - Entire matrix
    - Individual elements
    - As an attribute (model.design)
    - As a slice (mode['design'])

Model output
    - prefix
    - dtype
    - nobs
    - k_endog
    - k_states
    - k_posdef
    - time_invariant
    - endog
    - design
    - obs_intercept
    - obs_cov
    - transition
    - state_intercept
    - selection
    - state_cov
    - missing
    - nmissing
    - shapes
    - initialization

Filtering output
    - initial_state
    - initial_state_cov
    - converged
    - period_converged
    - filtered_state
    - filtered_state_cov
    - predicted_state
    - predicted_state_cov
    - kalman_gain
    - tmp1
    - tmp2
    - tmp3
    - tmp4
    - forecasts
    - forecasts_error
    - forecasts_error_cov
    - loglikelihood
    - collapsed_forecasts
    - collapsed_forecasts_error
    - collapsed_forecasts_error_cov

Smoothing output
    - scaled_smoothed_estimator
    - scaled_smoothed_estimator_cov
    - smoothing_error
    - smoothed_state
    - smoothed_state_cov
    - smoothed_measurement_disturbance
    - smoothed_state_disturbance
    - smoothed_measurement_disturbance_cov
    - smoothed_state_disturbance_cov

Simulation smoothing output
    - generated_obs
    - generated_state
    - simulated_state
    - simulated_measurement_disturbance
    - simulated_state_disturbance

Miscellaneous
- Stationary filter initialization
- Non-positive definite

Model construction
- Dynamic factors
- SARIMA
- Structural time series
- Regression

Model combination

Author: Chad Fulton
License: Simplified-BSD
"""
from __future__ import division, absolute_import, print_function

import numpy as np
import pandas as pd
import os

from dismalpy.ssm import _statespace, _kalman_filter
from numpy.testing import assert_allclose, assert_allclose
from nose.exc import SkipTest

current_path = os.path.dirname(os.path.abspath(__file__))

class StatespaceTest(object):

    def test_forecasts(self):
        assert_allclose(
            self.results_a.forecasts[0,:],
            self.results_b.forecasts[0,:]
        )

    @SkipTest
    def test_forecasts_error(self):
        assert_allclose(
            self.results_a.forecasts_error[0,:],
            self.results_b.forecasts_error[0,:]
        )

    @SkipTest
    def test_forecasts_error_cov(self):
        assert_allclose(
            self.results_a.forecasts_error_cov[0,0,:],
            self.results_b.forecasts_error_cov[0,0,:]
        )

    def test_filtered_state(self):
        assert_allclose(
            self.results_a.filtered_state,
            self.results_b.filtered_state
        )

    def test_filtered_state_cov(self):
        assert_allclose(
            self.results_a.filtered_state_cov,
            self.results_b.filtered_state_cov
        )

    def test_predicted_state(self):
        assert_allclose(
            self.results_a.predicted_state,
            self.results_b.predicted_state
        )

    def test_predicted_state_cov(self):
        assert_allclose(
            self.results_a.predicted_state_cov,
            self.results_b.predicted_state_cov
        )

    def test_loglike(self):
        assert_allclose(
            self.results_a.loglikelihood,
            self.results_b.loglikelihood
        )

    def test_scaled_smoothed_estimator(self):
        assert_allclose(
            self.results_a.scaled_smoothed_estimator,
            self.results_b.scaled_smoothed_estimator
        )

    def scaled_smoothed_estimator_cov(self):
        assert_allclose(
            self.results_a.scaled_smoothed_estimator_cov,
            self.results_b.scaled_smoothed_estimator_cov
        )

    def smoothing_error(self):
        assert_allclose(
            self.results_a.smoothing_error,
            self.results_b.smoothing_error
        )

    def test_smoothed_states(self):
        assert_allclose(
            self.results_a.smoothed_state,
            self.results_b.smoothed_state
        )

    def test_smoothed_states_cov(self):
        assert_allclose(
            self.results_a.smoothed_state_cov,
            self.results_b.smoothed_state_cov
        )

    @SkipTest
    def test_smoothed_measurement_disturbance(self):
        assert_allclose(
            self.results_a.smoothed_measurement_disturbance,
            self.results_b.smoothed_measurement_disturbance
        )

    @SkipTest
    def test_smoothed_measurement_disturbance_cov(self):
        assert_allclose(
            self.results_a.smoothed_measurement_disturbance_cov,
            self.results_b.smoothed_measurement_disturbance_cov
        )

    def test_smoothed_state_disturbance(self):
        assert_allclose(
            self.results_a.smoothed_state_disturbance,
            self.results_b.smoothed_state_disturbance
        )

    def test_smoothed_state_disturbance_cov(self):
        assert_allclose(
            self.results_a.smoothed_state_disturbance_cov,
            self.results_b.smoothed_state_disturbance_cov
        )

    def test_simulation_smoothed_state(self):
        assert_allclose(
            self.sim_a.simulated_state,
            self.sim_a.simulated_state
        )

    def test_simulation_smoothed_measurement_disturbance(self):
        assert_allclose(
            self.sim_a.simulated_measurement_disturbance,
            self.sim_a.simulated_measurement_disturbance
        )

    def test_simulation_smoothed_state_disturbance(self):
        assert_allclose(
            self.sim_a.simulated_state_disturbance,
            self.sim_a.simulated_state_disturbance
        )
