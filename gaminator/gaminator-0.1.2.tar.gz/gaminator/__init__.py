# -*- coding: utf-8 -*-

from .constants import CONSTANTS

from .game import game
from .thing import Thing
from .world import World

from .events import event
from .collisions import collision

from .color import Color
from .picture import Picture, open_picture, text_to_picture
from .canvas import Canvas
from .picture_thing import PictureThing

from .window import window


import pygame as _pygame
for name in dir(_pygame):
    if name.startswith("K_"):
        CONSTANTS[name] = getattr(_pygame, name)

import sys as _sys
_module = _sys.modules[__name__]
for key, value in CONSTANTS.items():
    setattr(_module, key, value)

_pygame.font.init()
