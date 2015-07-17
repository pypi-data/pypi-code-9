# -*- coding: utf-8 -*-
#
# Copyright 2015 Grigoriy Kramarenko <root@rosix.ru>
#
# This file is part of RosixDocs theme for Sphinx.
#
import os

VERSION = (0, 1, 3)

def get_version(*args, **kwargs):
    return '%d.%d.%d' % VERSION

def get_docs_version(*args, **kwargs):
    return '%d.%d' % VERSION[:2]

__version__ = get_version()


def get_themes_path():
    """ Returns path to included themes. """
    return os.path.abspath(os.path.join(os.path.dirname(__file__), 'themes'))

