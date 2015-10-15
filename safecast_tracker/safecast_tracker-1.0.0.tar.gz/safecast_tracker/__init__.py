#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Safecast Tracker.

"""
Safecast Tracker.
~~~~


:author: Greg Albrecht W2GMD <gba@orionlabs.co>
:copyright: Copyright 2015 Orion Labs, Inc.
:license: Apache License, Version 2.0
:source: <https://github.com/ampledata/safecast_tracker>

"""

import logging

from .classes import BGeigieNanoPoller


# Set default logging handler to avoid "No handler found" warnings.
try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        """Default logging handler to avoid "No handler found" warnings."""
        def emit(self, record):
            """Default logging handler to avoid "No handler found" warnings."""
            pass

logging.getLogger(__name__).addHandler(NullHandler())
