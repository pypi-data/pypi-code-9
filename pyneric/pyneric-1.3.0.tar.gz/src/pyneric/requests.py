# -*- coding: utf-8 -*-
"""Helpers for the `requests:requests` library."""

# Support Python 2 & 3.
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from pyneric.future import *

import requests

from pyneric.http import v1_1 as http


SUPPORTED_METHODS = (
    http.GET,
    http.OPTIONS,
    http.HEAD,
    http.POST,
    http.PUT,
    http.patch.PATCH,
    http.DELETE,
)
"""The HTTP methods supported by `requests:requests` as functions.

These are also exposed as methods in :class:`RequestHandler`."""


class RequestHandler(object):

    """Base class for handlers of request calls."""

    def _alter_kwargs(self, kwargs):
        """Allow altering of the request keyword arguments.

        :param dict kwargs: :meth:`request` keyword arguments
        :returns: :meth:`request` keyword arguments
        :rtype: dict

        Override this in a subclass to alter the keyword arguments
        passed to :meth:`request` if it has not been overridden to skip
        the calling of this method.

        """
        return kwargs

    def request(self, method, url, **kwargs):
        """Make an HTTP request using `requests:requests.request`.

        :param string method: request call argument
        :param string url: request call argument
        :param kwargs: request call keyword arguments
        :returns: result of the request
        :rtype: dependent on implementation;
                `~requests:requests.Response` by default

        This can be overridden in a subclass, but the most common use
        case is to extend it.

        """
        kwargs.update(method=method, url=url)
        kwargs = self._alter_kwargs(kwargs)
        handler = requests
        handlers = kwargs.pop('_handlers', ())
        if handlers:
            handler = handlers[0]
            kwargs = dict(kwargs, _handlers=handlers[1:])
        return handler.request(**kwargs)


for _method in SUPPORTED_METHODS:
    # A closure is needed to refer to the correct method.
    def _get_method_func(method):
        def _method_func(self, url, **kwargs):
            kwargs.setdefault('allow_redirects', method.safe)
            return self.request(method.token, url, **kwargs)
        return _method_func
    _method_func = _get_method_func(_method)
    _method_func.__name__ = future.native_str(_method.token.lower())
    _method_func.__doc__ = ("Call :meth:`request` with method '{}'."
                            .format(_method.token))
    setattr(RequestHandler, _method.token.lower(), _method_func)
