# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class IJssorViewlets(IDefaultBrowserLayer):
    """Marker interface that defines a Zope 3 browser layer."""
