# -*- coding: utf-8 -*-


from .thing import Vec
from .canvas import Platno
from .picture import Obrazok
from .exceptions import NepodporovanePriradenie


class ObrazkovaVec(Vec):

    def _init_graphics(self):
        self.obrazok = Obrazok(20, 20)

    @property
    def sirka(self):
        return self._width

    @sirka.setter
    def sirka(self, hodnota):
        raise NepodporovanePriradenie()

    @property
    def vyska(self):
        return self._height

    @vyska.setter
    def vyska(self, hodnota):
        raise NepodporovanePriradenie()

    @property
    def obrazok(self):
        return self._picture

    @obrazok.setter
    def obrazok(self, obrazok):
        self._picture = obrazok
        self._canvas = Platno(self._picture)
        self._width = obrazok.sirka
        self._height = obrazok.vyska

    @property
    def platno(self):
        return self._canvas

    def _repaint(self, canvas):
        canvas.obrazok(
            self._picture,
            (self.okraj_vlavo, self.okraj_hore),
        )

    def vykresli(self, platno):
        pass
