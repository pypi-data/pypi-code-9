from __future__ import print_function, division
from collections import defaultdict
import numpy as np
from scipy.stats import sem
from agaro.output_utils import (get_recent_model, get_filenames,
                                filename_to_model)


def get_average_measure(dirname, measure_func, t_steady=None):
    """
    Calculate a measure of a model in an output directory, averaged over
    all times when the model is at steady-state.

    Parameters
    ----------
    dirname: str
        Output directory
    measure_func: function
        Function which takes a :class:`Model` instance as a single argument,
        and returns the measure of interest, and its uncertainty.
    t_steady: None or float
        Time to consider the model to be at steady-state.
        `None` means just consider the latest time.

    Returns
    -------
    measure: numpy.ndarray
        Measure.
    measure_errs: numpy.ndarray
        Measure uncertainty.
        If no averaging is done, this is taken from the measure_func.
        Otherwise, the standard error over all samples is used.
    """
    if t_steady is None:
        meas, meas_err = measure_func(get_recent_model(dirname))
        return meas, meas_err
    else:
        ms = [filename_to_model(fname) for fname in get_filenames(dirname)]
        ms_steady = [m for m in ms if m.t > t_steady]
        meas_list = [measure_func(m) for m in ms_steady]
        meases, meas_errs = zip(*meas_list)
        return np.mean(meases), sem(meases)


def measures(dirnames, measure_func, t_steady=None):
    """Calculate a measure of a set of model output directories,
    for a measure function which returns an associated uncertainty.

    Parameters
    ----------
    dirnames: list[str]
        Model output directory paths.
    measure_func: function
        Function which takes a :class:`Model` instance as a single argument,
        and returns the measure of interest, and its uncertainty.
    t_steady: None or float
        Time to consider the model to be at steady-state.
        The measure will be averaged over all later times.
        `None` means just consider the latest time.

    Returns
    -------
    measures: numpy.ndarray
        Measures.
    measure_errs: numpy.ndarray
        Uncertainties.
    """
    measures, measure_errs = [], []
    for dirname in dirnames:
        meas, meas_err = get_average_measure(dirname, measure_func, t_steady)
        measures.append(meas)
        measure_errs.append(meas_err)
    return np.array(measures), np.array(measure_errs)


def params(dirnames, param_func, t_steady=None):
    """Calculate a parameter of a set of model output directories,
    for a measure function which returns an associated uncertainty.

    Parameters
    ----------
    dirnames: list[str]
        Model output directory paths.
    param_func: function
        Function which takes a :class:`Model` instance as a single argument,
        and returns the parameter of interest.

    Returns
    -------
    params: numpy.ndarray
        Parameters.
    """
    return np.array([param_func(get_recent_model(d)) for d in dirnames])


def t_measures(dirname, time_func, measure_func):
    """Calculate a measure over time for a single output directory,
    and its uncertainty.

    Parameters
    ----------
    dirname: str
        Path to a model output directory.
    time_func: function
        Function which takes a :class:`Model` instance as a single argument,
        and returns its time.
    measure_func: function
        Function which takes a :class:`Model` instance as a single argument,
        and returns the measure of interest, and its uncertainty.

    Returns
    -------
    ts: np.ndarray
        Times.
    measures: np.ndarray
        Measures.
    measure_errs: np.ndarray
        Measure uncertainties.
    """
    ts, measures, measure_errs = [], [], []
    for fname in get_filenames(dirname):
        m = filename_to_model(fname)
        ts.append(time_func(m))
        meas, meas_err = measure_func(m)
        measures.append(meas)
        measure_errs.append(meas_err)
    return np.array(ts), np.array(measures), np.array(measure_errs)


def group_by_key(dirnames, key):
    """Group a set of output directories according to a model parameter.

    Parameters
    ----------
    dirnames: list[str]
        Output directories
    key: various
        A field of a :class:`Model` instance.

    Returns
    -------
    groups: dict[various: list[str]]
        For each value of `key` that is found at least once in the models, a
        list of the output directories where `key` is that value.
    """
    groups = defaultdict(lambda: [])
    for dirname in dirnames:
        m = get_recent_model(dirname)
        groups[m.__dict__[key]].append(dirname)
    return dict(groups)
