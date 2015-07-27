
"""
mbox_globals
==========================================

Module that has mbox API globals.
"""


# Import
# ------------------------------------------------------------------
# import
import os
import logging


# Pathes
# ------------------------------------------------------------------
TOOL_ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))

# Version and Title
# ------------------------------------------------------------------
TITLE = 'mbox'
VERSION = '0.0.1'
DIVIDER = '--------------------'


# Logging
# ------------------------------------------------------------------
LOGGING_LEVEL = logging.DEBUG
