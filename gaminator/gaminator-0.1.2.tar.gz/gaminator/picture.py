#  -*- coding: utf-8 -*-


from . import color
from .constants import CONSTANTS
import pygame
import os


class Picture:

    def __init__(self, width, height, has_alpha=False):

        self._width = 0
        self._height = 0
        self._has_alpha = False

        if isinstance(width, pygame.Surface) and height is None:
            self._set_surface(width)
        else:
            self.reset(width, height, has_alpha)

    def reset(
        self, width=None, height=None, has_alpha=None
    ):
        if width is not None:
            self._width = width
        if height is not None:
            self._height = height
        if has_alpha is not None:
            self._has_alpha = has_alpha

        dims = (self._width, self._height)

        flags = 0
        if self._has_alpha:
            self._surface = pygame.Surface(dims, pygame.SRCALPHA, 32)
            self._surface.convert_alpha()
        else:
            self._surface = pygame.Surface(dims)
            self._surface.set_colorkey((0, 1, 0))

        self.clear()

    def clear(self):
        self._surface.fill((0, 1, 0, 0))

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def has_alpha(self):
        return self._has_alpha

    def _set_surface(self, surface):
        self._surface = surface
        self._width = surface.get_width()
        self._height = surface.get_height()


def open_picture(*path):
    surface = pygame.image.load(os.path.join(*path))
    return Picture(surface, None)


def text_to_picture(
    text="", size=10, color=CONSTANTS["BLACK"],
    bold=False, italic=False,
):
    font = pygame.font.SysFont(
        None, size, bold=bold, italic=italic,
    )
    surface = font.render(text, False, color)
    return Picture(surface, None)
