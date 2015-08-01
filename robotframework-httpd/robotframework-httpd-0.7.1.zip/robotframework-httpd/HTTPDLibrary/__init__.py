# -*- coding: utf-8 -*-
from threading import Thread
import time
import datetime

__author__ = 'mbbn'

import pkg_resources

from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
from SocketServer import ThreadingMixIn
from robot.api import logger


class HTTPDLibrary(object):
    """

    """
    ROBOT_LIBRARY_SCOPE = 'TEST CASE'
    __version__ = pkg_resources.get_distribution("robotframework-httpd").version

    def __init__(self, port, hostname='0.0.0.0'):
        self.port = port
        self.hostname = hostname

    def run_server(self, httpd_server, port):
        try:
            logger.info("Start Http Server with port {}.".format(port), also_console=True)
            httpd_server.serve_forever()
        except KeyboardInterrupt:
            pass

        logger.info("Http Server with port {} is stop.".format(port), also_console=True)
        httpd_server.shutdown()

    def create_httpd(self):
        self.httpd = ThreadedHTTPD((self.hostname, int(self.port)), RequestHandler)
        self.httpd.request_count = 0
        self.httpd.fails = []

    def start_httpd(self):
        try:
            self.httpd
        except (NameError , AttributeError) as e:
            self.create_httpd()

        t = Thread(name=self.port, target=self.run_server, args=(self.httpd, self.port))
        t.daemon = True
        t.start()
        time.sleep(1)

    def stop_httpd(self):
        self.httpd.shutdown()

    def set_wished_request(self, wished_request):
        self.wished_request = wished_request
        try:
            self.httpd.buffer = []
        except AttributeError:
            self.create_httpd()
            self.httpd.buffer = []

    def wait_to_receive_request(self, wished_request=None, timeout=10):
        if(wished_request == None and self.wished_request != None):
            wished_request = self.wished_request
        start = datetime.datetime.now()
        while datetime.datetime.now() < start + datetime.timedelta(seconds=int(timeout)):
            if len(self.httpd.buffer) > 0:
                for buff in self.httpd.buffer:
                    if wished_request["method"] == buff["method"] and wished_request["path"] == buff["path"]:
                        if "body" in wished_request:
                            if wished_request["body"] == buff["body"]:
                                return
                        else:
                            return
            time.sleep(1)

        # if datetime.datetime.now() > start + datetime.timedelta(seconds=int(timeout)):
        self.stop_httpd()
        raise Exception("Not Received Request after {} sec.".format(timeout))

    def wait_to_not_receive_request(self, timeout=10):
        start = datetime.datetime.now()
        while datetime.datetime.now() < start + datetime.timedelta(seconds=int(timeout)):
            if len(self.httpd.buffer) > 0:
                t = datetime.datetime.now() - start
                exceptionError = "Server with port {} received {} request after {}" \
                                 "".format(self.port, len(self.httpd.buffer), t)
                self.stop_httpd()
                raise Exception(exceptionError)

    def reset_buffer(self):
        self.httpd.buffer = []

    def wait_to_recieve_count(self, count, timeout=10):

        start = datetime.datetime.now()
        count = int(count)
        while datetime.datetime.now() < start + datetime.timedelta(seconds=int(timeout)):
            if len(self.httpd.buffer) >= count:
                break

        while datetime.datetime.now() < start + datetime.timedelta(seconds=int(timeout)):
            if len(self.httpd.buffer) > count:
                break

        if len(self.httpd.buffer) != count:
            t = datetime.datetime.now() - start
            exception_error = "Server with port {} received {} request after {}" \
                             "".format(self.port, len(self.httpd.buffer), t)
            self.stop_httpd()
            raise Exception(exception_error)

    def delay_run_httpd(self, delay_time, flag):
        time.sleep(float(delay_time))
        try:
            self.httpd
        except (NameError , AttributeError) as e:
            self.create_httpd()
        if flag == 'True':
            self.httpd.buffer =  self.buffer2
        self.run_server(self.httpd, self.port)

    def delay_to_start_httpd(self, delay_time, flag=False):

        t = Thread(name=self.port, target=self.delay_run_httpd, args=(delay_time,flag))
        t.daemon = True
        t.start()

    def delay_stop_httpd(self, delay_time, flag):
        time.sleep(float(delay_time))
        if flag == 'True' :
            self.buffer2 = self.httpd.buffer
        self.httpd.shutdown()
        del self.httpd

    def delay_to_stop_httpd(self, delay_time, flag=False):

        t = Thread(name=self.port, target=self.delay_stop_httpd, args=(delay_time,flag))
        t.daemon = True
        t.start()


class ThreadedHTTPD(ThreadingMixIn, HTTPServer):

    buffer = []

    def verify_request(self, request, client_address):
        return HTTPServer.verify_request(self, request, client_address)

    def shutdown(self):
        HTTPServer.shutdown(self)

    def server_close(self):
        HTTPServer.server_close(self)

    def add_to_buffer(self, method, path, body):
        self.buffer += [{
            "method": method,
            "path": path,
            "body": body
        }]

    def shutdown_request(self, request):
        HTTPServer.shutdown_request(self, request)

    def close_request(self, request):
        HTTPServer.close_request(self, request)


class RequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        SimpleHTTPRequestHandler.__init__(self, request, client_address, server)

    def do_GET(self):
        """Respond to a GET request."""
        content_len = int(self.headers.getheader('content-length', 0))
        body = self.rfile.read(content_len)
        self.server.add_to_buffer("GET", self.path, body)
        self.send_response(200)

    def do_POST(self):
        """Respond to a POST request."""
        content_len = int(self.headers.getheader('content-length', 0))
        body = self.rfile.read(content_len)
        self.server.add_to_buffer("POST", self.path, body)
        self.send_response(200)

    def log_message(self, format, *args):
        pass