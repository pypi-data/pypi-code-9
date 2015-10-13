#!/usr/bin/env python
#
# Copyright 2015-2016 calvin
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

__version__ = '0.2.3'

import json
import requests


class AplazameError(Exception):

    """
    Exception Handling
    """

    def __init__(self, response=None, ctype='json'):
        self.response = response
        self.code = response.status_code

        if response is not None and ctype == 'json':
            try:
                error = json.loads(response.content)['error']
            except ValueError:
                self.message = 'Unknown Error'
                self.type = None
            else:
                self.message = error['message']
                self.type = error['type']

    def __str__(self):
        return "{self.code}.{self.message}".format(self=self)

    def __repr__(self):
        return str(self)


class Client(object):

    """
    A client for the Aplazame Recovery API.
    See http://docs.aplazame.com/ for complete API documentation.
    """

    user_agent = 'AplazameSdk/rest-sdk-aplazame ' + __version__

    def __init__(self, access_token, sandbox=False, version='1',
                 ctype='json', ssl=True, host=None, verify=True):

        self.access_token = access_token
        self.version = version
        self.ctype = ctype
        self.sandbox = sandbox
        self.ssl = ssl
        self.verify = verify

        if host is None:
            self.host = 'api.aplazame.com'
        else:
            self.host = host

    @property
    def headers(self):
        return {
            'User-Agent': self.user_agent,
            'Authorization': 'Bearer ' + self.access_token,
            'Accept': "application/vnd.aplazame{site}.v{s.version}+{s.ctype}"
            .format(site=('.sandbox' if self.sandbox else ''), s=self)
        }

    def request(self, url, method, headers=None, **kwargs):
        http_headers = self.headers
        http_headers.update(headers or {})

        response = requests.request(
            method, url, headers=http_headers, verify=self.verify, **kwargs)

        if not (200 <= response.status_code < 300):
            raise AplazameError(response)

        return response

    def _endpoint(self, action, method, **kwargs):
        url = "{prot}://{self.host}/{action}".format(
            self=self, action=action, prot=('https' if self.ssl else 'http'))

        return self.request(url, method, **kwargs)

    def get(self, action, params=None, **kwargs):
        kwargs.update((params or {}))
        return self._endpoint(action, 'GET', params=kwargs)

    def post(self, action, json=None):
        return self._endpoint(action, 'POST', json=json)

    def put(self, action, json=None):
        return self._endpoint(action, 'PUT', json=json)

    def patch(self, action, json=None):
        return self._endpoint(action, 'PATCH', json=json)

    def delete(self, action, **kwargs):
        return self._endpoint(action, 'DELETE', **kwargs)

    def merchants(self, params=None, **kwargs):
        return self.get('merchants', params, **kwargs)

    def merchant_detail(self, id):
        return self.get("merchants/{id}".format(id=id))

    def me(self):
        return self.get('me')

    def operations(self, params=None, **kwargs):
        return self.get('me/operations', params, **kwargs)

    def payments(self, params=None, **kwargs):
        return self.get('me/payments', params, **kwargs)

    def merchant_request(self, service, id, params=None, **kwargs):
        return self.get("merchants/{0}/{1}".format(
            id, service), params, **kwargs)

    def customers(self, params=None, **kwargs):
        return self.get('customers', params, **kwargs)

    def customer_detail(self, id):
        return self.get("customers/{id}".format(id=id))

    def orders(self, params=None, **kwargs):
        return self.get('orders', params, **kwargs)

    def order_detail(self, id):
        return self.get("orders/{id}".format(id=id))

    def authorize(self, id):
        return self.post("orders/{id}/authorize".format(id=id))

    def cancel(self, id):
        return self.post("orders/{id}/cancel".format(id=id))

    def refund_check(self, id):
        return self.get("orders/{id}/refund".format(id=id))

    def refund(self, id, amount):
        return self.post("orders/{id}/refund".format(id=id), {
            'amount': amount
        })

    def update(self, id, json, partial=False):
        if partial:
            request = self.patch
        else:
            request = self.put

        return request("orders/{id}".format(id=id), json)

    def history(self, id, json):
        return self.post("orders/{id}/history".format(id=id), json)

    def simulator(self, amount):
        return self.get('instalment-plan-simulator', {'amount': amount})
