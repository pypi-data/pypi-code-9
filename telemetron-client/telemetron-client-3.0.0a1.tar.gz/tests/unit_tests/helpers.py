"""
Helpers module.

Contains helper classes for tests.
"""

import SocketServer
import SimpleHTTPServer
from Queue import Queue

SocketServer.TCPServer.allow_reuse_address = True

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
    last_response = None
    received_lines = Queue()

    def handle(self):
        if not hasattr(self, "buffer"):
            self.buffer = ""

        data = self.buffer + self.request.recv(1024)

        i = 0
        last = 0
        while 1:
            last = i
            i = data.find("\n", i)
            if i == -1:
                break
            self.received_lines.put(data[last:i])
            i += 1

        self.buffer += data[last:]


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


class MockHTTPHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    ret_code = 201

    def do_PUT(self):
        """Serve a GET request."""
        self.send_response(MockHTTPHandler.ret_code)
        self.send_header("Content-Length", 0)
        self.end_headers()
