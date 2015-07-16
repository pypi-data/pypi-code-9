import numpy as _np


def rgb2gray(image):
    return _np.dot(image, [0.2126, 0.7152, 0.0722])
