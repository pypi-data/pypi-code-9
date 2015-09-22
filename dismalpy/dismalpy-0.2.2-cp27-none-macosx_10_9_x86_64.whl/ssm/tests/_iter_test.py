import sys
if not sys.path[0] == '/Users/fulton/projects/pykalman_filter/':
    sys.path = ['/Users/fulton/projects/pykalman_filter/'] + sys.path

import numpy as np
import pandas as pd
import pykf
import matplotlib.pyplot as plt
from pykf.kalman_filter import dkalman_filter
from pykf._statespace import dIterableStatespace, dIncrementalKalmanFilter
from pykf.tests import results_kalman

def iterate_array(endog):
    nendog, nobs = endog.shape
    for t in range(nobs):
        yield 1

if __name__ == '__main__':

    # GDP, Quarterly, 1947.1 - 1995.3
    data = pd.DataFrame(
        results_kalman.uc_uni['data'],
        index=pd.date_range('1947-01-01', '1995-07-01', freq='QS'),
        columns=['GDP']
    )
    data['lgdp'] = np.log(data['GDP'])

    mod = pykf.Representation(data['lgdp'], nstates=4)

    # Statespace representation
    mod.design[:, :, 0] = [1, 1, 0, 0]
    mod.transition[([0, 0, 1, 1, 2, 3],
                    [0, 3, 1, 2, 1, 3],
                    [0, 0, 0, 0, 0, 0])] = [1, 1, 0, 0, 1, 1]
    mod.selection = np.eye(mod.nstates)

    # Update matrices with given parameters
    (sigma_v, sigma_e, sigma_w, phi_1, phi_2) = np.array(
        results_kalman.uc_uni['parameters']
    )
    mod.transition[([1, 1], [1, 2], [0, 0])] = [phi_1, phi_2]
    mod.state_cov[
        np.diag_indices(mod.nstates)+(np.zeros(mod.nstates, dtype=int),)] = [
        sigma_v**2, sigma_e**2, 0, sigma_w**2
    ]

    # Initialization
    initial_state = np.zeros((mod.nstates,))
    initial_state_cov = np.eye(mod.nstates)*100

    # Initialization: modification
    initial_state_cov = np.dot(
        np.dot(mod.transition[:, :, 0], initial_state_cov),
        mod.transition[:, :, 0].T
    )
    mod.initialize_known(initial_state, initial_state_cov)

    ss = dIterableStatespace(
        mod.nendog, mod.nstates, mod.nposdef,
        mod.obs, mod.design, mod.obs_intercept, mod.obs_cov,
        mod.transition, mod.state_intercept, mod.selection,
        mod.state_cov
    )
    ss.initialize_known(initial_state, np.asfortranarray(initial_state_cov))
    f = dIncrementalKalmanFilter(ss)

    next(f)