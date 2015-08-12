import os as _os
on_rtd = _os.environ.get('READTHEDOCS', None) == 'True'
if not on_rtd:
    import numpy as _np


def rgb2gray(image):
    """
    Convert an rgb image to grayscale.
    """
    return _np.dot(image, [0.2126, 0.7152, 0.0722])
