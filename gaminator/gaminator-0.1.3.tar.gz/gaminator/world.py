# -*- coding: utf-8 -*-


from collections import defaultdict
from operator import attrgetter
import pygame
import time

from .thing import Thing
from .picture import Picture
from .canvas import Canvas
from .window import window
from .events import _EventEmitterMixim
from .collisions import _CollisionEmitterMixim
from .exceptions import TopWorldSubworlding
from .exceptions import SelfSubworlding


class World(Thing, _EventEmitterMixim, _CollisionEmitterMixim):

    def __init__(self, **kwargs):
        self._start_time = time.time()
        self._time = 0
        self._ticks = 0

        self._things_by_class = defaultdict(set)
        self._things = set()

        self._things_by_z = None
        self._recalculate_z = True

        _EventEmitterMixim.__init__(self)
        Thing.__init__(self, **kwargs)

        self.x_align = 0
        self.y_align = 0

    def _init_graphics(self):
        self._width = window.width
        self._height = window.height
        self.background = Picture(self.width, self.height)

    @property
    def width(self):
        if self._world == self:
            # @HACK: Top worlds are kids of themselves
            return window.width
        return self._width

    @width.setter
    def width(self, value):
        if self._world == self:
            # @HACK: Top worlds are kids of themselves
            window.width = value
        else:
            self._width = value

    @property
    def height(self):
        if self._world == self:
            # @HACK: Top worlds are kids of themselves
            return window.height
        return self._height

    @height.setter
    def height(self, value):
        if self._world == self:
            # @HACK: Top worlds are kids of themselves
            window.height = value
        else:
            self._height = value

    @property
    def background(self):
        return self._picture

    @background.setter
    def background(self, picture):
        self._picture = picture
        self._canvas = Canvas(self._picture)

    @property
    def canvas(self):
        return self._canvas

    @property
    def ticks(self):
        return self._ticks

    @property
    def time(self):
        return self._time

    @property
    def things(self):
        return list(self._things)

    @property
    def subworlds(self):
        return list(self._things_by_class[World])

    def _repaint(self, canvas):
        my_picture = Picture(self.width, self.height)
        my_canvas = Canvas(my_picture)

        my_canvas.picture(
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

        canvas.picture(
            my_picture,
            (self.border_left, self.border_up),
        )

    def _connect_thing(self, thing):
        if thing == self:
            # @HACK: Top worlds are kids of themselves
            raise SelfSubworlding()
        self._recalculate_z = True
        self._things.add(thing)
        for cls in thing.__class__.__mro__:
            self._things_by_class[cls].add(thing)

    def _disconnect_thing(self, thing):
        if thing == self:
            # @HACK: Top worlds are kids of themselves
            raise TopWorldSubworlding()
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

        for subworld in self._things_by_class[World]:
            subworld._tick()
