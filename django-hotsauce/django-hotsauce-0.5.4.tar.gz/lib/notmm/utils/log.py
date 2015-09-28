#!/usr/bin/env python
# Copyright (C) 2007-2012 Etienne Robillard <erob@gthcfoundation.org>
# All rights reserved
# <LICENSE=ISC>
"""Basic logging utilities"""
import logging
from notmm.utils.django_settings import SettingsProxy

__all__ = ['configure_logging']


_settings = SettingsProxy(autoload=True).get_settings()

def configure_logging(logger, level=40, loggingClass=logging.FileHandler):
    #XXX: use DJANGO_DEBUG_FILENAME here

    hdl = loggingClass(
        getattr(_settings, 'LOGGING_ERROR_LOG', '/var/log/python.log')
        )
    logger.addHandler(hdl)
    logger.setLevel(level)
    
    return logger

