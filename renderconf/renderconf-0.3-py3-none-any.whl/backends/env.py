# -*- coding: utf-8 -*-
'''
Defines variables from the environment. The prefix is removed and variable
names are lower case.

Arguments:
  * prefix: Include environment variables that begin with this string.
'''
import logging
import os

log = logging.getLogger(__name__)
description = 'Defines variables from the environment'


def dict_vars(source, prefix):
    context = {}
    log.info('Building context from dict for variables with '
             'prefix "{}"'.format(prefix))
    for var, value in source.items():
        if var.startswith(prefix):
            context[var[len(prefix):].lower()] = value

    return context


def context(prefix='CONF_'):
    return dict_vars(os.environ, prefix)
