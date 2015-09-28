#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
#import logging
import webdav
from webdav.controller import DAVRequestHandler

from notmm.http import httpserver

WSGI_REQUEST_CLASS = DAVRequestHandler

def main():
    wsgi_app = WSGI_REQUEST_CLASS()
    host = webdav.DAV10_CONFIG['DAV'].get('host', 'localhost')
    port = webdav.DAV10_CONFIG['DAV'].get('port', 8081)
    s = httpserver.HTTPServer(wsgi_app, (host, int(port)), **{})
    s.serve()

if __name__ == '__main__':
    main()
