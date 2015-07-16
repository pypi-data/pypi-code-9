import os as _os
on_rtd = _os.environ.get('READTHEDOCS', None) == 'True'
if not on_rtd:
    import matplotlib.image as _mplim
    import numpy as _np
# import ipdb


def NonUniformImage(x, y, z, **kwargs):
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
    ax = kwargs.pop('ax')
    im = _mplim.NonUniformImage(ax)

    vmin = kwargs.pop('vmin', _np.min(z))
    vmax = kwargs.pop('vmax', _np.max(z))
    im.set_clim(vmin=vmin, vmax=vmax)

    try:
        cmap = kwargs.pop('cmap')
        im.set_cmap(cmap)
    except KeyError:
        pass

    try:
        alpha = kwargs.pop('alpha')
        im.set_alpha(alpha)
    except KeyError:
        pass

    im.set_data(x, y, z)
    ax.images.append(im)

    scalex = kwargs.pop('scalex', True)
    if scalex:
        xmin = min(x)
        xmax = max(x)
        ax.set_xlim(xmin, xmax)

    scaley = kwargs.pop('scaley', True)
    if scaley:
        ymin = min(y)
        ymax = max(y)
        ax.set_ylim(ymin, ymax)

    return im
