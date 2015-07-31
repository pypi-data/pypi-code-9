# -*- coding: UTF-8 -*-

"""Logger class"""

# System imports
import logging
import logging.handlers
import sys
import multiprocessing

DEBUG = logging.DEBUG  # 10
INFO  = logging.INFO   # 20
WARN  = logging.WARN   # 30
ERROR = logging.ERROR  # 40

_setup_done = False


def setup_logger(level, stderr=False, instance_name=''):
    """Install default logger"""
    global _setup_done  # pylint: disable=global-statement
    if len(multiprocessing.active_children()):  # pylint: disable=no-member
        return
    if _setup_done:
        return
    root = logging.getLogger()
    lg = root.getChild("syrpc")

    if (
            sys.platform.startswith("mac") or
            sys.platform.startswith("darwin")
    ):  # pragma: no cover
        handler = logging.handlers.SysLogHandler(
            facility=logging.handlers.SysLogHandler.LOG_LOCAL0,
            address='/var/run/syslog'
        )
    else:
        handler = logging.handlers.SysLogHandler(
            facility=logging.handlers.SysLogHandler.LOG_LOCAL0,
            address='/dev/log'
        )

    formatter = logging.Formatter(
        fmt=('syrpc[{0}]: [%(levelname)1.1s %(asctime)s '
             '%(module)s:%(lineno)d] '
             '%(message)s').format(instance_name)
    )
    for rh in root.handlers:
        rh.setFormatter(formatter)
    handler.setFormatter(formatter)
    root.addHandler(handler)

    lg.DEBUG = logging.DEBUG  # 10
    lg.INFO  = logging.INFO   # 20
    lg.WARN  = logging.WARN   # 30
    lg.ERROR = logging.ERROR  # 40
    if stderr:  # pragma: no cover
        errformater = logging.Formatter()
        errhandler  = logging.StreamHandler(sys.stderr)
        errhandler.setFormatter(errformater)
        root.addHandler(errhandler)
    root.setLevel(level)
    _setup_done = True
    return lg
