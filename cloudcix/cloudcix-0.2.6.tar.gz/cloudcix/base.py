# python
from __future__ import unicode_literals
from datetime import datetime, date, time
import json
import os
import re
import six
# libs
import requests
from requests.auth import AuthBase
# local
from .utils import settings, ExtendedJSONDecoder, ExtendedJSONEncoder

try:
    CLOUDCIX_SERVER_URL = getattr(settings, 'CLOUDCIX_SERVER_URL', None)
except ImportError:
    CLOUDCIX_SERVER_URL = os.environ['CLOUDCIX_SERVER_URL']
# IMPORTANT: shortcut for str to be six.text_type
# (unicode on py2.7 and str on 3+)
str = six.text_type


class MissingServiceKWARG(Exception):

    def __init__(self, arg_name, cli):
        self.message = '"{0}" argument is required by the {1}'.format(
            arg_name, cli)

    def __str__(self):
        return self.message


class TokenAuth(AuthBase):
    """Requests authentication object"""

    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers['X-Auth-Token'] = self.token
        return r


class APIClient(object):

    def __init__(self, application, service_uri, server_url=None,
                 api_version='v1'):
        """Initialises the APIClient with details necessary for the call

        :param application: Application name that will be used as part of
                            service uri, eg. "Membership"
        :type application: unicode
        :param service_uri: Service uri part, eg. "User/"
        :type service_uri: unicode
        :param server_url: Optional, server url for the call,
                           eg. "https://api.cloudcix.com",
                           default: contents of the settings.CLOUCIX_SERVER_URL
                                    variable
        :type server_url: unicode
        :param api_version: Version of the service that should be used,
                            eg. "v1", default: "v1"
        :type api_version: unicode
        """
        self.application = application
        self.headers = {
            'content-type': 'application/json',
        }
        self.service_uri = service_uri
        self.server_url = server_url or self._get_server_url
        self.api_version = api_version

    def __repr__(self):
        return u'<APIClient(%s)>' % "/".join([
            self.server_url, self.application, self.api_version,
            self.service_uri])

    @property
    def _get_server_url(self):
        """Returns the CloudCIX server url.

        :returns: CloudCIX server url
        :rtype: unicode
        """
        self.server_url = CLOUDCIX_SERVER_URL.rstrip('/')
        return self.server_url

    def create(self, token=None, data=None, params=None, **kwargs):
        """Used to create a new resource.

        :param token: Optional, Token to be used for the request.
                      Must be present if method requires authentication.
        :type token: unicode
        :param dict data: Optional, Data to be sent with the request.
        :param dict params: Optional, Query params to be sent along with the
                            request.
        :param kwargs: Any positional arguments required but the service
                       method. For example if method is available at
                       /Membership/v1/Member/<idMember>/Territories/
                       you should pass in idMember=xxx as part of kwargs.
                       Additionally any other parameters that should be passed
                       to requests library call
        :returns: requests.Response
        """
        return self._call('post', token, data=data, params=params, **kwargs)

    def read(self, pk, token=None, params=None, **kwargs):
        """Used to retrieve existing resource.

        :param pk: Unique identifier (primary key) of the object
        :type pk: unicode | int
        :param token: Optional, Token to be used for the request.
                      Must be present if method requires authentication.
        :type token: unicode
        :param dict params: Optional, Query params to be sent along with the
                            request.
        :param kwargs: Any positional arguments required but the service
                       method. For example if method is available at
                       /Membership/v1/Member/<idMember>/Territories/
                       you should pass in idMember=xxx as part of kwargs.
                       Additionally any other parameters that should be passed
                       to requests library call
        :returns: requests.Response
        """
        return self._call('get', token, pk, params=params, **kwargs)

    def update(self, pk, token=None, data=None, params=None, **kwargs):
        """Used to update existing resource.

        :param pk: Unique identifier (primary key) of the object
        :type pk: unicode | int
        :param token: Optional, Token to be used for the request.
                      Must be present if method requires authentication.
        :type token: unicode
        :param dict data: Optional, Data to be sent with the request.
        :param dict params: Optional, Query params to be sent along with the
                            request.
        :param kwargs: Any positional arguments required but the service
                       method. For example if method is available at
                       /Membership/v1/Member/<idMember>/Territories/
                       you should pass in idMember=xxx as part of kwargs.
                       Additionally any other parameters that should be passed
                       to requests library call
        :returns: requests.Response
        """
        return self._call('put', token, pk, data=data, params=params, **kwargs)

    def partial_update(self, pk, token=None, data=None, params=None, **kwargs):
        """Used to partially update existing resource.

        :param pk: Unique identifier (primary key) of the object
        :type pk: unicode | int
        :param token: Optional, Token to be used for the request.
                      Must be present if method requires authentication.
        :type token: unicode
        :param dict data: Optional, Data to be sent with the request. Should
                          contain only the values that are to be updated.
        :param dict params: Optional, Query params to be sent along with the
                            request.
        :param kwargs: Any positional arguments required but the service
                       method. For example if method is available at
                       /Membership/v1/Member/<idMember>/Territories/
                       you should pass in idMember=xxx as part of kwargs.
                       Additionally any other parameters that should be passed
                       to requests library call
        :returns: requests.Response
        """
        return self._call('patch', token, pk, data=data, params=params,
                          **kwargs)

    def delete(self, pk, token=None, params=None, **kwargs):
        """Used to delete an existing resource.

        :param pk: Unique identifier (primary key) of the object
        :type pk: unicode | int
        :param token: Optional, Token to be used for the request.
                      Must be present if method requires authentication.
        :type token: unicode
        :param dict params: Optional, Query params to be sent along with the
                            request.
        :param kwargs: Any positional arguments required but the service
                       method. For example if method is available at
                       /Membership/v1/Member/<idMember>/Territories/
                       you should pass in idMember=xxx as part of kwargs.
                       Additionally any other parameters that should be passed
                       to requests library call
        :returns: requests.Response
        """
        return self._call('delete', token, pk, params=params, **kwargs)

    def bulk_delete(self, token=None, params=None, **kwargs):
        """Used to delete a part of collection. Request body should contain a
        list of elements that should be deleted

        :param token: Optional, Token to be used for the request.
                      Must be present if method requires authentication.
        :type token: unicode
        :param dict params: Optional, Query params to be sent along with the
                            request.
        :param kwargs: Any positional arguments required but the service
                       method. For example if method is available at
                       /Membership/v1/Member/<idMember>/Territories/
                       you should pass in idMember=xxx as part of kwargs.
                       Additionally any other parameters that should be passed
                       to requests library call
        :returns: requests.Response
        """
        return self._call('delete', token, params=params, **kwargs)

    def list(self, token=None, params=None, **kwargs):
        """Used to list resources in a collection.

        :param token: Optional, Token to be used for the request.
                      Must be present if method requires authentication.
        :type token: unicode
        :param dict params: Optional, Query params to be sent along with the
                            request.
        :param kwargs: Any positional arguments required but the service
                       method. For example if method is available at
                       /Membership/v1/Member/<idMember>/Territories/
                       you should pass in idMember=xxx as part of kwargs.
                       Additionally any other parameters that should be passed
                       to requests library call
        :returns: requests.Response
        """
        return self._call('get', token, params=params, **kwargs)

    def head(self, pk=None, token=None, params=None, **kwargs):
        """Used to check existence of a resource/collection.

        :param pk: Optional, unique identifier (primary key) of the object
                   (if the request is against a resource)
        :type pk: unicode | int
        :param token: Optional, Token to be used for the request.
                      Must be present if method requires authentication.
        :type token: unicode
        :param basestring token: Optional, Token to be used for the request.
                                 Must be present if method requires
                                 authentication.
        :param dict params: Optional, Query params to be sent along with the
                            request.
        :param kwargs: Any positional arguments required but the service
                       method. For example if method is available at
                       /Membership/v1/Member/<idMember>/Territories/
                       you should pass in idMember=xxx as part of kwargs.
                       Additionally any other parameters that should be passed
                       to requests library call
        :returns: requests.Response
        """
        return self._call('head', token, pk, params=params, **kwargs)

    def _call(self, method, token=None, pk=None, data=None, params=None,
              **kwargs):
        """Does the actual call using the requests lib.

        :param method: on of the supported http request methods
        :type method: unicode | int
        :param token: Optional, Token to be used for the request.
                      Must be present if method requires authentication.
        :type token: unicode
        :param dict data: Optional, Data to be sent with the request. Should
                          contain only the values that are to be updated.
        :param dict params: Optional, Query params to be sent along with the
                            request.
        :param kwargs: Any additional that should be passed to requests library
                       call
        :returns: requests.Response
        """
        data = data or {}
        service_kwargs, kwargs = self.filter_service_kwargs(kwargs)
        if 'headers' in kwargs:
            kwargs['headers'].updated(self.headers)
        else:
            kwargs['headers'] = self.headers
        if token:
            kwargs['auth'] = TokenAuth(token)
        uri = self.get_uri(pk, service_kwargs)
        data = json.dumps(data, cls=ExtendedJSONEncoder)
        params = self.prepare_params(params)
        response = getattr(requests, method)(uri, data=data, params=params,
                                             **kwargs)

        # Extend the response.json method with setting our decoder by default
        def extended_json_dump(func):
            def wrapper(**kw):
                kw['cls'] = ExtendedJSONDecoder
                return func(**kw)
            return wrapper
        response.json = extended_json_dump(response.json)

        return response

    def prepare_params(self, params):
        """Does processing on url params. Ensures that iterables are parsed
        into format expected by CloudCIX.

        :param dict params: Dictionary of parameters that should be passed to
                            CloudCIX in URL
        :returns: Dictionary with values prepared to be passed directly into
                  requests lib
        :rtype: dict
        """
        if not params:
            return {}
        for k, v in params.items():
            if hasattr(v, 'isoformat'):
                params[k] = v.isoformat()
            elif isinstance(v, bool):
                params[k] = str(v).lower()
            elif hasattr(v, '__iter__'):
                params[k] = str(tuple(
                    str(i).encode('utf-8') if not isinstance(i, bytes) else i
                    for i in v)).replace(' ', '')
        return params

    def filter_service_kwargs(self, kwargs):
        """Filters out kwargs required by the service uri from general kwargs.

        :param dict kwargs: Contains all the keyword arguments received by the
                            method
        :returns: Two dictionaries:
                    service_args - contains only the arguments required in
                                   the service uri
                    kwargs - dictionary with all the service_kwargs filtered
                             out
        :rtype: (dict, dict)
        """
        pattern = re.compile(r'(?<=/\{)(?P<match>\w+)(?=\})')
        result = pattern.findall(self.service_uri)
        service_kwargs = dict(
            (k, str(v).decode('utf-8') if not isinstance(v, str) else v)
            for k, v in kwargs.items() if k in result)

        kwargs = dict(filter(lambda i: i[0] not in result, kwargs.items()))
        return service_kwargs, kwargs

    def get_uri(self, pk=None, service_kwargs=None):
        """Populates the service uri with required arguments and returns the
        final uri that should be used for the call.

        :param pk: Optional unique id if the call is made to a resource
        :type pk: unicode | int
        :param dict service_kwargs: dict containing any other arguments
                                    (beside pk that are required by the service
                                    uri)
        :returns: Absolute uri for the requests call
        :rtype: unicode
        """
        absolute_uri = "/".join([self.server_url, self.application,
                                 self.api_version, self.service_uri])
        if pk is not None:
            absolute_uri += "{0}/".format(
                str(pk).decode('utf-8') if not isinstance(pk, str) else pk)
        service_kwargs = service_kwargs or {}
        try:
            return absolute_uri.format(**service_kwargs)
        except KeyError as e:
            raise MissingServiceKWARG(e.args[0], self)
