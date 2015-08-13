"""
qson

Quick JSON based key value store over http
"""
import os
import sys

import server
import client

VERSION = "0.0.1"

def make_daemon():
    # Daemonize to run in background
    pid = os.fork()
    if pid > 0:
        # exit first parent
        sys.exit(0)
    pid = os.fork()
    if pid > 0:
        # exit second parent
        sys.exit(0)
    else:
        output = open("/dev/null", 'wb')
    sys.stdout = output
    sys.stderr = output

def start(port=server.PORT, daemon=False):
    """
    Starts the webserver, first argument is port number, default is 9898
    """
    if type(port) != int:
        port = int(port)
    address = (server.ADDRESS, port)
    test_server = server.ThreadedHTTPServer(address, server.Handler)
    if daemon is not False:
        make_daemon()
    test_server.serve_forever()

def method(*args):
    """
    Runs client methods
    """
    test_client = client.client()
    action = getattr(test_client, args[0])
    print action(*args[1:])

def query(*args):
    """
    Runs client get or set
    """
    test_client = client.client()
    print test_client(*args)

def main():
    action = getattr(sys.modules[__name__], sys.argv[1])
    action(*sys.argv[2:])

if __name__ == '__main__':
    main()
