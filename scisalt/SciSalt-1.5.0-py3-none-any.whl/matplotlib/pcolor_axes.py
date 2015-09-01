import os as _os
on_rtd = _os.environ.get('READTHEDOCS', None) == 'True'
if not on_rtd:
    import numpy as _np


def px_to_units(xpx, ypx):
    return xpx, ypx


def pcolor_axes(array, px_to_units=px_to_units):
    """
    Return axes :code:`x, y` for *array* to be used with :func:`matplotlib.pyplot.color`.

    *px_to_units* is a function to convert pixels to units. By default, returns pixels.
    """
    # ======================================
    # Coords need to be +1 larger than array
    # ======================================
    x_size = array.shape[0]+1
    y_size = array.shape[1]+1

    x = _np.empty((x_size, y_size))
    y = _np.empty((x_size, y_size))

    for i in range(x_size):
        for j in range(y_size):
            x[i, j], y[i, j] = px_to_units(i-0.5, j-0.5)

    return x, y
