# -*- coding: utf-8 -*-
from __future__ import absolute_import

import six
import logging

from suds import client

from .sudsssltransport import SudsClientStrictSSL
from .exceptions import BaseError

logger = logging.getLogger(__name__)

__all__ = ['Portal', 'TransportError', 'Error']

WSDL_PATHS = {
    'super': '/services/VidyoPortalSuperService?wsdl',
    'admin': '/services/v1_1/VidyoPortalAdminService?wsdl',
    'user': '/services/v1_1/VidyoPortalUserService?wsdl',
    'guest': '/services/VidyoPortalGuestService?wsdl',
    'replay': '/replay/services/VidyoReplayContentManagementService?wsdl',
}


def _force_unicode(s):
    """
    If `s` is a bytestring, convert to unicode assuming utf-8
    """
    if s is None:
        return
    if isinstance(s, six.text_type):
        return s
    return s.decode('utf-8')


class Error(BaseError):
    pass


class TransportError(Error):
    pass


class TLSError(TransportError):
    """
    Raised when we are unable to get an encrypted/authenticated conference link.
    """
    def __init__(self, *args, **kwargs):
        super(TLSError, self).__init__(*args, **kwargs)
        self.message = "Could not establish a secure connection"


class _PortalServiceUrl(object):
    """
    Parses /verifies sanity of a given host and selects the WSDL based on the
    value of {api_type}.
    Defaults to the 'admin' api.
    Defaults to using SSL transport.
    defines URL builders for a number of Vidyo locations:
    super, admin, user, guest, and replay WSDLs;
    ajax 'POST' location;
    service base URL
    """

    def __init__(self, host, api_type='admin', ssl=True):
        self.host = host
        self.ssl = True
        self.url = None
        self.ajax_url = None
        self.service_base = None

        try:
            WSDL_PATHS[api_type.lower()]
        except KeyError:
            logger.exception('unknown api type: %s', api_type)
            raise ValueError("unknown VidyoPortal API: %s" % api_type)

        self.api_type = api_type
        self._construct_portal_url(host, api_type, ssl)
        self._construct_ajax_url()
        self._construct_service_url()

    def _construct_portal_url(self, url, api_type, ssl):
        scheme = ssl and 'https://' or 'http://'
        self.ssl = bool(ssl)
        assert (url.startswith(scheme) or (not url.startswith('http://'))), \
            "transport/url mismatch" + ssl and 'ssl' + url

        try:
            if six.moves.urllib_parse.urlparse(url).scheme == '':
                spliturl = six.moves.urllib_parse.urlsplit(scheme + url)
            else:
                spliturl = six.moves.urllib_parse.urlsplit(url)
        except ValueError:
            logger.exception('malformed url:%s', url)
            raise Error("malformed url %s" % url)

        host = spliturl.hostname
        assert host

        self.url = six.moves.urllib_parse.urlparse(
            spliturl.scheme +
            '://' +
            host +
            WSDL_PATHS[self.api_type]
        )
        logger.debug('portal url constructed as %s', self.url.geturl())

    def _construct_ajax_url(self):
        if self.url is None:
            raise AssertionError("Must be called after full url is constructed")

        self.ajax_url = (
            self.url.scheme
            + '://'
            + self.url.netloc
            + '/linkendpoint.ajax'
        )
        logger.debug('ajax url constructed as %s', self.ajax_url)

    def _construct_service_url(self):
        if self.url is None:
            raise AssertionError("URL not constructed;")

        self.services_url = (
            self.url.scheme
            + '://'
            + self.url.netloc
            + '/services')
        logger.debug('service url constructed as %s', self.services_url)

    def geturl(self):
        u = self.url.geturl()
        return u


@six.python_2_unicode_compatible
class Portal(object):
    """Portal class contains the low-level VidyoPortal functionality.
    Instantiation initiates authentication with the portal,
    and initialises the SOAP transport.
    """

    def __init__(self, host, user=None, password=None, api_type='admin', ssl=True):
        host = _force_unicode(host)
        self.user = _force_unicode(user)
        self.password = _force_unicode(password)
        self.ssl = bool(ssl)
        self.api_type = api_type
        if not isinstance(api_type, six.string_types):
            raise TypeError("expected str args, got " + str(type(api_type)))

        self.url = _PortalServiceUrl(host, api_type, ssl)
        # special case for non-authenticated access
        if self.api_type == 'guest':
            try:
                self.client = self.open_soap_client(url=self.url.geturl(), ssl=ssl)
            except Exception as e:
                raise TransportError("Couldn't connect to VidyoPortal:%s" % e)

        else:
            try:
                self.client = self.open_soap_client(
                    url=self.url.geturl(),
                    username=user,
                    password=password,
                    # see above
                    ssl=ssl
                )
            except Exception as e:
                raise
                raise TransportError("Couldn't connect to VidyoPortal: %s" % e)

        self.service = self.client.service

    @staticmethod
    def open_soap_client(**kwargs):
        ssl = bool(kwargs.get('ssl', True))
        if ssl:
            kwargs['verify_ssl'] = True
            # rewrite_to_https=None or ssl is to work around Vidyo's buggy WSDL;
            # see http://tracker.ajenta.net/issues/25 for details
            kwargs['rewrite_to_https'] = True
            suds_kwargs = {k: v for k, v in kwargs.items() if k in (
                'url', 'username', 'password', 'proxy',
                'timeout', 'rewrite_to_https', 'verify_ssl'
            )}
            logger.debug('using strict SSL transport with for SOAP')
            return SudsClientStrictSSL(**suds_kwargs)
        else:
            suds_kwargs = {k: v for k, v in kwargs.items() if k in (
                'url', 'username', 'password', 'proxy', 'timeout'
            )}
        logger.debug('using SUDS default transport with plain HTTP for SOAP')
        return client.Client(**suds_kwargs)

    def __str__(self):
        return "VidyoPortal @ %r" % self.url.geturl()
