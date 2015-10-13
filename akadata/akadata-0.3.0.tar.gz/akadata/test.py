# Copyright (c) 2015, RedJack, LLC.
# All rights reserved.
#
# Please see the COPYING file in this distribution for license details.
import struct

try:
    import SocketServer as socketserver
except ImportError:  # Py3
    import socketserver

from akadata import status, EDGESCAPE_VERSION


def format_edgescape_response(ip, data, status_code=status.AKAMAI_OK,
                              version=EDGESCAPE_VERSION, flags=0, size=None):
    """
    Convert an IP address and a dict (e.g. the result of an `ip_lookup`)
    into a bytestring that EdgeScape could have returned to produce the
    input `data`.

    Useful for generating responses for `akadata.test.FakeEdgeScapeServer`.
    """
    data = data.copy()

    # If `data` is the result of an `ip_lookup` call, it will have an 'ip'
    # key added.
    data.pop('ip', None)

    if data.get('default_answer') is False:
        # default_answer=False was set by our client
        del data['default_answer']
    elif data.get('default_answer') is True:
        # Akamai encodes booleans as T/F
        data['default_answer'] = 'T'

    # Encode lists (of numbers or strings) as '+' delimited strings
    for key, val in data.items():
        if isinstance(val, list):
            data[key] = '+'.join('%s' % v for v in val)

    # The result/data portion of the EdgeScape response consists of the
    # IP address concatenated with null-byte separated key=value pairs with
    # the GeoIP/network/etc. information. Finally, each response ends with
    # two null bytes.
    packed_data = ip + '\x00'.join(
        '{}={}'.format(key, val) for key, val in sorted(data.items())
    ) + '\x00\x00'
    packed_data = packed_data.encode('utf-8')

    # We allow the user to set an invalid size if they provide the `size`
    # kwarg.
    if size is None:
        size = len(packed_data) + 8

    return struct.pack('!BBHHBB{}s'.format(len(packed_data)),
                       version, flags, 0, size, status_code, 0, packed_data)


class FakeEdgeScapeServer(socketserver.UDPServer):
    """
    A UDP server that pops responses from `self.responses` on each request.
    """

    def __init__(self, port=0):
        socketserver.UDPServer.__init__(self, ('localhost', port), None)

        self.responses = []

    def finish_request(self, request, client_address):
        socket = request[1]
        socket.sendto(self.responses.pop(), client_address)

    @property
    def host(self):
        return self.server_address[0]

    @property
    def port(self):
        return self.server_address[1]
