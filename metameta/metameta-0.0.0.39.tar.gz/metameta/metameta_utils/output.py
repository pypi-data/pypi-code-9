#! /usr/bin/env python

"""print statement with improved functionality"""

from __future__ import print_function

__version__ = '0.0.0.3'

from datetime import datetime
import sys


def output(message, program_verbosity, message_verbosity, log_file=None,
           time_stamp=True, fatal=False):
    """Writes verbosity dependant message to either STDOUT or a log file"""

    if int(program_verbosity) >= int(message_verbosity):
        if time_stamp:
            message_time = '[{0}] '.format(str(datetime.now()))
            message = message_time + message
        if fatal:
            fatal_message = '\nAbove error is fatal. Exiting program.'
            message += fatal_message
        if log_file is None:
            print(message)
        else:
            with open(log_file, 'a') as out_handle:
                out_handle.write(message + '\n')
        if fatal:
            sys.exit(1)
