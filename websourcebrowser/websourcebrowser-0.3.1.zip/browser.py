#! /usr/bin/env python
# encoding: UTF-8
# Copyright (C) 2007-2010, Stefan Schwarzer
# see the file LICENSE for the license of this software

"""
This is the "main program" of Websourcebrowser.

The module contains the application-specific webserver code,
including the handling of some special path prefixes.
"""

from __future__ import with_statement

import cgi
import mimetypes
import os
import sys
import urlparse

import feature
if feature.cherrypy:
    import cherrypy
else:
    import cherrypy_dummy as cherrypy

# Websourcebrowser modules
import coding
import config
import feature
import page
import template
import tools
import urlpath


STATIC_FILES = set([
  # native Websourcebrowser files
  "websourcebrowser.css",
  "websourcebrowser.js",
  "favicon.ico",
  # JQuery core libraries
  "jquery-1.4.2.js",
  "jquery-ui-1.8.js",
  # other JavaScript libraries
  "jquery.layout-1.3.0.rc28.js",
  "jquery.treeview.js",
  "jquery.treeview.css",
  # images for treeview library
  "file.gif",
  "folder-closed.gif",
  "folder.gif",
  "minus.gif",
  "plus.gif",
  "treeview-default-line.gif",
  "treeview-default.gif",
])

def check_access(func=None):
    """Return a new function/method, decorated with an access checker.

    In the new function, an access is denied with an HTTP status code
    403 if 

    - only a specific set of clients is allowed (command line option
      `--allowed-client` != "ALL") and 
    - the client host isn't in the set of allowed clients and
    - the requested URL isn't the Websourcebrowser stylesheet (so an
      error page can still use the CSS)

    If access is granted, just call the original callable and
    return its result. However, if `func` is `None`, suppress
    calling anything; just do the access check.
    """
    def new_func(*args, **kwargs):
        # reject forbidden clients
        not_all_clients_allowed = config.allowed_clients is not \
                                  config.ALL_CLIENTS
        not_this_client_allowed = cherrypy.request.remote.ip not in \
                                  config.allowed_clients
        file_is_not_css = cherrypy.request.path_info != \
                          "/%s/websourcebrowser.css" % config.STATIC_DIR
        if not_all_clients_allowed and not_this_client_allowed and \
          file_is_not_css:
            raise cherrypy.HTTPError(403)
        if func is not None:
            return func(*args, **kwargs)
    return new_func


class Websourcebrowser(object):

    # decorator order matters
    @cherrypy.expose
    @check_access
    def static(self, *args):
        """Handle URLs of the form `/static/...`: If the part
        after `static` is a valid file name, return the file's
        data. The data is searched in the directory `static` in
        the Websourcebrowser module directory.
        """
        # check argument(s)
        if len(args) == 1:
            filename = args[0]
        else:
            #TODO
            raise cherrypy.NotFound()
        if filename not in STATIC_FILES:
            #TODO
            raise cherrypy.NotFound()
        # determine file type (CSS, JavaScript, Gif)
        mime_type = mimetypes.guess_type(filename, strict=False)[0]
        cherrypy.response.headers['Content-Type'] = mime_type
        # find actual file in filesystem
        py_path = os.path.abspath(sys.modules[__name__].__file__)
        static_path = os.path.join(os.path.dirname(py_path), config.STATIC_DIR,
                                   filename)
        # return the file's contents (without encoding anything: if
        #  there are non-ASCII characters, they're usually in comments
        #  where they don't matter)
        if mime_type in ("text/css", "application/javascript"):
            read_mode = "r"
        else:
            read_mode = "rb"
        with open(static_path, read_mode) as fobj:
            data = fobj.read()
        return data

    @cherrypy.expose
    @check_access
    def ajaxfile(self, *args):
        """Handle URLs of the form `/ajaxfile/...`. These are
        HTML fragments intended to be inserted into the file pane.
        """
        url = tools.sequence_to_url(args, absolute=True)
        path = urlpath.to_file_system(url, config.root)
        html = page.file_pane_html(path)
        return html

    @cherrypy.expose
    @check_access
    def image(self, *args):
        """Handle URLs of the form `/image/...`. This is raw
        image data, with the according MIME type set. If the
        file pane should show an image, the image's source
        attribute is set to `/image/<path>`.
        """
        url = tools.sequence_to_url(args, absolute=True)
        path = urlpath.to_file_system(url, config.root)
        with open(path, "rb") as fobj:
            image_data = fobj.read()
        mime_type = mimetypes.guess_type(path, strict=False)[0]
        cherrypy.response.headers['Content-Type'] = mime_type
        return image_data

    @cherrypy.expose
    @check_access
    def raw(self, *args):
        """Handle URLs of the form `/raw/...`. This is used
        to return raw data (for a download). The MIME type is
        set to application/octet-stream.
        """
        # not yet used; binary files are presented as hexdump

    @cherrypy.expose
    @check_access
    def help(self, *args):
        """Shows a help page."""
        return u"Help page isn't available yet."

    @cherrypy.expose
    @check_access
    def project(self, *args):
        """Show a file from the project's filesystem subdirectory.

        The list `args` contains the path components which are to
        be appended on the project root directory.
        """
        # build a complete HTML page
        url = tools.sequence_to_url(args, absolute=True)
        path = urlpath.to_file_system(url, config.root)
        html = page.page_html(path)
        return html

    @cherrypy.expose
    @check_access
    def default(self, *args, **kwargs):
        """(Try to) return the data for a complete page, i. e.
        with `config.PROJECT_DIR` prepended.
        """
        url = tools.sequence_to_url(args, absolute=True)
        if url == "/":
            raise cherrypy.HTTPRedirect("/project/")
        elif url == "/favicon.ico":
            return self.static("favicon.ico")
        raise cherrypy.NotFound()


def startup_info():
    print "Trying to listen on host %s, port %d." % \
          (config.http_host, config.http_port)
    print ("Type http://%s:%d/ into the address field of your "
           "webbrowser.") % (config.http_host, config.http_port)
    print "Access is allowed from these IP addresses:",
    if config.allowed_clients is config.ALL_CLIENTS:
        print "all (running as public server)."
    else:
        print "%s." % (", ".join(sorted(config.allowed_clients)))
    if config.invalid_clients:
        print "Ignored invalid client addresses: %s." % \
              ", ".join(config.invalid_clients)
    if feature.cherrypy:
        print "Using CherryPy as webserver."
    else:
        print "Using built-in (single-threaded) webserver."
    if feature.pygments:
        print "Using Pygments library for syntax highlighting."
    else:
        print "Pygments library not found - no syntax highlighting possible."
        if config.line_numbers:
            print "Pygments library not found - omitting line numbers."
    if 'win' in sys.platform:
        exit_key = "Ctrl-Break"
    else:
        exit_key = "Ctrl-C"
    print "Press %s to exit." % exit_key

def _main():
    config.set_from_environment()
    config.set_from_args()
    startup_info()
    root = Websourcebrowser()
    # configuration dictionary has no effect on `cherrypy_dummy` module
    app_config = {
      "global": {
        "server.protocol_version": "HTTP/1.1",
        "server.environment": "development",
        "server.socket_host": config.http_host,
        "server.socket_port": config.http_port,
        "server.thread_pool": 10,
        "tools.encode.on": True,
        "tools.encode.encoding": "UTF-8",
        "log.screen": config.logging,
      },
      "/favicon.ico": {
        "tools.staticfile.on": True,
        "tools.staticfile.filename": os.getcwd() + "/static/favicon.ico",
      }
    }
    # second argument here is `script_name`, not used though
    cherrypy.quickstart(root, "", app_config)


def main():
    try:
        _main()
    except KeyboardInterrupt:
        print "Aborted by keyboard interrupt from user."

if __name__ == '__main__':
    main()

