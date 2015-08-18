import sys, re, lyricscreen, os, posixpath, urllib, cgi, shutil, mimetypes

from io import BytesIO
from os import path
from http.server import HTTPServer, BaseHTTPRequestHandler

from .settings import settings, default_settings_dir

local_web_root = os.path.join(default_settings_dir, "web_client")
if isinstance(settings.web_client_dir, bool):
    pass
else:
    local_web_root = settings.web_client_dir
web_root = path.abspath(local_web_root)

class WebClientRequestHandler(BaseHTTPRequestHandler):

    """Simple HTTP request handler with GET and HEAD commands.

    This serves files from the current directory and any of its
    subdirectories.  It assumes that all files are plain text files
    unless they have the extension ".html" in which case it assumes
    they are HTML files.

    The GET and HEAD requests are identical except that the HEAD
    request omits the actual contents of the file.

    """

    server_version = "LyricScreenHTTP/" + lyricscreen.__version__

    def send_head(self):
        """Common code for GET and HEAD commands.

        This sends the response code and MIME headers.

        Return value is either a file object (which has to be copied
        to the outputfile by the caller unless the command was HEAD,
        and must be closed by the caller under all circumstances), or
        None, in which case the caller has nothing further to do.

        """
        path = self.translate_path(self.path)
        path = path.split('?', maxsplit=1)[0]
        f = None
        if os.path.isdir(path):
            for index in "index.html", "index.htm":
                index = os.path.join(path, index)
                if os.path.exists(index):
                    path = index
                    break
            else:
                return self.list_directory(path)
        ctype = self.guess_type(path)
        if ctype.startswith('text/'):
            mode = 'r'
        else:
            mode = 'rb'
        mode = 'rb'
        try:
            f = open(path, mode)
        except IOError:
            self.send_error(404, "File not found")
            return None
        self.send_response(200)
        self.send_header("Content-type", ctype)
        self.end_headers()
        return f

    def list_directory(self, path):
        """Helper to produce a directory listing (absent index.html).

        Return value is either a file object, or None (indicating an
        error).  In either case, the headers are sent, making the
        interface the same as for send_head().

        """
        try:
            list = os.listdir(path)
        except os.error:
            self.send_error(404, "No permission to list directory")
            return None
        f = BytesIO()
        f.write(bytes("<title>Directory listing for %s</title>\n" % self.path,
            'UTF-8'))
        f.write(bytes("<h2>Directory listing for %s</h2>\n" % self.path,
            'UTF-8'))
        f.write(bytes("<hr>\n<ul>\n", 'UTF-8'))
        for name in list:
            fullname = os.path.join(path, name)
            displayname = linkname = name = cgi.escape(name)
            # Append / for directories or @ for symbolic links
            if os.path.isdir(fullname):
                displayname = name + "/"
                linkname = name + "/"
            if os.path.islink(fullname):
                displayname = name + "@"
                # Note: a link to a directory displays with @ and links with /
            f.write(bytes('<li><a href="%s">%s</a>\n' % (linkname, displayname),
                'UTF-8'))
        f.write(bytes("</ul>\n<hr>\n", 'UTF-8'))
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        return f

    def translate_path(self, path):
        """Translate a /-separated PATH to the local filename syntax.

        Components that mean special things to the local file system
        (e.g. drive or directory names) are ignored.  (XXX They should
        probably be diagnosed.)

        """
        path = posixpath.normpath(urllib.parse.unquote(path))
        words = path.split('/')
        words = filter(None, words)
        path = web_root
        for word in words:
            drive, word = os.path.splitdrive(word)
            head, word = os.path.split(word)
            if word in (os.curdir, os.pardir): continue
            path = os.path.join(path, word)
        return path

    def copyfile(self, source, outputfile):
        """Copy all data between two file objects.

        The SOURCE argument is a file object open for reading
        (or anything with a read() method) and the DESTINATION
        argument is a file object open for writing (or
        anything with a write() method).

        The only reason for overriding this would be to change
        the block size or perhaps to replace newlines by CRLF
        -- note however that this the default server uses this
        to copy binary data as well.

        """
        shutil.copyfileobj(source, outputfile)

    def guess_type(self, path):
        """Guess the type of a file.

        Argument is a PATH (a filename).

        Return value is a string of the form type/subtype,
        usable for a MIME Content-type header.

        The default implementation looks the file's extension
        up in the table self.extensions_map, using text/plain
        as a default; however it would be permissible (if
        slow) to look inside the data to make a better guess.

        """

        base, ext = posixpath.splitext(path)
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        ext = ext.lower()
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        else:
            return self.extensions_map['']

    extensions_map = mimetypes.types_map.copy()
    extensions_map.update({
        '': 'application/octet-stream', # Default
        '.py': 'text/plain',
        '.c': 'text/plain',
        '.h': 'text/plain',
        })

    """Simple request handler for our default web interface"""
    def __init__(self, server_address, RequestHandlerClass, server):
        super(WebClientRequestHandler, self).__init__(server_address, RequestHandlerClass, server)

    def log_message(self, format, *args):
        if settings.verbose:
            super(WebClientRequestHandler, self).log_message(format, *args)

    def do_GET(self):
        """Handle HTTP GET requests"""

        # Simple redirects for the console page
        if self.path == "/console" or self.path == "/admin":
            self.path = "/console.html"

        # Simple redirects for the display
        if self.path == "/" or self.path == "/display" or self.path == "/":
            self.path = "/display.html"

        f = self.send_head()
        if f:
            self.copyfile(f, self.wfile)
            f.close()

class WebClientServer(object):
    """Simple HTTP server (manager?)"""
    def __init__(self):
        super(WebClientServer, self).__init__()
        self.port = settings.http_port
        self.address = settings.http_host

    def start(self):
        server_info = (self.address, self.port)
        addr = self.address
        if addr.strip() == "":
            addr = "0.0.0.0"
        self.httpd = HTTPServer(server_info, WebClientRequestHandler)
        print("Started web client (http) server on {1}:{0}".format(self.port, addr))
        if settings.verbose:
            print("    Visit http://localhost:{0}/console in your browser if it doesn't open automatically".format(self.port))
        self.httpd.serve_forever()

def is_valid_hostname(hostname):
    """Validate a hostname"""

    """ Credit: @tim-pietzcker of Stack Overflow
        http://stackoverflow.com/questions/2532053/validate-a-hostname-string """

    if len(hostname) > 255:
        return False
    if hostname[-1] == ".":
        hostname = hostname[:-1]
    allowed = re.compile("(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
    return all(allowed.match(x) for x in hostname.split("."))

