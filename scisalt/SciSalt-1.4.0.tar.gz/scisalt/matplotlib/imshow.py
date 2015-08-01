import os as _os
_on_rtd = _os.environ.get('READTHEDOCS', None) == 'True'
if not _on_rtd:
    import matplotlib.pyplot as _plt
    import matplotlib as _mpl
    import numpy as _np

from .colorbar import colorbar as _cb
from .setup_axes import setup_axes as _setup_axes

_CONTOUR = 1
_IMSHOW  = 2
_QUIVER  = 3

__all__ = [
        'contour',
        'imshow',
        'scaled_figsize'
        ]


def imshow(X, ax=None, add_cbar=True, rescale_fig=True, **kwargs):
    """
    .. versionadded:: 1.3

    Plots an array *X* such that the first coordinate is the *x* coordinate and the second coordinate is the *y* coordinate, with the origin at the bottom left corner.

    Optional argument *ax* allows an existing axes to be used.

    *\*\*kwargs* are passed on to :meth:`matplotlib.axes.Axes.imshow`.

    Returns :class:`matplotlib.image.AxesImage`.
    """
    return _plot_array(_IMSHOW, X, ax=ax, add_cbar=add_cbar, rescale_fig=rescale_fig, **kwargs)


def contour(X, ax=None, add_cbar=True, rescale_fig=True, **kwargs):
    """
    .. versionadded:: 1.3

    Plots an array *X* such that the first coordinate is the *x* coordinate and the second coordinate is the *y* coordinate, with the origin at the bottom left corner.

    Optional argument *ax* allows an existing axes to be used.

    *\*\*kwargs* are passed on to :meth:`matplotlib.axes.Axes.contour`.

    Returns :class:`matplotlib.image.AxesImage`.
    """
    return _plot_array(_CONTOUR, X, ax=ax, add_cbar=add_cbar, rescale_fig=rescale_fig, **kwargs)


def quiver(U, V, ax=None, rescale_fig=True, **kwargs):
    """
    .. versionadded:: 1.3

    Plots an array *X* such that the first coordinate is the *x* coordinate and the second coordinate is the *y* coordinate, with the origin at the bottom left corner.

    Optional argument *ax* allows an existing axes to be used.

    *\*\*kwargs* are passed on to :meth:`matplotlib.axes.Axes.quiver`.

    Returns :class:`matplotlib.image.AxesImage`.
    """
    return _plot_array(_QUIVER, U, V, ax=ax, add_cbar=False, rescale_fig=rescale_fig, **kwargs)


def _plot_array(type, *args, ax=None, add_cbar=True, rescale_fig=True, **kwargs):
    # ======================================
    # Get an ax
    # ======================================
    if ax is None:
        if rescale_fig:
            figsize = scaled_figsize(args[0])
        fig, ax = _setup_axes(figsize=figsize)

    if type == _IMSHOW:
        im = ax.imshow(_np.transpose(*args), origin='lower', **kwargs)
    elif type == _CONTOUR:
        im = ax.contour(_np.transpose(*args), origin='lower', **kwargs)
    elif type == _QUIVER:
        im = ax.quiver(args[1], args[0], **kwargs)

    if add_cbar:
        _cb(ax, im)

    if ax is None:
        return fig, ax, im
    else:
        return im


def scaled_figsize(X, figsize=None):
    """
    .. versionadded:: 1.3

    Given an array *X*, determine a good size for the figure to be by shrinking it to fit within *figsize*. If not specified, shrinks to fit the figsize specified by the current :attr:`matplotlib.rcParams`.
    """
    if figsize is None:
        figsize = _mpl.rcParams['figure.figsize']

    # ======================================
    # Find the height and width
    # ======================================
    width, height = _np.shape(X)
    
    ratio = width / height
    
    # ======================================
    # Find how to rescale the figure
    # ======================================
    if ratio > figsize[0]/figsize[1]:
        figsize[1] = figsize[0] / ratio
    else:
        figsize[0] = figsize[1] * ratio
    
    return figsize
