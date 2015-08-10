import os as _os
on_rtd = _os.environ.get('READTHEDOCS', None) == 'True'
if not on_rtd:
    import numpy as _np
    import scipy as _sp

import logging as _logging
logger = _logging.getLogger(__name__)


def fill_missing_timestamps(timestamp, values):
    # ======================================
    # Find the stats of the values
    # ======================================
    values_mean = _np.mean(values)
    values_std = _np.std(values)

    # ======================================
    # Find timestamp interval between each
    # step
    # ======================================
    offsets = timestamp[1:]-timestamp[:-1]
    mode_res = _sp.stats.mstats.mode(offsets)
    dt = mode_res[0][0]

    # ======================================
    # Start the arrays to fill
    # ======================================
    ts_new = _np.array([timestamp[0]])
    values_new = _np.array([values[0]])

    for ts_i, val_i in zip(timestamp[1:], values[1:]):
        # ======================================
        # Find gap from last time
        # ======================================
        gap = ts_i-ts_new[-1]

        # ======================================
        # Find number of intervals the gap is
        # ======================================
        n_dt = _np.round(gap/dt)

        # ======================================
        # Shots are missing if the gap is > 1*dt
        # ======================================
        if n_dt > 1:
            n_fill = n_dt - 1
            logger.warn('{} missing shot(s) after timestamp: {}'.format(n_fill, ts_new[-1]))

            # ======================================
            # Fill time info
            # ======================================
            t_fill = ts_new[-1] + dt * _np.linspace(1, n_fill, n_fill)
            logger.warn('Filling time: {}'.format(t_fill))
            ts_new = _np.append(ts_new, t_fill)

            # ======================================
            # Fill values with random values
            # ======================================
            val_fill    = _np.random.normal(values_mean, values_std, n_fill)
            logger.warn('Filling values: {}'.format(val_fill))
            values_new = _np.append(values_new, val_fill)

        # ======================================
        # Append next shot
        # ======================================
        ts_new     = _np.append(ts_new, ts_i)
        values_new = _np.append(values_new, val_i)

    return (ts_new, values_new)
