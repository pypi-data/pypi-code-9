#!/usr/bin/env python

'''Vertical or horizontal flipping of image arrays'''


from . import image


def _flip_vertical(array):
    return array[::-1, :]


def flip_vertical(img):
    '''Flip an image array vertically.'''
    return image.map_to_channels(
        _flip_vertical,
        lambda shape: shape,
        img,
    )


def _flip_horizontal(array):
    return array[:, ::-1]


def flip_horizontal(img):
    '''Flip an image array horizontally.'''
    return image.map_to_channels(
        _flip_horizontal,
        lambda shape: shape,
        img,
    )


if __name__ == '__main__':
    pass
