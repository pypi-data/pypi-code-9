#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This module is for communicating with im.kayac.com.

"""

from __future__ import absolute_import
from __future__ import unicode_literals
from . import exceptions
from . import constants
import future.standard_library
future.standard_library.install_aliases()
import builtins
import urllib.parse
import urllib.request
import hashlib
import contextlib
import json
import urllib.error
import logging

#: The logger for this module.
api_logger = logging.getLogger(__name__)


def create_post_request(url, params, encoding=constants.KAYACIM_ENCODING):
    """URL-encode the parameters and create a POST request.

    :param url: The URL where a POST request should be sent.
    :type url: str (on Python 3) or unicode (on Python 2)
    :param dict params: The dictionary representing the parameters,
                        whose values should be str (on Python 3) or
                        unicode (on Python 2).
    :param encoding: The encoding should be used.
    :type encoding: str (on Python 3) or unicode (on Python 2)
    :return: an HTTP POST request
    :rtype: :class:`urllib.request.Request` (on Python 3) or
            :class:`future.backports.urllib.request.Request`
            (on Python 2)

    """

    # Encode strings
    enc_params = dict((k, v.encode(encoding)) for k, v in params.items())

    # URL-encode parameters
    api_logger.debug("URL-encoding the parameters.")
    urlenc_params = urllib.parse.urlencode(enc_params).encode(encoding)

    # Create a request
    api_logger.debug("Creating an HTTP POST request.")
    return urllib.request.Request(url=url, data=urlenc_params)


def generate_signature(data, encoding=constants.KAYACIM_ENCODING):
    """Generate the SHA-1 digest of the given string.

    :param data: The string should be processed.
    :type data: str (on Python 3) or unicode (on Python 2)
    :return: the SHA-1 digest
    :rtype: str (on Python 3) or
            :class:`future.types.newstr.newstr` (on Python 2)

    """

    api_logger.debug("Generating a SHA-1 digest.")
    return builtins.str(hashlib.sha1(data.encode(encoding)
                                     ).hexdigest())


class KayacIMAPI(object):
    """Class for accessing im.kayac.com API.

    :param username: The username for your account.
    :type username: str (on Python 3) or unicode (on Python 2)
    :param method: (optional) The authorization method. Choose
                       from
                       :data:`pykayacim.constants.KAYACIM_METHODS`.
    :type method: str (on Python 3) or unicode (on Python 2)
    :param key: (optional) The password or secret key.
    :type key: str (on Python 3) or unicode (on Python 2)
    :raises pykayacim.exceptions.PyKayacIMMethodError: if an
                                                       unavailable
                                                       method is
                                                       specified
                                                       or the
                                                       provided
                                                       information is
                                                       insufficient

    """

    def __init__(self, username, method="none", key=None):
        #: The username for your im.kayac.com account.
        self.username = username
        #: The URL where POST requests should be sent.
        self.post_url = constants.KAYACIM_URL + self.username
        if method in constants.KAYACIM_METHODS:
            #: The authorization method im.kayac.com accepts.
            self.method = method
        else:
            api_logger.critical(
                "Unavailable method: '{method}'".format(method=method))
            raise exceptions.PyKayacIMMethodError(
                details="The method '{method}' is unavailable.".format(
                    method=method))
        if self.method != "none":
            if key is not None:
                #: The password or secret key.
                self.key = key
            else:
                api_logger.critical("Missing parameter: 'key'")
                raise exceptions.PyKayacIMMethodError(
                    details="Provide 'key' for '{method}'.".format(
                        method=method))
        #: The parameters for a POST request.
        self.post_params = dict()
        #: The object representing the request sent to im.kayac.com.
        self.post_request = None
        #: The dictionary representing the response from im.kayac.com.
        self.post_response = None
        api_logger.debug("Successfully initialized a KayacIMAPI instance.")

    def prepare_parameters(self, message, handler=None):
        """Creates a dictionary representing the provided parameters.

        This method is called by
        :meth:`pykayacim.api.KayacIMAPI.send`, and does not need to
        be called directly.

        :param message: The message which should be sent.
        :type message: str (on Python 3) or unicode (on Python 2)
        :param handler: (optional) The URI scheme for iPhone
                        applications, which starts with "mailto:"
                        for example.

        """

        self.post_params["message"] = message
        if handler is not None:
            self.post_params["handler"] = handler
        if self.method == "password":
            self.post_params["password"] = self.key
        elif self.method == "secret":
            self.post_params["sig"] = generate_signature(
                message + self.key)
        api_logger.debug("Prepared the parameters for the POST request.")

    def resend(self):
        """Resend the previous message.

        :raises pykayacim.exceptions.PyKayacIMAPIError: if im.kayac.com
                                                        reports an error
        :raises pykayacim.exceptions.PyKayacIMCommunicationError: if
                                                                  connection
                                                                  with
                                                                  im.kayac.com
                                                                  fails
        :raises pykayacim.exceptions.PyKayacIMMessageError: if no message was
                                                            sent previously

        """

        if self.post_request is None:
            api_logger.error(
                "No message was sent to {username} previously.".format(
                    username=self.username))
            raise exceptions.PyKayacIMMessageError(
                details="No message was sent to {username} previously.".format(
                    username=self.username))
        api_logger.debug("Connecting: {url}".format(url=self.post_url))
        try:
            with contextlib.closing(
                    urllib.request.urlopen(self.post_request)) as res:
                api_logger.debug("Analyzing the response.")
                self.post_response = json.loads(
                    res.read().decode(constants.KAYACIM_ENCODING))
        except urllib.error.URLError as e:
            api_logger.exception("Communication failed: %s", e)
            raise exceptions.PyKayacIMCommunicationError(
                reason=builtins.str(e.reason))
        except ValueError as e:
            api_logger.exception("Invalid response: %s", e)
            raise exceptions.PyKayacIMAPIError(
                errmsg="Invalid response from im.kayac.com.")
        else:
            if self.post_response["result"] != u"posted":
                errmsg = self.post_response["error"]
                api_logger.error("API Error: {errmsg}".format(errmsg=errmsg))
                raise exceptions.PyKayacIMAPIError(errmsg=errmsg)
            else:
                api_logger.info("Sent the notification to {username}".format(
                    username=self.username))

    def send(self, message, handler=None):
        """Send a push notification via im.kayac.com.

        :param message: The message which should be sent.
        :type message: str (on Python 3) or unicode (on Python 2)
        :param handler: (optional) The URI scheme for iPhone applications,
                        which starts with "mailto:" for example.
        :type handler: str (on Python 3) or unicode (on Python 2)
        :raises pykayacim.exceptions.PyKayacIMAPIError: if im.kayac.com
                                                        reports an error
        :raises pykayacim.exceptions.PyKayacIMCommunicationError: if
                                                                  connection
                                                                  with
                                                                  im.kayac.com
                                                                  fails

        """

        self.prepare_parameters(message=message, handler=handler)
        self.post_request = create_post_request(
            url=self.post_url, params=self.post_params)
        self.resend()
