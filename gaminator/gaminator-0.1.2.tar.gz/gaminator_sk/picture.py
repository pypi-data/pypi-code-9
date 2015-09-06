#  -*- coding: utf-8 -*-


from . import color
from .constants import CONSTANTS
import pygame
import os


class Obrazok:

    def __init__(self, sirka, vyska, je_priesvitny=False):

        self._width = 0
        self._height = 0
        self._has_alpha = False

        if isinstance(sirka, pygame.Surface) and vyska is None:
            self._set_surface(sirka)
        else:
            self.zresetuj(sirka, vyska, je_priesvitny)

    def zresetuj(
        self, sirka=None, vyska=None, je_priesvitny=None
    ):
        if sirka is not None:
            self._width = sirka
        if vyska is not None:
            self._height = vyska
        if je_priesvitny is not None:
            self._has_alpha = je_priesvitny

        dims = (self._width, self._height)

        flags = 0
        if self._has_alpha:
            self._surface = pygame.Surface(dims, pygame.SRCALPHA, 32)
            self._surface.convert_alpha()
        else:
            self._surface = pygame.Surface(dims)
            self._surface.set_colorkey((0, 1, 0))

        self.zmaz()

    def zmaz(self):
        self._surface.fill((0, 1, 0, 0))

    @property
    def sirka(self):
        return self._width

    @property
    def vyska(self):
        return self._height

    @property
    def je_priesvitny(self):
        return self._has_alpha

    def _set_surface(self, surface):
        self._surface = surface
        self._width = surface.get_width()
        self._height = surface.get_height()


def obrazok_zo_suboru(*path):
    surface = pygame.image.load(os.path.join(*path))
    return Picture(surface, None)


def obrazok_z_textu(
    text="", velkost=10, farba=CONSTANTS["CIERNA"],
    hrube=False, sikme=False,
):
    font = pygame.font.SysFont(
        None, velkost, bold=hrube, italic=sikme,
    )
    surface = font.render(text, False, farba)
    return Picture(surface, None)
