""" Connection class establishes HTTP connection with server.
    Utilized to send Thrift Report Requests.
"""
from thrift import Thrift
from thrift.transport import THttpClient
from thrift.protocol import TBinaryProtocol
from traceguide.crouton import ReportingService

class _Connection(object):
    """ Instances of _Connection are used to establish a connection to
        the server via HTTP protocol.
    """
    def __init__(self, service_url):
        self._service_url = service_url
        self._transport = None
        self._client = None
        self._initial_connection_established = False
        self._report_exceptions_count = 0

    def _open(self):
        """ Establish HTTP connection to the server.
            Note: THttpClient also supports https and will use http/https
                according to the scheme in the URL it is given.
        """
        try:
            # Establish connection to server
            self._transport = THttpClient.THttpClient(self._service_url)
            self._transport.open()
            protocol = TBinaryProtocol.TBinaryProtocol(self._transport)
            self._client = ReportingService.Client(protocol)
            self._initial_connection_established = True
        except Thrift.TException:
            self._report_exceptions_count += 1

    def _close(self):
        """ Close HTTP connection to the server.
        """
        # Close the connection to the server
        if self._transport is None:
            return
        if self._client is None:
            return
        self._transport.close()
