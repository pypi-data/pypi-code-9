#!/usr/bin/env python

'''Logistic functions applied to image arrays'''


from functools import partial
from numpy import exp as _exp

from . import image


def _logistic(k, array):
    return 1.0 / (1.0 + _exp(-k * array))


def logistic(k, img):
    '''Apply the logistic function of degree k to an image array.'''
    return image.map_to_channels(
        partial(_logistic, k),
        lambda shape: shape,
        img,
    )


if __name__ == '__main__':
    pass
