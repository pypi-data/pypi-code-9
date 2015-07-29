__author__ = 'yue'

from utils.http_conn import *
import sys

class EhcConnection(HttpConnection):
    def __init__(self, host, port=443, protocol='https',
            pool=None, expires=None,
            retry_time=3, http_socket_timeout=10, debug=False):
        """
        @param host - the host to make the connection to
        @param port - the port to use when connect to host
        @param protocol - the protocol to access to web server, "http" or "https"
        @param pool - the connection pool
        @param retry_time - the retry_time when message send fail
        """
        self.host = host
        self.port = port
        self.retry_time = retry_time
        self.http_socket_timeout = http_socket_timeout
        self._conn = pool if pool else ConnectionPool()
        self.expires = expires
        self.protocol = protocol
        self.secure = protocol.lower() == "https"
        self.debug = debug


    def send_request(self, body, type, url, token='', verb='GET'):
        full_url = "/api/%s/%s" % (type, url)
        print full_url
        request = body
        if self.debug:
            print json_dump(request)
            sys.stdout.flush()
        if self.expires:
            request['expires'] = self.expires
        resp = self.send(full_url, request, verb, token=token)
        if self.debug:
            print resp
            sys.stdout.flush()
        if resp:
            return json_loads(resp)

