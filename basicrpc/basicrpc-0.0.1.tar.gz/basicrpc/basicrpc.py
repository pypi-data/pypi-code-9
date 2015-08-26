# -*- coding: utf-8 -*-
"""
    basicrpc
    ~~~~~
    authors: Jude Nelson and Muneeb Ali
    license: MIT, see LICENSE for more details.
"""

import socket
import uuid
import json

from .config import MAX_RPC_LEN


class Proxy(object):
    """
    Not-quite-JSONRPC client.
    For metstring servers that expect a raw Netstring that encodes
    a JSON object with a "method" string and an "args" list.  It will ignore
    "id" and "version", and will not accept keyword arguments.  It also does
    not guarantee that the "result" and "error" keywords will be present.
    """

    def __init__(self, server, port, max_rpc_len=MAX_RPC_LEN):
        self.server = server
        self.port = port
        self.sock = None
        self.max_rpc_len = max_rpc_len

    def __getattr__(self, key):
        try:
            return object.__getattr__(self, key)
        except AttributeError:
            return self.dispatch(key)

    def socket():
        return self.sock

    def default(self, *args):
        self.params = args
        return self.request()

    def dispatch(self, key):
        self.method = key
        return self.default

    def ensure_connected(self):
        if self.sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
            self.sock.connect((self.server, self.port))

        return True

    def request(self):

        self.ensure_connected()
        request_id = str(uuid.uuid4())
        parameters = {
            'id': request_id,
            'method': self.method,
            'params': self.params,
            'version': '2.0'
        }

        data = json.dumps(parameters)
        data_netstring = str(len(data)) + ":" + data + ","

        # send request
        self.sock.sendall(data_netstring)

        # get response: expect comma-ending netstring
        # get the length first
        len_buf = ""

        while True:
            c = self.sock.recv(1)
            if len(c) == 0:
                # connection closed
                self.sock.close()
                raise Exception("Server closed remote connection")

            c = c[0]

            if c == ':':
                break
            else:
                len_buf += c
                buf_len = 0

                # ensure it's an int
                try:
                    buf_len = int(len_buf)
                except Exception, e:
                    # invalid
                    self.sock.close()
                    raise Exception("Invalid response: invalid netstring length")

                # ensure it's not too big
                if buf_len >= self.max_rpc_len:
                    self.sock.close()
                    raise Exception("Invalid response: message too big")

        # receive message
        response = self.sock.recv(buf_len+1)

        # ensure that the message is terminated with a comma
        if response[-1] != ',':
            self.sock.close()
            raise Exception("Invalid response: invalid netstring termination")

        # trim ','
        response = response[:-1]

        # parse the response
        try:
            result = json.loads(response)
        except Exception, e:

            # try to clean up
            self.sock.close()
            raise Exception("Invalid response: not a JSON string")

        return result
