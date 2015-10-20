import os as _os
_on_rtd = _os.environ.get('READTHEDOCS', None) == 'True'
if not _on_rtd:
    import matplotlib.pyplot as _plt
    import numpy as _np

from .setup_axes import setup_axes as _setup_axes


def plot(*args, ax=None, **kwargs):
    """
    .. versionadded:: 1.4

    Plots but automatically resizes x axis.
    """
    if ax is None:
        fig, ax = _setup_axes()

    pl = ax.plot(*args, **kwargs)

    if _np.shape(args)[0] > 1:
        if type(args[1]) is not str:
            min_x = min(args[0])
            max_x = max(args[0])
            ax.set_xlim((min_x, max_x))

    return pl
