# -*- coding: utf-8 -*-
import sys
import io
import http.client
import http
import urllib
import urllib.request
import gzip
import json
import socket
import ssl


class ServerError(Exception):
    """
        raise when take error from server
    """
    pass


class UrlError(Exception):
    """
        raise when url error
    """
    pass


class TLS1Connection(http.client.HTTPSConnection):
    def __init__(self, *args, **kwargs):
        http.client.HTTPSConnection.__init__(self, *args, **kwargs)

    def connect(self):
        sock = socket.create_connection((self.host, self.port), self.timeout)
        if self._tunnel_host:
            self.sock = sock
            self._tunnel()

        self.sock = ssl.wrap_socket(sock, self.key_file, self.cert_file,
                                    ssl_version=ssl.PROTOCOL_TLSv1)


class TLS1Handler(urllib.request.HTTPSHandler):
    def https_open(self, req):
        return self.do_open(TLS1Connection, req)


class XMLStats:

    # host = "erikberg.com"
    # sport = "nba"
    # method = "events"
    # id = None
    # format = "json"
    # parameters = {
    #    'sport': 'nba',
    #     'date': '20130414'
    # }

    def __init__(self, access_token, email):
        self.access_token = access_token
        self.user_agent = "python-xmlstats/0.7 ({email})".format(email=email)
        urllib.request.install_opener(urllib.request.build_opener(TLS1Handler()))

    def make_request(self, host, sport, method, id, format, parameters):

        url = self._build_url(host, sport, method,
                              id, format, parameters)
        req = urllib.request.Request(url)
        req.add_header("Authorization", "Bearer " + self.access_token)
        # Set user agent
        req.add_header("User-agent", self.user_agent)
        # Tell server we can handle gzipped content
        req.add_header("Accept-encoding", "gzip")

        try:
            response = urllib.request.urlopen(req)
        except urllib.request.HTTPError as err:
            raise ServerError(
                "Server returned {code} error code!\n{message}".format(
                    code=err.code,
                    message=json.loads(err.read().decode('utf-8'))), err.code)
        except urllib.request.URLError as err:
            raise UrlError(
                "Error retrieving file: {}".format(
                    err.reason))

        data = None
        if "gzip" == response.info().get("Content-encoding"):
            buf = io.BytesIO(response.read())
            f = gzip.GzipFile(fileobj=buf)
            data = f.read()
        else:
            data = response.read()

        return json.loads(data.decode('utf-8'))

    def _build_url(self, host, sport, method, id, format, parameters):
        """
            build url from args
        """
        path = "/".join(filter(None, (sport, method, id)))
        url = "https://" + host + "/" + path + "." + format
        if parameters:
            paramstring = urllib.parse.urlencode(parameters)
            url = url + "?" + paramstring
        return url
