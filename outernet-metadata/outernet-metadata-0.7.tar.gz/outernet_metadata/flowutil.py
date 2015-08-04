"""
Functions for handling signals

Copyright 2015, Outernet Inc.
Some rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

from __future__ import print_function

import sys
import signal


def oninterrupt(signum, frame):
    print('\nProgram was terminated', file=sys.stderr)
    sys.exit(1)


signal.signal(signal.SIGINT, oninterrupt)
signal.signal(signal.SIGTERM, oninterrupt)
