import numpy as _np


def NonUniformImage_axes(img):
    xmin = 0
    xmax = img.shape[1]-1
    ymin = 0
    ymax = img.shape[0]-1
    x = _np.linspace(xmin, xmax, img.shape[1])
    y = _np.linspace(ymin, ymax, img.shape[0])
    return x, y
