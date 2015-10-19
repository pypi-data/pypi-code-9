'''
Objects handling preparation and sending of the queries.

Copyright (c) 2015 Skylable Ltd.
License: Apache 2.0, see LICENSE for more details.

'''

import functools
import json
import hashlib
import hmac
import os
import sys
import time
from email.utils import formatdate

import requests
from requests import ConnectionError, HTTPError
from requests.packages.urllib3.poolmanager import PoolManager

from .exceptions import SXClusterFatalError, SXClusterNonFatalError
from .models import QueryParameters
from .utils import generate_poll_times

class QueryHandler(object):
    '''
    Prepare and send a query to an SX cluster.

    Initialization parameters (set as the attributes):
      - node_address -- address of the cluster's node to connect to
      - cluster -- Cluster data structure containing cluster's location
        data
      - session -- requests.Session-derived object used to send the
        requests

    Other attributes:
      - url -- actual URL used to connect to the node
      - query -- latest sent query
      - response -- latest received response
      - poll_time_gen -- poll time generator; if replaced, should
        accept two arguments, start and end, and indefinitely yield the
        values from the interval bounded by start and end.
    '''

    def __init__(self, node_address, cluster, session):
        self.node_address = node_address
        self.cluster = cluster
        self.session = session
        self.query = None
        self.response = None
        self.poll_time_gen = functools.partial(generate_poll_times, steps=10)

    @property
    def url(self):
        return self.cluster.get_host_url(self.node_address)

    def prepare_query(self, query_params, body=None):
        query = self._create_query(query_params, body)
        self.query = query

    def make_query(self):
        if self.query.is_complex:
            self._make_complex_query()
        else:
            self._make_simple_query()

    def _make_simple_query(self):
        self.response = self._send_request(self.query, self.session)

    def _make_complex_query(self):
        resp = self._send_request(self.query, self.session)
        resp_body = resp.json()
        req_id = resp_body[u'requestId']
        min_time = resp_body[u'minPollInterval'] / 1000.0
        max_time = resp_body[u'maxPollInterval'] / 1000.0

        for period in self.poll_time_gen(min_time, max_time):
            time.sleep(period)
            resp = self._make_poll_query(req_id)
            self.response = resp
            resp_body = resp.json()
            status = resp_body[u'requestStatus']

            if status == u'PENDING':
                continue
            elif status == u'OK':
                break
            elif status == u'ERROR':
                resp_msg = resp_body[u'requestMessage']
                raise SXClusterNonFatalError(resp_msg)
            else:
                raise SXClusterNonFatalError('Invalid poll response status')

    def _create_query(self, query_params, body=None):
        verb, is_complex, path, params = (query_params.verb,
                                          query_params.is_complex,
                                          query_params.path,
                                          query_params.params)

        url = '/'.join([self.url, path])
        body_str = json.dumps(body, encoding='utf-8') if body else ''
        query = requests.Request(verb, url, params=params, data=body_str)
        query = self.session.prepare_request(query)
        query.is_complex = is_complex
        return query

    def _make_poll_query(self, req_id, timeout=None):
        poll_query = self._create_query(_jobPollParams(req_id))
        resp = self._send_request(poll_query,
                                  self.session,
                                  timeout=timeout)
        return resp

    @staticmethod
    def _send_request(req, session, timeout=None):
        '''
        Send 'requests.PreparedRequests', using session provided in the
        argument and raise error in case of failure.
        '''
        try:
            resp = session.send(req, timeout=timeout)
        except ConnectionError:
            err_val, err_tb = sys.exc_info()[1:]
            raise SXClusterNonFatalError, str(err_val), err_tb

        # Check whether the response status is valid.
        try:
            resp.raise_for_status()
        except HTTPError:
            err_val, err_tb = sys.exc_info()[1:]
            try:
                resp_msg = resp.json()[u'ErrorMessage']
            except ValueError:
                resp_msg = ''
            if (400 <= resp.status_code < 500 and
                    resp.status_code not in (404, 408, 429)):
                raise SXClusterFatalError, str(err_val) + resp_msg, err_tb
            else:
                raise SXClusterNonFatalError, str(err_val) + resp_msg, err_tb
        # Check whether the response content is parseable into JSON.
        try:
            info = resp.json()
        except ValueError:
            err_val, err_tb = sys.exc_info()[1:]
            new_msg = ': '.join(['Cannot parse JSON', str(err_val)])
            raise SXClusterNonFatalError, new_msg, err_tb
        # Check whether there is an error message in parsed response content.
        if u'ErrorMessage' in info:
            raise SXClusterNonFatalError(info[u'ErrorMessage'])

        return resp


class ClusterSession(requests.Session):
    '''
    Custom session object used by a QueryHandler object.

    Initialization parameters:
      - cluster -- Cluster data structure; cluster.name is used for SSL
        verification
      - user_data -- UserData object used for authentication
      - verify -- parameter indicating whether the SSL certificate should be
        validated; defaults to True. If string is be passed as a value, it is
        be used as a path to a custom trusted CA bundle for certificate
        verifications.
    '''

    def __init__(self, cluster, user_data=None, verify=True):
        super(ClusterSession, self).__init__()
        self.mount('https://', SXHostnameAdapter(assert_hostname=cluster.name))
        if user_data is not None:
            self.auth = SXAuth(user_data)
        self.verify = verify


class SXAuth(requests.auth.AuthBase):
    '''
    Attach custom 'Authorization' and 'Date' headers to the request;
    the headers are required for SX cluster-side request authentication.
    '''

    def __init__(self, user_data):
        self.uid = user_data.uid
        self.secret_key = user_data.secret_key
        self.padding = user_data.padding

    def __call__(self, r):
        body = '' if not r.body else r.body
        bodysha1 = hashlib.sha1(body).hexdigest()
        date = formatdate(timeval=None, localtime=False, usegmt=True)
        request_string = '\n'.join([r.method,
                                    r.path_url.lstrip('/'),
                                    date,
                                    bodysha1,
                                    ''])

        digest = hmac.new(self.secret_key, request_string,
            hashlib.sha1).digest()
        auth_token = self.uid + digest + self.padding
        auth_header = ' '.join(['SKY', auth_token.encode('base64').rstrip()])

        r.headers['Authorization'] = auth_header
        r.headers['Date'] = date
        return r


class SXHostnameAdapter(requests.adapters.HTTPAdapter):
    def __init__(self, assert_hostname=None, **kwargs):
        self.assert_hostname = assert_hostname
        super(SXHostnameAdapter, self).__init__(**kwargs)

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       assert_hostname=self.assert_hostname)


def _jobPollParams(req_id):
    '''Create query parameters object for job poll query.'''
    params = QueryParameters(sx_verb='GET',
                             path_items=['.results', req_id],
                             bool_params=set(),
                             dict_params={})
    return params
