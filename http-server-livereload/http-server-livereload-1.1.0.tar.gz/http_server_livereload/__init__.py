# *-* coding: utf-8 *-*
# Copyright (c) 2015 Mounier Florian

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
try:
    from http.server import HTTPServer
    from urllib.request import urlopen
except ImportError:
    from BaseHTTPServer import HTTPServer
    from urllib import urlopen

from functools import wraps
import os.path


def patch(lr_host='localhost', lr_port=35729, files=None):
    """
    Patch the server_forever method of http.server to make a
    livereload call at the very last moment before starting serve.
    """

    # Save the original serve_forever method
    old_serve_forever = HTTPServer.serve_forever

    @wraps(old_serve_forever)
    def new_serve_forever(self):
        """This is the patched server_forever method"""

        try:
            # Make a tiny-lr compatible request
            urlopen('http://%s:%d/changed?files=%s' % (
                lr_host, lr_port, ','.join(files or '/',)
            ))
        except Exception:
            # Do nothing if it does not work
            pass

        # Call the original serve_forever
        old_serve_forever(self)

    # Patch the method
    HTTPServer.serve_forever = new_serve_forever


def patch_werkzeug_reloader(filter_=None):
    """
    Patch the WatchdogReloaderLoop of werkzeug to add an exclude filter
    Preventing reload on emacs lock files for example.

    The filter_ attribute takes the file absolute path and the file name
    as parameters. It must be a function that returns true if the file
    must NOT be taken in account.
    Defaults to excluding files starting with '.#'
    """
    try:
        import watchdog
    except ImportError:
        print('You must have watchdog installed to use this patch')
        return

    from werkzeug._reloader import reloader_loops, WatchdogReloaderLoop
    default_filter = lambda abspath, fn: fn.startswith('.#')


    class FilteredWatchdogReloaderLoop(WatchdogReloaderLoop):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            this = self

            class _BetterHandler(self.event_handler.__class__):

                def on_created(self, event):
                    if not this.is_excluded(event.src_path):
                        super(_BetterHandler, self).on_created(event)

                def on_modified(self, event):
                    if not this.is_excluded(event.src_path):
                        super(_BetterHandler, self).on_modified(event)

                def on_moved(self, event):
                    if (not this.is_excluded(event.src_path) and
                            not this.is_excluded(event.dest_path)):
                        super(_BetterHandler, self).on_moved(event)

                def on_deleted(self, event):
                    if not this.is_excluded(event.src_path):
                        super(_BetterHandler, self).on_deleted(event)

            self.event_handler = _BetterHandler()

        def is_excluded(self, fn):
            return (filter_ or default_filter)(fn, os.path.basename(fn))

    if reloader_loops['auto'] == reloader_loops['watchdog']:
        reloader_loops['auto'] = FilteredWatchdogReloaderLoop
    reloader_loops['watchdog'] = FilteredWatchdogReloaderLoop
