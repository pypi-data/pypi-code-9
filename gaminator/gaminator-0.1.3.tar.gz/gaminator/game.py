#  -*- coding: utf-8 -*-


import pygame
from threading import Condition
import traceback

from .interactive import interact
from .picture import Picture
from .canvas import Canvas
from .window import window


class _Game:

    def __init__(self):
        self._end = False
        self._interactive = False
        self._lock = Condition()
        self._screen = None
        self._worlds = []
        self._world_changes = []
        self.tps = 60
        self.autoescape = True
        pass

    @property
    def world(self):
        return self._worlds[-1]

    def end(self):
        self._end = True

    def push_world(self, world):
        self._world_changes.append((1, world))

    def swap_world(self, world):
        self._world_changes.append((0, world))

    def pop_world(self):
        self._world_changes.append((-1, None))

    def start(self, world, interactive=False):
        self._interactive = interactive
        self.push_world(world)
        self._loop()

    def pressed(self, key):
        return self._pressed_keys[key]

    def _loop(self):

        if self._interactive:
            console = interact(self)

        pygame.init()

        window._apply_changes()
        self._screen = Picture(pygame.display.get_surface(), None)

        clock = pygame.time.Clock()

        try:
            with self._lock:
                while not self._end:

                    self._handle_world_changes()
                    if not self._worlds:
                        break

                    window._apply_changes()

                    if self._interactive:
                        self._lock.wait(0)

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.end()
                        elif event.type == pygame.VIDEORESIZE:
                            window._height = event.h
                            window._width = event.w
                        elif event.type == pygame.KEYDOWN:
                            if (
                                self.autoescape and
                                event.key == pygame.K_ESCAPE
                            ):
                                self.end()

                            self._worlds[-1].event(
                                ("KEYDOWN", event.key), event.unicode
                            )
                            self._worlds[-1].event(
                                "KEYDOWN", event.key, event.unicode
                            )
                        elif event.type == pygame.KEYUP:
                            self._worlds[-1].event(
                                ("KEYUP", event.key)
                            )
                            self._worlds[-1].event(
                                "KEYUP", event.key
                            )

                    self._pressed_keys = pygame.key.get_pressed()

                    self._worlds[-1]._tick()

                    self._screen._surface.fill((255, 255, 255, 0))
                    self._worlds[-1]._repaint(Canvas(self._screen))

                    pygame.display.flip()
                    clock.tick(self.tps)
        except:
            traceback.print_exc()
        finally:
            pygame.quit()

    def _handle_world_changes(self):
        for action, world in self._world_changes:
            if self._worlds:
                self._worlds[-1]._deactivate()
            if action in [-1, 0] and self._worlds:
                w = self._worlds.pop()
                w._world = None  # @HACK: Topworlds are kids of themselves
            if action in [0, 1]:
                self._worlds.append(world)
                world.world = None  # Disconect world from its parent
                world._world = world  # @HACK: Topworlds are kids of themselves
            if self._worlds:
                self._worlds[-1]._activate()
        self._world_changes = []


game = _Game()
