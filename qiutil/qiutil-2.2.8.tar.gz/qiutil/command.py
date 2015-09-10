"""Command helper functions."""

import os
from . import logging


def add_options(parser):
    """
    Adds the standard ``--log``, ``--quiet``, ``--verbose`` and ``--debug``
    options to the given command line argugment parser.
    """
    parser.add_argument('-l', '--log', help='the log file', metavar='FILE')
    verbosity_grp = parser.add_mutually_exclusive_group()
    verbosity_grp.add_argument(
        '-q', '--quiet', help="only log error messages", dest='log_level',
        action='store_const', const='ERROR')
    verbosity_grp.add_argument(
        '-d', '--debug', help='log debug messages', dest='log_level',
        action='store_const', const='DEBUG')


def configure_log(*names, **opts):
    """
    Configures the logger.

    :param names: the loggers to configure
    :param opts: the following keyword options:
    :keyword log: the log file
    :keyword log_level: the log level
    """
    log_cfg = {}
    if 'log' in opts:
        log_file = os.path.abspath(opts.get('log'))
        log_cfg['filename'] = log_file
    if 'log_level' in opts:
        log_cfg['level'] = opts.get('log_level')
    logging.configure(*names, **log_cfg)
