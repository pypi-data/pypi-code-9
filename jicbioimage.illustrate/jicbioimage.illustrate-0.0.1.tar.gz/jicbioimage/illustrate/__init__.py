"""Module for creating illustrations.

To create an annotated image we need an instance of the
:class:`jicbioimage.illustrate.AnnotatedImage` class.

>>> from jicbioimage.illustrate import AnnotatedImage

Suppose that we have an existing image.

>>> from jicbioimage.core.image import Image
>>> im = Image((50,50))

We can use this image to create an canvas instance populated with the data
as a RGB gray scale image.

>>> canvas = AnnotatedImage.from_grayscale(im)

The :class:`jicbioimage.illustrate.Canvas` instance has built in annotation
functionality. We can draw a cross at coordinates (10, 20).

>>> canvas.draw_cross(10, 20)

Or mask out a bitmap with the color cyan.

>>> bitmap = np.zeros((50, 50), dtype=bool)
>>> bitmap[30:40, 30:40] = True
>>> canvas.mask_region(bitmap, color=(0, 255, 255))

"""

import os.path

import PIL.ImageFont
import numpy as np

__version__ = "0.0.1"

HERE = os.path.dirname(__file__)
DEFAULT_FONT_PATH = os.path.join(HERE, "fonts", "UbuntuMono-R.ttf")


class Canvas(np.ndarray):
    """Class for building up annotated images."""

    @staticmethod
    def blank_canvas(width, height):
        """Return a blank canvas to annotate.

        :param x: xdim
        :param y: ydim
        :returns: :class:`jicbioimage.illustrate.Canvas`
        """
        canvas = np.zeros((height, width, 3), dtype=np.uint8)
        return canvas.view(Canvas)

    def draw_cross(self, x, y, color=(255, 0, 0), radius=4):
        """Draw a cross on the canvas.

        :param x: x coordinate (int)
        :param y: y coordinate (int)
        :param color: RGB tuple
        :param radius: radius of the cross (int)
        """
        for xmod in np.arange(-radius, radius+1, 1):
            xpos = x + xmod
            if xpos < 0:
                continue  # Negative indices will draw on the opposite side.
            if xpos >= self.shape[0]:
                continue  # Out of bounds.
            self[y, xpos] = color
        for ymod in np.arange(-radius, radius+1, 1):
            ypos = y + ymod
            if ypos < 0:
                continue  # Negative indices will draw on the opposite side.
            if ypos >= self.shape[1]:
                continue  # Out of bounds.
            self[ypos, x] = color

    def mask_region(self, region, color=(0, 255, 0)):
        """Mask a region with a color.

        :param region: :class:`jicbioimage.core.region.Region`
        :param color: RGB tuple
        """
        self[region] = color

    def text_at(self, text, x, y, color=(255, 255, 255),
                size=12, antialias=True):
        """Write text at x, y top left corner position.

        :param text: text to write
        :param x: x coordinate (int)
        :param y: y coordinate (int)
        :param color: RGB tuple
        """
        def antialias_value(value, normalisation):
            return int(round(value * normalisation))

        def antialias_rgb(color, normalisation):
            return tuple([antialias_value(v, normalisation) for v in color])

        font = PIL.ImageFont.truetype(DEFAULT_FONT_PATH, size=size)
        mask = font.getmask(text)
        width, height = mask.size
        for ystep in range(height):
            for xstep in range(width):
                normalisation = mask[ystep * width + xstep] / 255.
                if antialias:
                    if normalisation != 0:
                        rgb_color = antialias_rgb(color, normalisation)
                        self[y + ystep, x + xstep] = rgb_color
                else:
                    if normalisation > .5:
                        self[y + ystep, x + xstep] = color


class AnnotatedImage(Canvas):
    """Class for building up annotated images."""

    @staticmethod
    def from_grayscale(im, channels_on=(True, True, True)):
        """Return a canvas from a grayscale image.

        :param im: single channel image
        :channels_on: channels to populate with input image
        :returns: :class:`jicbioimage.illustrate.Canvas`
        """
        xdim, ydim = im.shape
        canvas = np.zeros((xdim, ydim, 3), dtype=np.uint8)
        for i, include in enumerate(channels_on):
            if include:
                canvas[:, :, i] = im
        return canvas.view(AnnotatedImage)
