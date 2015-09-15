# -*- coding: utf-8 -*-
__author__ = 'Luke Plant'
__email__ = 'L.Plant.98@cantab.net'
__version__ = '0.1.0'

import contextlib
import os
import platform
import sys
import traceback
from enum import Enum

import easygui

# First, we need to work out if the script is running:

# 1. manually from a terminal
# 2. OR from something like crontab (where we have no possibility of interaction)
# 3. OR from being double-clicked from file manager


class RunningMode(Enum):
    terminal = 1
    gui = 2
    # non_interactive = 3  - might need to distinguish this in the future


def running_mode_unix():
    if os.isatty(sys.stdin.fileno()):
        return RunningMode.terminal
    else:
        return RunningMode.gui


def running_mode_windows():
    # Untested - see http://stackoverflow.com/questions/558776/detect-script-start-up-from-command-prompt-or-double-click-on-windows
    if 'PROMPT' in os.environ:
        return RunningMode.terminal
    else:
        return RunningMode.gui


PLATFORM = platform.system()

if PLATFORM.lower() == 'windows':
    running_mode = running_mode_windows
else:
    running_mode = running_mode_unix


@contextlib.contextmanager
def friendly_success(success_message=None):
    if running_mode() == RunningMode.gui:
        try:
            yield
        except:
            raise
        else:
            if success_message is None:
                success_message = "Script {0} completed successfully.".format(os.path.basename(sys.argv[0]))
            easygui.msgbox(success_message)
    else:
        yield


@contextlib.contextmanager
def friendly_failure(failure_message=None):
    if running_mode() == RunningMode.gui:
        try:
            yield
        except Exception:
            if failure_message is None:
                failure_message = "An error occurred running {0}!".format(os.path.basename(sys.argv[0]))
            failure_message += ("\nThe following might be helpful to report to someone, "
                                "or provide a clue about how to fix it:\n\n")
            easygui.codebox(msg=failure_message, text=traceback.format_exc())
    else:
        yield


@contextlib.contextmanager
def friendly_success_and_failure(success_message=None, failure_message=None):
    with friendly_failure(failure_message=failure_message):
        with friendly_success(success_message=success_message):
            yield
