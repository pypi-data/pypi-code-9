

"""
mbox
==========================================

Module to read and format mbox file input.

.. code::

    python mbox.py file_to_read.mbox

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
import argparse


# logging basic configuration
logging.basicConfig()


# Import variable
do_reload = True


# mbox_globals
from lib import mbox_globals as mbox_globals
if(do_reload):
    reload(mbox_globals)


# mbox_object
from lib import mbox_object as mbox_object
if(do_reload):
    reload(mbox_object)


# Globals
# ------------------------------------------------------------------
TITLE = mbox_globals.TITLE
VERSION = mbox_globals.VERSION
LOGGING_LEVEL = mbox_globals.LOGGING_LEVEL
DIVIDER = mbox_globals.DIVIDER


# Logger
# ------------------------------------------------------------------
# logger
logger = logging.getLogger(__name__)
logger.setLevel(LOGGING_LEVEL)


# Command Line Arguments
# ------------------------------------------------------------------
# parser
parser = argparse.ArgumentParser(prog='{0} {1}'.format(TITLE, VERSION), description='Command line arguments for mbox')
parser.add_argument('mbox', nargs='+', type=str, help='mbox file to process')


# Functions
# ------------------------------------------------------------------
def path_valid(file_path):
    """
    Return True or False based on wether or not
    file_path exists in the filesystem.
    """

    # check
    return True if os.path.isfile(file_path) else False


# Run
# ------------------------------------------------------------------
def run():
    """
    Main function to run and process mbox files.
    """

    # args
    args = parser.parse_args()

    # mbox_file_path
    mbox_file_path = args.mbox[0]

    # check if mbox_file_path valid
    if not(path_valid(mbox_file_path)):
        # log
        logger.debug('Path {0} not valid. Please enter valid path to mbox file'.format(mbox_file_path))
        return

    # mbox_object_instance
    mbox_object_instance = mbox_object.MboxObject(mbox_file_path)

    # print_domains_stats
    mbox_object_instance.print_domains_stats()


# Run
# ------------------------------------------------------------------
if(__name__ == '__main__'):

    # run
    run()
