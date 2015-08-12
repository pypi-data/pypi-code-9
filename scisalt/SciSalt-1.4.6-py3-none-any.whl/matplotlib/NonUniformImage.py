import os as _os
on_rtd = _os.environ.get('READTHEDOCS', None) == 'True'
if not on_rtd:
    import matplotlib.image as _mplim
    import numpy as _np
# import ipdb

from .setup_axes import setup_axes as _setup_axes


def NonUniformImage(x, y, z, ax=None, cmap=None, alpha=None, scalex=True, scaley=True, **kwargs):
    """
    Plots a set of coordinates where:

    * *x* and *y* are 1-D ndarrays of lengths N and M, respectively, specifying pixel centers
    * *z* is an (M, N) ndarray or masked array of values to be colormapped, or a (M, N, 3) RGB array, or a (M, N, 4) RGBA array.

    *\*\*kwargs* can contain keywords:
    
    * *cmap* for set the colormap
    * *alpha* to set transparency
    * *scalex* to set the x limits to available data
    * *scaley* to set the y limits to available data

    Returns class :class:`matplotlib.image.NonUniformImage`.
    """
    if ax is None:
        fig, ax = _setup_axes()

    im = _mplim.NonUniformImage(ax, **kwargs)

    vmin = kwargs.pop('vmin', _np.min(z))
    vmax = kwargs.pop('vmax', _np.max(z))
    im.set_clim(vmin=vmin, vmax=vmax)

    if cmap is not None:
        im.set_cmap(cmap)

    if alpha is not None:
        im.set_alpha(alpha)

    im.set_data(x, y, z)
    ax.images.append(im)

    if scalex:
        xmin = min(x)
        xmax = max(x)
        ax.set_xlim(xmin, xmax)

    if scaley:
        ymin = min(y)
        ymax = max(y)
        ax.set_ylim(ymin, ymax)

    return im
