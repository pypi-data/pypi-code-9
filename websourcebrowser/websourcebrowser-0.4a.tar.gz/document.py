# encoding: UTF-8
# Copyright (C) 2008-2010, Stefan Schwarzer
# see the file LICENSE for the license of this software

"""
A simple class `Document` representing documents from the filesystem
to be rendered.
"""

import cgi

import coding
import tools


class ReadError(Exception):
    """Error encountered while reading a document (or trying to)."""
    pass


class Document(object):
    """Represent a rather generic document which can be rendered as HTML."""

    def __init__(self, **kwargs):
        """Init this document from the supplied keyword arguments.
        These are the starting point for converters which will work
        on the document.

        If an argument `path` is passed in, it will be normalized and
        the original path value be stored as the `original_path`
        attribute.
        """
        self.__dict__.update(kwargs)
        if hasattr(self, "path"):
            self.original_path = self.path
            self.path = tools.normalize_path(self.path)
        self.html = u""
        self.mime_type = None

