import os as _os
_on_rtd = _os.environ.get('READTHEDOCS', None) == 'True'
if not _on_rtd:
    from mpl_toolkits import axes_grid1 as _ag1
    import matplotlib.pyplot as _plt

import logging as _logging
_logger = _logging.getLogger(__name__)

import pdb as _pdb


def colorbar(ax, im, loc="right", size="5%", pad="3%"):
    """
    .. versionadded:: 1.3

    Adds a polite colorbar that steals space so :meth:`matplotlib.pyplot.tight_layout` works nicely.
    """
    fig = ax.get_figure()

    # _pdb.set_trace()
    if loc == "left" or loc == "right":
        width = fig.get_figwidth()
        new = width * (1 + _pc2f(size) + _pc2f(pad))
        _logger.debug('Setting new figure width: {}'.format(new))
        fig.set_size_inches(new, fig.get_figheight(), forward=True)
    elif loc == "top" or loc == "bottom":
        height = fig.get_figheight()
        new = height * (1 + _pc2f(size) + _pc2f(pad))
        _logger.debug('Setting new figure height: {}'.format(new))
        fig.set_figheight(fig.get_figwidth(), new, forward=True)

    divider = _ag1.make_axes_locatable(ax)
    cax = divider.append_axes(loc, size=size, pad=pad)
    return _plt.colorbar(im, cax=cax)


def _pc2f(str):
    return float(str.strip('%'))/100
