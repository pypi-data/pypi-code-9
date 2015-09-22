"""
Multivariate Kalman Filter (Python)

Author: Chad Fulton
License: Simplified-BSD

"""
from __future__ import division, absolute_import, print_function

import numpy as np
from scipy.linalg import solve_discrete_lyapunov, blas, lapack


def py_kalman_filter(model, dtype=None, return_loglike=False):
    # Parameters
    if dtype is None:
        dtype = model.obs.dtype

    # Dimensions
    nobs = model.nobs
    k_endog = model.k_endog
    k_states = model.k_states
    k_posdef = model.k_posdef

    # Allocate memory for variables
    filtered_state = np.zeros((k_states, nobs), dtype=dtype)
    filtered_state_cov = np.zeros((k_states, k_states, nobs), dtype=dtype)
    predicted_state = np.zeros((k_states, nobs+1), dtype=dtype)
    predicted_state_cov = np.zeros((k_states, k_states, nobs+1), dtype=dtype)
    forecast = np.zeros((k_endog, nobs), dtype=dtype)
    forecast_error = np.zeros((k_endog, nobs), dtype=dtype)
    forecast_error_cov = np.zeros((k_endog, k_endog, nobs), dtype=dtype)
    loglikelihood = np.zeros((nobs+1,), dtype=dtype)

    # Selected state covariance matrix
    selected_state_cov = (
        np.dot(
            np.dot(model.selection[:, :, 0],
                   model.state_cov[:, :, 0]),
            model.selection[:, :, 0].T
        )
    )

    # Initial values
    if model.initialization == 'known':
        initial_state = model._initial_state.astype(dtype)
        initial_state_cov = model._initial_state_cov.astype(dtype)
    elif model.initialization == 'approximate_diffuse':
        initial_state = np.zeros((k_states,), dtype=dtype)
        initial_state_cov = (
            np.eye(k_states).astype(dtype) * model._initial_variance
        )
    elif model.initialization == 'stationary':
        initial_state = np.zeros((k_states,), dtype=dtype)
        initial_state_cov = solve_discrete_lyapunov(
            np.array(model.transition[:, :, 0], dtype=dtype),
            np.array(selected_state_cov[:, :], dtype=dtype),
        )
    else:
        raise RuntimeError('Statespace model not initialized.')

    # Copy initial values to predicted
    predicted_state[:, 0] = initial_state
    predicted_state_cov[:, :, 0] = initial_state_cov
    # print(predicted_state_cov[:, :, 0])

    # Setup indices for possibly time-varying matrices
    design_t = 0
    obs_intercept_t = 0
    obs_cov_t = 0
    transition_t = 0
    state_intercept_t = 0
    selection_t = 0
    state_cov_t = 0

    # Iterate forwards
    time_invariant = model.time_invariant
    for t in range(nobs):
        # Get indices for possibly time-varying arrays
        if not time_invariant:
            if model.design.shape[2] > 1:             design_t = t
            if model.obs_intercept.shape[1] > 1:      obs_intercept_t = t
            if model.obs_cov.shape[2] > 1:            obs_cov_t = t
            if model.transition.shape[2] > 1:         transition_t = t
            if model.state_intercept.shape[1] > 1:    state_intercept_t = t
            if model.selection.shape[2] > 1:          selection_t = t
            if model.state_cov.shape[2] > 1:          state_cov_t = t

        # Selected state covariance matrix
        if model.selection.shape[2] > 1 or model.state_cov.shape[2] > 1:
            selected_state_cov = (
                np.dot(
                    np.dot(model.selection[:, :, selection_t],
                           model.state_cov[:, :, state_cov_t]),
                    model.selection[:, :, selection_t].T
                )
            )

        # #### Forecast for time t
        # `forecast` $= Z_t a_t + d_t$
        #
        # *Note*: $a_t$ is given from the initialization (for $t = 0$) or
        # from the previous iteration of the filter (for $t > 0$).
        forecast[:, t] = (
            np.dot(model.design[:, :, design_t], predicted_state[:, t]) +
            model.obs_intercept[:, obs_intercept_t]
        )

        # *Intermediate calculation* (used just below and then once more)  
        # `tmp1` array used here, dimension $(m \times p)$  
        # $\\#_1 = P_t Z_t'$  
        # $(m \times p) = (m \times m) (p \times m)'$
        tmp1 = np.dot(predicted_state_cov[:, :, t],
                      model.design[:, :, design_t].T)

        # #### Forecast error for time t
        # `forecast_error` $\equiv v_t = y_t -$ `forecast`
        forecast_error[:, t] = model.obs[:, t] - forecast[:, t]

        # #### Forecast error covariance matrix for time t
        # $F_t \equiv Z_t P_t Z_t' + H_t$
        forecast_error_cov[:, :, t] = (
            np.dot(model.design[:, :, design_t], tmp1) +
            model.obs_cov[:, :, obs_cov_t]
        )
        # Store the inverse
        if k_endog == 1:
            forecast_error_cov_inv = 1 / forecast_error_cov[0, 0, t]
            determinant = forecast_error_cov[0, 0, t]
        else:
            forecast_error_cov_inv = np.linalg.inv(forecast_error_cov[:, :, t])
            determinant = np.linalg.det(forecast_error_cov[:, :, t])
        # Make a new temporary array
        tmp2 = np.dot(tmp1, forecast_error_cov_inv)
        # print(predicted_state_cov[:, :, t])

        # #### Filtered state for time t
        # $a_{t|t} = a_t + P_t Z_t' F_t^{-1} v_t$  
        # $a_{t|t} = 1.0 * \\#_1 \\#_2 + 1.0 a_t$
        filtered_state[:, t] = (
            predicted_state[:, t] + np.dot(tmp2, forecast_error[:, t])
        )

        # #### Filtered state covariance for time t
        # $P_{t|t} = P_t - P_t Z_t' F_t^{-1} Z_t P_t$  
        # $P_{t|t} = P_t - \\#_1 \\#_3 P_t$  
        filtered_state_cov[:, :, t] = (
            predicted_state_cov[:, :, t] -
            np.dot(
                np.dot(tmp2, model.design[:, :, design_t]),
                predicted_state_cov[:, :, t]
            )
        )

        # #### Loglikelihood
        loglikelihood[t] = -0.5 * (
            np.log((2*np.pi)**k_endog * determinant) +
            np.dot(
                forecast_error[:, t],
                np.dot(forecast_error_cov_inv, forecast_error[:, t])
            )
        )

        # #### Predicted state for time t+1
        # $a_{t+1} = T_t a_{t|t} + c_t$
        predicted_state[:, t+1] = (
            np.dot(model.transition[:, :, transition_t],
                   filtered_state[:, t]) +
            model.state_intercept[:, state_intercept_t]
        )

        # #### Predicted state covariance matrix for time t+1
        # $P_{t+1} = T_t P_{t|t} T_t' + Q_t^*$
        predicted_state_cov[:, :, t+1] = (
            np.dot(
                np.dot(model.transition[:, :, transition_t],
                       filtered_state_cov[:, :, t]),
                model.transition[:, :, transition_t].T
            ) + selected_state_cov
        )

    if return_loglike:
            return np.array(loglikelihood)
    else:
        return FilterResults(model, filtered_state, filtered_state_cov,
                             predicted_state, predicted_state_cov, forecast,
                             forecast_error, forecast_error_cov, loglikelihood)

