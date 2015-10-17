# encoding: UTF-8
# Copyright (C) 2009-2010, Stefan Schwarzer

"""
This module supports only so much of the CherryPy API that it
can provide a simple single-threaded server which works with
the code in `browser.py`.

Note: For now, the dummy module doesn't actually evaluate the
CherryPy configuration dictionary but takes the configuration
directly from the `config` module.
"""

import BaseHTTPServer
import email.Utils
import httplib

import coding
import config


# exception classes mimicing CherryPy's
class HTTPError(Exception):
    pass

class NotFound(HTTPError):
    pass

class HTTPRedirect(HTTPError):
    pass

# defining this globally is ok as long as we only have one thread
# XXX Is this also true if the request is stopped inbetween?
class Bunch(object):
    pass


class SourceBrowserHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    #protocol_version = "HTTP/1.1"
    server_version = "Websourcebrowser %s" % config.VERSION
    sys_version = ""

    #
    # HTTP-specific processing
    #
    def log_message(self, *args, **kwargs):
        if config.logging:
            return BaseHTTPServer.BaseHTTPRequestHandler.log_message(
                   self, *args, **kwargs)

    def send_data(self, data=u"", http_status=httplib.OK, mtime=None):
        """
        Emit the `data` on the HTTP output stream with a content type
        of `content_type`. If the integer `http_status` is set, it's
        the HTTP status code of the response. The default is 200 (OK).
        If `mtime` is set, it's taken as a floating point value like
        from `time.time()` to set a Last-Modified header.
        """
        headers = response.headers
        self.send_response(http_status)
        if not headers.has_key('Content-Type'):
            # use a sensible default
            headers['Content-Type'] = "text/html"
        for header, value in headers.iteritems():
            self.send_header(header, value)
        self.end_headers()
        content_type = headers["Content-Type"]
        if content_type == "text/html":
            http_status_group = str(http_status)[:1]
            if http_status_group in ("4", "5"):
                data = httplib.responses[http_status]
        if content_type.startswith("text/") or \
          content_type == u"application/javascript":
            try:
                data = coding.encode(data)
            except coding.Error:
                pass
        self.wfile.write(data)

    def _set_up_cherrypy_emulation(self):
        """Set up the `request` variable, so it behaves similar to
        `cherrypy.request`. Only the necessary functionality is
        emulated.
        """
        import browser
        self.wsb = browser.Websourcebrowser()
        # use global objects, so that they're usable as `cherrypy.request`
        #  and `cherrypy.response` in `browser.py`
        global request, response
        request = Bunch()
        request.path_info = self.path
        request.remote = Bunch()
        request.remote.ip = self.client_address[0]
        response = Bunch()
        response.headers = {}

    def do_GET(self):
        """Handle HTTP GET request."""
        self._set_up_cherrypy_emulation()
        # avoid recursive import `browser` <-> `cherrypy_dummy`
        import browser
        check_access_func = browser.check_access()
        try:
            url_parts = request.path_info.split("/")
            # don't consider slashes at start and end of original URL
            url_parts = [part for part in url_parts if part]
            # just a slash in original URL denotes the project's root
            if not url_parts:
                url_parts = ["project"]
            # select handler (`Websourcebrowser` method)
            method = getattr(self.wsb, url_parts[0], self.wsb.default)
            if method is self.wsb.default:
                args = url_parts
            else:
                args = url_parts[1:]
            # call the appropriate handler
            self.send_data(data=method(*args))
        except NotFound, exc:
            print "not found"
        except HTTPRedirect, exc:
            print "redirect"
        except HTTPError, exc:
            print "other error"


def expose(func):
    return func

def quickstart(app_root, script_name, app_config):
    """Start the server as `cherrypy.quickstart` would do.

    Here, `app_root` is the namespace representing the application,
    `app_config` is the configuration dictionary.

    Note that `app_config` isn't even considered here. The
    configuration values are directly taken from the `config` module.
    """
    server_address = (config.http_host, config.http_port)
    httpd = BaseHTTPServer.HTTPServer(server_address, SourceBrowserHandler)
    httpd.serve_forever()

