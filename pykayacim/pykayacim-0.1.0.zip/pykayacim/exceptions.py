#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This module contains exceptions of PyKayacIM.

"""

from __future__ import absolute_import
import future.utils


class PyKayacIMError(Exception):
    """This is the base class for the exceptions in this module.

    """

    pass


@future.utils.python_2_unicode_compatible
class PyKayacIMAPIError(PyKayacIMError):
    """Raised when im.kayac.com reports an error.

    :param errmsg: The detailed information about the error.
    :type errmsg: str (on Python 3) or unicode (on Python 2)

    """

    def __init__(self, errmsg):
        self.errmsg = errmsg

    def __str__(self):
        return self.errmsg


@future.utils.python_2_unicode_compatible
class PyKayacIMMethodError(PyKayacIMError):
    """Raised when there is a problem about the authorization method.

    :param details: The detailed information about the problem.
    :type details: str (on Python 3) or unicode (on Python 2)

    """

    def __init__(self, details):
        self.details = details

    def __str__(self):
        return self.details


@future.utils.python_2_unicode_compatible
class PyKayacIMCommunicationError(PyKayacIMError):
    """Raised when communication with im.kayac.com fails.

    This exception will be raised when this module cannot establish
    connection with im.kayac.com, or an HTTP error occurs.

    :param reason: The reason why the communication failed.
    :type reason: str (on Python 3) or unicode (on Python 2)

    """

    def __init__(self, reason):
        self.reason = reason

    def __str__(self):
        return self.reason


@future.utils.python_2_unicode_compatible
class PyKayacIMMessageError(PyKayacIMError):
    """Raised when there is something wrong with the message to be sent.

    :param details: The detailed information about the problem.
    :type details: str (on Python 3) or unicode (on Python 2)

    """

    def __init__(self, details):
        self.details = details

    def __str__(self):
        return self.details
