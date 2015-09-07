#  -*- coding: utf-8 -*-


from .constants import CONSTANTS
import pygame
import pygame.gfxdraw


def norm(x):
    return int(round(x))


class Canvas:

    def __init__(self, picture, color=None):
        self.color = color or CONSTANTS['BLACK']
        self._surface = picture._surface

    def line(self, p1, p2):
        (x1, y1) = p1
        (x2, y2) = p2
        pygame.gfxdraw.line(
            self._surface, norm(x1), norm(y1), norm(x2), norm(y2),
            self.color,
        )

    def pixel(self, p):
        (x, y) = p
        pygame.gfxdraw.pixel(
            self._surface, norm(x), norm(y), self.color,
        )

    def rectangle(
        self, p, width, height, filled=False
    ):
        (x, y) = p
        params = (
            self._surface,
            (norm(x), norm(y), norm(width), norm(height)),
            self.color,
        )
        if filled:
            pygame.gfxdraw.box(*params)
        else:
            pygame.gfxdraw.rectangle(*params)

    def ellipse(self, p, rx, ry, filled=False):
        (x, y) = p
        params = (
            self._surface,
            norm(x), norm(y), norm(rx), norm(ry),
            self.color,
        )
        if filled:
            pygame.gfxdraw.filled_ellipse(*params)
        else:
            pygame.gfxdraw.ellipse(*params)

    def polygon(self, points, filled=False):
        params = (
            self._surface,
            list(map(lambda p: (norm(p[0]), norm(p[1])), points)),
            self.color,
        )
        if filled:
            pygame.gfxdraw.filled_polygon(*params)
        else:
            pygame.gfxdraw.polygon(*params)

    def picture(self, picture, p):
        (x, y) = p
        self._surface.blit(picture._surface, (norm(x), norm(y)))
