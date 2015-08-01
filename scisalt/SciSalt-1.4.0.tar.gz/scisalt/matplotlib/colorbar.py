import os as _os
_on_rtd = _os.environ.get('READTHEDOCS', None) == 'True'
if not _on_rtd:
    from mpl_toolkits import axes_grid1 as _ag1
    import matplotlib.pyplot as _plt


def colorbar(ax, im):
    """
    .. versionadded:: 1.3

    Adds a polite colorbar that steals space so :meth:`matplotlib.pyplot.tight_layout` works nicely.
    """
    divider = _ag1.make_axes_locatable(ax)
    cax = divider.append_axes("right", "5%", pad="3%")
    return _plt.colorbar(im, cax=cax)
