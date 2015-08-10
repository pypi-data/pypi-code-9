import matplotlib.image as _mplim
import numpy as _np
# import ipdb


def NonUniformImage(x, y, z, **kwargs):
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
