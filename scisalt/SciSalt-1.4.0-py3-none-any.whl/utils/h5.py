import numpy as _np


def keys(f):
    """
    .. versionadded:: 1.4

    Returns an array of strings of the keys like Python 2 used to do.
    """
    return [key for key in f.keys()]


def get(f, key, default=None):
    """
    .. versionadded:: 1.4

    Gets an array from datasets.
    """

    if key in f.keys():
        val = f[key].value

        if default is None:
            return val
        else:
            if _np.shape(val) == _np.shape(default):
                return val

    return default
