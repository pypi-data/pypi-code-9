
"""
test_task_globals
==========================================

Module that has test_task API globals.
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
TITLE = 'Test Task'
VERSION = 0.1
DIVIDER = '--------------------'


# Logging
# ------------------------------------------------------------------
INITIAL_LOGGING_LEVEL = logging.DEBUG
