#  -*- coding: utf-8 -*-


import pygame


class _WindowSettings(object):

    def __init__(self):
        self._flags = 0
        self._width = 600
        self._height = 400
        self._changed_mode = True
        self._caption = "Gaminator"
        self._changed_caption = True
        self.fps = 60

    def _set_flag(self, flag):
        self._flags = self._flags | flag

    def _reset_flag(self, flag):
        self._flags = (self._flags | flag) - flag

    def _apply_changes(self):
        if self._changed_mode:
            self._changed_mode = False
            pygame.display.set_mode((self._width, self._height), self._flags)
        if self._changed_caption:
            self._changed_caption = False
            pygame.display.set_caption(self._caption)

    @property
    def sirka(self):
        return self._width

    @sirka.setter
    def sirka(self, _width):
        self._changed_mode = True
        self._width = _width

    @property
    def vyska(self):
        return self._height

    @vyska.setter
    def vyska(self, _height):
        self._changed_mode = True
        self._height = _height

    @property
    def nadpis(self):
        return self._caption

    @nadpis.setter
    def nadpis(self, _nazov):
        self._changed_caption = True
        self._caption = _nazov

    def cela_obrazovka(self):
        self._changed_mode = True
        self._flags = (
            pygame.FULLSCREEN | pygame.DOUBLEBUF |
            pygame.HWSURFACE | pygame.NOFRAME
        )

    def pevne(self):
        self._changed_mode = True
        self._flags = 0

    def nastavitelne(self):
        self._changed_mode = True
        self._flags = pygame.RESIZABLE


okno = _WindowSettings()
