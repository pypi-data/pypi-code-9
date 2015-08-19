#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from collections import namedtuple


# Functions & classes =========================================================
class ConversionResponse(namedtuple("ConversionResponse", ["mods_files"])):
    """
    Converted MODS files.

    Attributes:
        mods (list): List of converted MODS files.
    """
