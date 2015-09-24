#!/usr/bin/env python

"""
parrot is a simple HTTP server that responds to any valid GET
request with the file specified on the command line.

It is useful during testing (e.g. to mock out a server application),
or to do client testing.
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import magic

import sys, os.path
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), '..')))
from parrot import __version__

file_to_send = {}

class ParrotHTTPRequestHandler(BaseHTTPRequestHandler):
    """
    Request handler for the parrot server. It supports HTTP/1.0.
    All this does is send the file specified at the command line back
    for any GET request.
    """

    server_version = 'parrot/' + __version__
    protocol_version = 'HTTP/1.0'

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', file_to_send['Content-Type'])
        self.end_headers()
        self.wfile.write(file_to_send['data'])

def guess_mime_type(data):
    """
    Guess the mime type of the data given. This seems to default to
    'application/octet-stream' for unrecognised data.
    """
    return magic.from_buffer(data, mime=True).decode('utf-8')

def populate_dict(filename):
    """
    Populate the global dictionary with details of the file to send back.
    We store this globally so the request handler can access it.
    """
    data = open(filename, 'rb').read()

    global file_to_send
    file_to_send = {
        'filename': filename,
        'data': data,
        'Content-Type': guess_mime_type(data)
    }

def parse_args():
    import argparse
    parser = argparse.ArgumentParser(prog='parrot',
            description='Response to incoming HTTP requests with a specified file')
    parser.add_argument('port', type=int, help='Port to listen on')
    parser.add_argument('filename', help='Filename of the data to send in response to all requests')
    parser.add_argument('--version', action='version', version='%(prog)s ' + __version__)
    return parser.parse_args()

def run_server(port):
    server_address = ('', port)
    http = HTTPServer(server_address, ParrotHTTPRequestHandler)
    print('parrot/{v} listening on {server}:{port} with file {filename} ({mt})'.format(
        v=__version__, server=http.socket.getsockname()[0], port=port, filename=file_to_send['filename'], 
        mt=file_to_send['Content-Type']))
    http.serve_forever()

def main():
    args = parse_args()
    populate_dict(args.filename)
    run_server(args.port)


if __name__ == '__main__':
    main()
