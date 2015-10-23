# -*- coding: utf-8
from __future__ import absolute_import

import warnings
import functools


def deprecated(method):
    @functools.wraps(method)
    def wrapped(obj, *args, **kwargs):
        warnings.warn(
            "%r is deprecated and will be removed in the next version." % method,
            PendingDeprecationWarning
        )
        return method(obj, *args, **kwargs)
    return wrapped


def notimplemented(method):
    """method decorator that throws NotImplementedError()"""
    @functools.wraps(method)
    def error(*args, **kwargs):
        raise NotImplementedError(repr(method))

    return error
