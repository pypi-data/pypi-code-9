import os as _os
_on_rtd = _os.environ.get('READTHEDOCS', None) == 'True'
if not _on_rtd:
    import numpy as _np
from .setup_figure import setup_figure as _setup_figure


def setup_axes(rows=1, cols=1, figsize=(8, 6), expand=True, **kwargs):
    """
    .. versionadded:: 1.2

    Sets up a figure of size *figsize* with a number of rows (*rows*) and columns (*cols*).

    Returns :code:`fig, axes`:
    
    * *fig*: The figure
    * *axes*: An array of all of the axes. (Unless there's only one axis, in which case it returns an object instance :class:`matplotlib.axis.Axis`.)
    """

    if expand:
        figsize = (figsize[0]*cols, figsize[1]*rows)

    fig, gs = _setup_figure(rows=rows, cols=cols, figsize=figsize)

    axes = _np.empty(shape=(rows, cols), dtype=object)

    for i in range(rows):
        for j in range(cols):
            axes[i, j] = fig.add_subplot(gs[i, j], **kwargs)

    if axes.shape == (1, 1):
        return fig, axes[0, 0]
    else:
        return fig, axes
