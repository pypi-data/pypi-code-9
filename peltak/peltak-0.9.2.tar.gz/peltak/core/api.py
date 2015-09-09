#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import absolute_import
import requests
import copy
from igor.jsutil import jsobj, json_loads, json_dumps
from six import PY2, PY3
if PY2:
    from urlparse import urljoin
    from urllib import quote as urlescape
elif PY3:
    from urllib.parse import urljoin, quote as urlescape


class ApiError(RuntimeError):
    """ API error exception class.

    There is an aditional ``response`` field that contains the erranous
    response.
    """
    def __init__(self, response):
        super(ApiError, self).__init__("{}:\n{}".format(
            response.status_code,
            response.content
        ))
        self.response = response


class ApiClient(object):
    """ Wrapper for a HTTP endpoint.

    This will allow HTTP calls using *requests* interface. It also allows
    to store globally a set of defaults for each call. All values will be
    passed as arguments to *requests* and headers will be merged with those
    in the request.
    """
    def __init__(self, endpoint):
        self.endpoint = endpoint
        self.defaults = jsobj()

    def _process_args(self, args):
        ret = copy.copy(self.defaults)
        if 'headers' in self.defaults and 'headers' in args:
            headers = self.defaults['headers']
            headers.update(args['headers'])
            args['headers'] = headers
        ret.update(args)
        return ret

    def get(self, url, **kwargs):
        args = self._process_args(kwargs)
        u = urljoin(self.endpoint, url)
        return requests.get(urljoin(self.endpoint, url), **args)

    def post(self, url, **kwargs):
        args = self._process_args(kwargs)
        return requests.post(urljoin(self.endpoint, url), **args)

    def put(self, url, **kwargs):
        args = self._process_args(kwargs)
        return requests.put(urljoin(self.endpoint, url), **args)

    def delete(self, url, **kwargs):
        args = self._process_args(kwargs)
        return requests.delete(urljoin(self.endpoint, url), **args)


class Gitlab(object):
    """ Gitlab API """

    def __init__(self, url, token=None, verify_ssl=True):
        self.api = ApiClient(urljoin(url, '/api/v3/'))
        self._token = None
        self.token = token
        self.users = None
        self.branches = None
        self.api.defaults['verify'] = verify_ssl

    def _parse_response(self, r):
        try:
            content = json_loads(r.content)
            if isinstance(content, list):
                return [jsobj(item) for item in content]
            return jsobj(r.content)
        except:
            return jsobj()

    @property
    def logged_in(self):
        """ Return ``True`` if the instance is logged in (has token) """
        return self.token is not None

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, value):
        """ Set token.

        The token will be passed in each request for authorization.
        """
        self._token = value
        if value is not None:
            headers = self.api.defaults.setdefault('headers', {})
            headers['PRIVATE-TOKEN'] = value

    def login(self, username, password):
        """ Login to remote Gitlab instance. """
        r = self.api.post('session', data={
            'login': username,
            'password': password,
        })
        if r.status_code != 201:
            raise ApiError(r)
        user = self._parse_response(r)
        self.token = user.get('private_token')
        return user

    def current_user(self):
        """ Return currently logged in users """
        r = self.api.get('user')
        if r.status_code != 200:
            raise ApiError(r)
        return self._parse_response(r)

    def list_users(self, force_fetch=False):
        """ List all users on the remote instance.

        :arg force_fetch:   If set to ``True``. This will force HTTP request
                            to fetch the user list from remote instance.
                            Otherwise it will use cached version.
        """
        if force_fetch or self.users is None:
            r = self.api.get('users', params={'per_page': 100})

            if r.status_code != 200:
                raise ApiError(r)

            self.users = [jsobj(u) for u in r.json()]

        return self.users

    def list_branches(self, project_id, force_fetch=False):
        """ List remote branches.

        :arg project_id:    ID of the project for which the branches will be
                            listed.
        :arg force_fetch:   If set to ``True``. This will force HTTP request
                            to fetch the branch list from remote instance.
                            Otherwise it will use cached version.
        """
        if force_fetch or self.branches is None:
            url = 'projects/{}/repository/branches'.format(project_id)
            r = self.api.get(url, params={'per_page': 100})

            if r.status_code != 200:
                raise ApiError(r)

            self.branches = [jsobj(u) for u in r.json()]

        return self.branches

    def has_user(self, username):
        """ Check if the user with the given *username* exists. """
        users = self.list_users()
        return username in (u.username for u in users)

    def find_user(self, username):
        """ Return the user with the given *username* if it exists. """
        return next((u for u in self.list_users() if u.username == username),
                    None)

    def get_project(self, id):
        """ Return the project with the given ID.

        :arg id:    Either project ID as int or a NAMESPACE/PROJECT string.
        """
        url = 'projects/{}'.format(urlescape(str(id), safe=''))
        r = self.api.get(url)
        if r.status_code != 200:
            raise ApiError(r)
        return self._parse_response(r)

    def get_mr(self, project_id, mr_id):
        """ Get MR by ID.

        :arg project_id:    Project ID for which we're requesting a MR.
        :arg mr_id:         The merge request ID.
        """
        url = 'projects/{}/merge_requests?iid={}'.format(project_id, mr_id)
        r = self.api.get(url)
        if r.status_code != 200:
            raise ApiError(r)
        results = self._parse_response(r)
        if results:
            return results[0]
        return jsobj()

    def create_mr(self, project_id, mr):
        """ Create merge request.

        :arg project_id:    Project ID for which we're creating a MR.
        :arg mr:            A dictionary like object that contains the MR
                            details. For more information consult Gitlab API
                            reference.
        """
        project_id = urlescape(str(project_id), safe='')
        r = self.api.post(
            'projects/{}/merge_requests'.format(project_id),
            headers = {'content-type': 'application/json'},
            data    = json_dumps(mr)
        )
        if r.status_code != 201:
            raise ApiError(r)
        return self._parse_response(r)

    def update_mr(self, project_id, mr_id, values):
        """ Update merge request.

        :arg project_id:    Project ID for which we're creating a MR.
        :arg mr_id:         The ID of the merge request to change.
        :arg mr:            A dictionary like object that contains the values
                            to update in the merge request.
        """
        url = 'projects/{}/merge_request/{}'.format(project_id, mr_id)
        r = self.api.put(
            url,
            headers = {'content-type': 'application/json'},
            data    = json_dumps(values),
        )
        if r.status_code != 200:
            raise ApiError(r)
        return self._parse_response(r)

