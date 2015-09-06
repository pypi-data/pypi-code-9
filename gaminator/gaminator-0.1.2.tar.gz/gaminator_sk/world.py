# -*- coding: utf-8 -*-


from collections import defaultdict
from operator import attrgetter
import pygame
import time

from .thing import Vec
from .picture import Obrazok
from .canvas import Platno
from .window import okno
from .events import _EventEmitterMixim
from .collisions import _CollisionEmitterMixim
from .exceptions import NemoznoVnoritSvet
from .exceptions import CyklickeVnorenieSveta


class Svet(Vec, _EventEmitterMixim, _CollisionEmitterMixim):

    def __init__(self, **kwargs):
        self._start_time = time.time()
        self._time = 0
        self._ticks = 0

        self._things_by_class = defaultdict(set)
        self._things = set()

        self._things_by_z = None
        self._recalculate_z = True

        _EventEmitterMixim.__init__(self)
        Vec.__init__(self, **kwargs)

        self.x_zarovnanie = 0
        self.y_zarovnanie = 0

    def _init_graphics(self):
        self._width = okno.sirka
        self._height = okno.vyska
        self.pozadie = Obrazok(self.sirka, self.vyska)

    @property
    def sirka(self):
        if self._world == self:
            # @HACK: Top worlds are kids of themselves
            return okno.sirka
        return self._width

    @sirka.setter
    def sirka(self, hodnota):
        if self._world == self:
            # @HACK: Top worlds are kids of themselves
            okno.sirka = hodnota
        else:
            self._width = hodnota

    @property
    def vyska(self):
        if self._world == self:
            # @HACK: Top worlds are kids of themselves
            return okno.vyska
        return self._height

    @vyska.setter
    def vyska(self, hodnota):
        if self._world == self:
            # @HACK: Top worlds are kids of themselves
            okno.vyska = hodnota
        else:
            self._height = hodnota

    @property
    def pozadie(self):
        return self._picture

    @pozadie.setter
    def pozadie(self, obrazok):
        self._picture = obrazok
        self._canvas = Platno(self._picture)

    @property
    def platno(self):
        return self._canvas

    @property
    def kroky(self):
        return self._ticks

    @property
    def cas(self):
        return self._time

    @property
    def veci(self):
        return list(self._things)

    @property
    def podsvety(self):
        return list(self._things_by_class[Svet])

    def _repaint(self, canvas):
        my_picture = Obrazok(self.sirka, self.vyska)
        my_canvas = Platno(my_picture)

        my_canvas.obrazok(
            self._picture,
            (0, 0),
        )

        if self._recalculate_z:
            self._things_by_z = list(
                sorted(self._things, key=lambda x: (x._z, x.id))
            )
            self._recalculate_z = False
        for thing in self._things_by_z:
            thing._repaint(my_canvas)

        canvas.obrazok(
            my_picture,
            (self.okraj_vlavo, self.okraj_hore),
        )

    def _connect_thing(self, thing):
        if thing == self:
            # @HACK: Top worlds are kids of themselves
            raise CyklickeVnorenieSveta()
        self._recalculate_z = True
        self._things.add(thing)
        for cls in thing.__class__.__mro__:
            self._things_by_class[cls].add(thing)

    def _disconnect_thing(self, thing):
        if thing == self:
            # @HACK: Top worlds are kids of themselves
            raise NemoznoVnoritSvet()
        self._recalculate_z = True
        self._things.remove(thing)
        for cls in thing.__class__.__mro__:
            self._things_by_class[cls].remove(thing)

    def _clear_things(self, thing):
        self._recalculate_z = True
        for thing in self._things:
            thing._world = None
        self._things.clear()
        for cls in self._things_by_class:
            self._things_by_class[cls].clear()

    def _activate(self):
        self._start_time = time.time() - self._time

    def _deactivate(self):
        self._time = time.time() - self._start_time

    def _tick(self):
        self._ticks += 1
        self._time = time.time() - self._start_time

        self._tick_collisions()
        self._tick_events()

        for subworld in self._things_by_class[Svet]:
            subworld._tick()
