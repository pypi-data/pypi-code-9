#  -*- coding: utf-8 -*-


from .constants import CONSTANTS
import pygame
import pygame.gfxdraw


def norm(x):
    return int(round(x))


class Platno:

    def __init__(self, obrazok, farba=None):
        self.farba = farba or CONSTANTS['CIERNA']
        self._surface = obrazok._surface

    def ciara(self, p1, p2):
        (x1, y1) = p1
        (x2, y2) = p2
        pygame.gfxdraw.line(
            self._surface, norm(x1), norm(y1), norm(x2), norm(y2),
            self.farba,
        )

    def pixel(self, p):
        (x, y) = p
        pygame.gfxdraw.pixel(
            self._surface, norm(x), norm(y), self.farba,
        )

    def obdlzdnik(
        self, p, sirka, vyska, vyfarbenie=False
    ):
        (x, y) = p
        params = (
            self._surface,
            (norm(x), norm(y), norm(sirka), norm(vyska)),
            self.farba,
        )
        if vyfarbenie:
            pygame.gfxdraw.box(*params)
        else:
            pygame.gfxdraw.rectangle(*params)

    def elipsa(self, p, rx, ry, vyfarbenie=False):
        (x, y) = p
        params = (
            self._surface,
            norm(x), norm(y), norm(rx), norm(ry),
            self.farba,
        )
        if vyfarbenie:
            pygame.gfxdraw.filled_ellipse(*params)
        else:
            pygame.gfxdraw.ellipse(*params)

    def mnohouholnik(self, body, vyfarbenie=False):
        params = (
            self._surface,
            list(map(lambda p: (norm(p[0]), norm(p[1])), body)),
            self.farba,
        )
        if vyfarbenie:
            pygame.gfxdraw.filled_polygon(*params)
        else:
            pygame.gfxdraw.polygon(*params)

    def obrazok(self, obrazok, p):
        (x, y) = p
        self._surface.blit(obrazok._surface, (norm(x), norm(y)))
