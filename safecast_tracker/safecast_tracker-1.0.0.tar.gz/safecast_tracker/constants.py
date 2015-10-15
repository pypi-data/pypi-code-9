#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Constants for Safecast Tracker.
"""

__author__ = 'Greg Albrecht W2GMD <gba@orionlabs.co>'
__license__ = 'Apache License, Version 2.0'
__copyright__ = 'Copyright 2015 Orion Labs, Inc.'


import logging


LOG_LEVEL = logging.INFO
LOG_FORMAT = logging.Formatter(
    ('%(asctime)s %(levelname)s %(name)s.%(funcName)s:%(lineno)d '
     '- safecast_tracker - %(message)s'))

GPS_WARM_UP = 5
