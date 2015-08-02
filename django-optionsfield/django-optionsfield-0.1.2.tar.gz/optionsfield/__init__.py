#!/usr/bin/env python
# -*- coding: utf-8 -*-

u"""
django-optionsfield
"""

__author__ = u"Rafał Selewońko <rafal@selewonko.com>"

# version info is stored in separate module so its possible to import it from
# setup.py without importing whole app
from ._version import __version__, __version_info__  # flake8: noqa

from .fields import OptionsField  # flake8: noqa
