# -*- coding: utf-8 -*-

import enum

version = '0.0.1'


class Modes(enum.Enum):
    SHARED = 'SHARED'
    STATIC = 'STATIC'
    ANY = 'ANY'
    PREFER_SHARED = 'PREFER_SHARED'
    PREFER_STATIC = 'PREFER_STATIC'


SHARED = Modes.SHARED
STATIC = Modes.STATIC
ANY = Modes.ANY
PREFER_SHARED = Modes.PREFER_SHARED
PREFER_STATIC = Modes.PREFER_STATIC
