#!/usr/bin/python

from __future__ import unicode_literals

import os
import socket
import time
import threading

from . import core
try:
    from BaseHTTPServer import BaseHTTPRequestHandler
    from BaseHTTPServer import HTTPServer
    from urllib2 import build_opener, Request, HTTPHandler
    from urllib import quote_plus
except ImportError:
    # Python 3
    unicode = str
    from http.server import BaseHTTPRequestHandler
    from http.server import HTTPServer
    from urllib.request import build_opener, Request, HTTPHandler
    from urllib.parse import quote_plus


CONTENT_TYPE_LATEST = 'text/plain; version=0.0.4; charset=utf-8'
'''Content type of the latest text format'''


def generate_latest(registry=core.REGISTRY):
    '''Returns the metrics from the registry in latest text format as a string.'''
    output = []
    for metric in registry.collect():
        output.append('# HELP {0} {1}'.format(
            metric._name, metric._documentation.replace('\\', r'\\').replace('\n', r'\n')))
        output.append('\n# TYPE {0} {1}\n'.format(metric._name, metric._type))
        for name, labels, value in metric._samples:
            if labels:
                labelstr = '{{{0}}}'.format(','.join(
                    ['{0}="{1}"'.format(
                     k, v.replace('\\', r'\\').replace('\n', r'\n').replace('"', r'\"'))
                     for k, v in sorted(labels.items())]))
            else:
                labelstr = ''
            output.append('{0}{1} {2}\n'.format(name, labelstr, core._floatToGoString(value)))
    return ''.join(output).encode('utf-8')


class MetricsHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', CONTENT_TYPE_LATEST)
        self.end_headers()
        self.wfile.write(generate_latest(core.REGISTRY))

    def log_message(self, format, *args):
        return


def start_http_server(port, addr=''):
    """Starts a HTTP server for prometheus metrics as a daemon thread."""
    class PrometheusMetricsServer(threading.Thread):
        def run(self):
            httpd = HTTPServer((addr, port), MetricsHandler)
            httpd.serve_forever()
    t = PrometheusMetricsServer()
    t.daemon = True
    t.start()


def write_to_textfile(path, registry):
    '''Write metrics to the given path.

    This is intended for use with the Node exporter textfile collector.
    The path must end in .prom for the textfile collector to process it.'''
    tmppath = '%s.%s.%s' % (path, os.getpid(), threading.current_thread().ident)
    with open(tmppath, 'wb') as f:
        f.write(generate_latest(registry))
    # rename(2) is atomic.
    os.rename(tmppath, path)


def push_to_gateway(gateway, job, registry=core.REGISTRY, grouping_key=None, timeout=None):
    '''Push metrics to the given pushgateway.

    This overwrites all metrics with the same job and grouping_key.
    This uses the PUT HTTP method.'''
    _use_gateway('PUT', gateway, job, registry, grouping_key, timeout)


def pushadd_to_gateway(gateway, job, registry=core.REGISTRY, grouping_key=None, timeout=None):
    '''PushAdd metrics to the given pushgateway.

    This replaces metrics with the same name, job and grouping_key.
    This uses the POST HTTP method.'''
    _use_gateway('POST', gateway, job, registry, grouping_key, timeout)


def delete_from_gateway(gateway, job, grouping_key=None, timeout=None):
    '''Delete metrics from the given pushgateway.

    This deletes metrics with the given job and grouping_key.
    This uses the DELETE HTTP method.'''
    _use_gateway('DELETE', gateway, job, None, grouping_key, timeout)


def _use_gateway(method, gateway, job, registry, grouping_key, timeout):
    url = 'http://{0}/job/{1}'.format(gateway, quote_plus(job))

    data = b''
    if method != 'DELETE':
        data = generate_latest(registry)

    if grouping_key is None:
        grouping_key = {}
    url = url + ''.join(['/{0}/{1}'.format(quote_plus(str(k)), quote_plus(str(v)))
                             for k, v in sorted(grouping_key.items())])

    request = Request(url, data=data)
    request.add_header('Content-Type', CONTENT_TYPE_LATEST)
    request.get_method = lambda: method
    resp = build_opener(HTTPHandler).open(request, timeout=timeout)
    if resp.code >= 400:
        raise IOError("error talking to pushgateway: {0} {1}".format(
            resp.code, resp.msg))

def instance_ip_grouping_key():
    '''Grouping key with instance set to the IP Address of this host.'''
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('', 0))
    return {'instance': s.getsockname()[0]}
