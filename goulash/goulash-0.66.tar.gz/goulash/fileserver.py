# SOURCE:
#  http://stackoverflow.com/questions/14088294/multithreaded-web-server-in-python
import os
import sys
from SocketServer import ThreadingMixIn
from BaseHTTPServer import HTTPServer
import SimpleHTTPServer

from fabric.colors import red


class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    pass


def main(args):
    port = int(args.port) if args.port else 8000
    _dir = args.dir if args.dir else os.getcwd()
    if not os.path.exists(_dir):
        err = "cannot serve nonexistent directory: {0}".format(_dir)
        raise SystemExit(err)
    os.chdir(_dir)
    msg = "starting file server. port is {0}, directory is {1}"
    msg = msg.format(port, _dir)
    print red(msg)
    server = ThreadingSimpleServer(
        ('', port),
        SimpleHTTPServer.SimpleHTTPRequestHandler)
    try:
        while 1:
            sys.stdout.flush()
            server.handle_request()
    except KeyboardInterrupt:
        print "Finished"

import addict


def runserver(**kargs):
    args = addict.Dict(**kargs)
    main(args)
run_server = runserver

if __name__ == '__main__':
    runserver()
