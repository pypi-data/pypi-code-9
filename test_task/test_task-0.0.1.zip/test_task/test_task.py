

"""
test_task
==========================================

Module for application purposes.

.. code::

    Show how to start here

-----------------------
Current Status: alpha
-----------------------

**Author:** `Timm Wagener <mailto:wagenertimm@gmail.com>`_
"""


# Import
# ------------------------------------------------------------------
# python
import sys
import os
import functools
import logging


# logging basic configuration
logging.basicConfig()


# Import variable
do_reload = True


# test_task_globals
from lib import test_task_globals as test_task_globals
if(do_reload):
    reload(test_task_globals)


# Globals
# ------------------------------------------------------------------
TITLE = test_task_globals.TITLE
VERSION = test_task_globals.VERSION
INITIAL_LOGGING_LEVEL = test_task_globals.INITIAL_LOGGING_LEVEL
TOOL_ROOT_PATH = test_task_globals.TOOL_ROOT_PATH
DIVIDER = test_task_globals.DIVIDER


# TestTask class
# ------------------------------------------------------------------
class TestTask(object):
    """
    TestTask class.
    """

    # Create and initialize
    # ------------------------------------------------------------------
    def __new__(cls, *args, **kwargs):
        """
        TestTask instance factory.
        """

        # test_task_instance
        test_task_instance = super(TestTask, cls).__new__(cls, args, kwargs)

        return test_task_instance

    def __init__(self, logging_level=INITIAL_LOGGING_LEVEL):
        """
        Customize instance.
        """

        # instance variables
        # ------------------------------------------------------------------
        # logger
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.setLevel(logging_level)

    # Methods
    # ------------------------------------------------------------------
    def test_method(self, msg):
        """
        Return self.path.
        """

        self.logger.debug('{0}'.format(msg))

# Run
# ------------------------------------------------------------------
if(__name__ == '__main__'):

    # test_task_instance
    test_task_instance = TestTask()

    # test_method
    msg = 'Success starting {0} {1}'.format(TITLE, VERSION)
    test_task_instance.test_method(msg)
