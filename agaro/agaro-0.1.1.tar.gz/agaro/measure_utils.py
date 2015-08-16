from __future__ import print_function, division
from collections import defaultdict
import numpy as np
from agaro.output_utils import (get_recent_model, get_filenames,
                                filename_to_model)


def get_average_measure(dirname, get_measure_func, t_steady=None):
    """
    Calculate a measure of a model in an output directory, averaged over
    all times when the model is at steady-state.

    Parameters
    ----------
    dirname: str
        Output directory
    get_measure_func: function
        Function which takes a :class:`Model` instance as a single argument,
        and returns the measure of interest.
    t_steady: None or float
        Time to consider the model to be at steady-state.
        `None` means just consider the latest time.

    Returns
    -------
    measure: various
        Average measure.
    """
    if t_steady is None:
        return get_measure_func(get_recent_model(dirname))
    else:
        ms = [filename_to_model(fname) for fname in get_filenames(dirname)]
        ms_steady = [m for m in ms if m.t > t_steady]
        return np.mean([get_measure_func(m) for m in ms_steady])


def measures(dirnames, measure_func, t_steady=None):
    """Calculate a measure of a set of
    model output directories.

    Parameters
    ----------
    dirnames: list[str]
        Model output directory paths.
    t_steady: None or float
        Time to consider the model to be at steady-state.
        The measure will be averaged over all later times.
        `None` means just consider the latest time.

    Returns
    -------
    measures: numpy.ndarray[dtype=float]
        Measures.
    """
    measures = []
    for dirname in dirnames:
        measures.append(get_average_measure(dirname, measure_func, t_steady))
    return np.array(measures)


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
