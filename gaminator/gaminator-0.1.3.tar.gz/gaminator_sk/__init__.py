# -*- coding: utf-8 -*-

from .constants import CONSTANTS

from .game import hra
from .thing import Vec
from .world import Svet

from .events import udalost
from .collisions import zrazka

from .color import Farba
from .picture import Obrazok, obrazok_zo_suboru, obrazok_z_textu
from .canvas import Platno
from .picture_thing import ObrazkovaVec

from .window import okno


import pygame as _pygame
for name in dir(_pygame):
    if name.startswith("K_"):
        CONSTANTS[name] = getattr(_pygame, name)

import sys as _sys
_module = _sys.modules[__name__]
for key, value in CONSTANTS.items():
    setattr(_module, key, value)

_pygame.font.init()
