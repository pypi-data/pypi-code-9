# coding: utf-8
import urllib
import platform

import requests

import exceptions
import http_codes
import version


class Resource(object):
    __slots__ = ('entrypoint', 'args', 'kwargs')

    def __init__(self, entrypoint=None, *args, **kwargs):
        self.entrypoint = entrypoint or 'https://drivigo.com/api/v1/'
        self.args = args
        self.kwargs = kwargs

    def get_headers(self):
        user_agent = "drivigo-api-client-python {} (python-{}) ({})".format(
            version.version,
            platform.python_version(),
            platform.version()
        )
        return {
            "User-Agent": user_agent,
            "Accept-Charset": "utf-8",
        }

    def make_exception(self, url, method, code, msg):
        cls = http_codes.codes.get(code, exceptions.ClientException)
        return cls(url=url, method=method, code=code, msg=msg)

    def raise_for_status(self, response):
        if not response.ok:
            raise self.make_exception(url=response.url, method=response.request.method, code=response.status_code,
                                      msg=response.text)

    def get_entrypoint(self, *args, **kwargs):
        url = self.entrypoint
        if args:
            url += '/'.join([urllib.quote(r) for r in args])
            if url[-1] != '/':
                url += '/'
        if kwargs:
            url += '?' + '&'.join('{}={}'.format(urllib.quote(k), urllib.quote(v))
                                  for k, v in kwargs.items())
        return url

    def request(self, method=None, url=None, headers=None, *args, **kwargs):
        if headers is None:
            headers = self.get_headers()
        else:
            new_headers = self.get_headers()
            new_headers.update(headers)
            headers = new_headers
        response = requests.session().request(method=method, url=url, headers=headers, *args, **kwargs)
        self.raise_for_status(response)
        return response
