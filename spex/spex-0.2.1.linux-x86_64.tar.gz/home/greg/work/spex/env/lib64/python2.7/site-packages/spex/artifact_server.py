import tornado.ioloop

import tornado.web
import tornado.netutil
import tornado.httpserver
import threading
from os import path
import socket

from .utils import ArtifactResolver


# pylint: disable=attribute-defined-outside-init,too-many-instance-attributes
class ArtifactServer(object):

    def __init__(self, root_dir, port=0):
        """Create a new artifact server

        Parameters
        ----------
        root_dir : str
            Root directory from which to serve files
        port : int, optional
            The port to listen on, may be randomly choosen
        """
        self.root_dir = path.realpath(root_dir)
        # TODO - One day our DC will be pure IPv6 and this will need to change
        self.sockets = tornado.netutil.bind_sockets(port, family=socket.AF_INET)
        self.is_running = False
        self._running = threading.Lock()

        self.thread = threading.Thread(name='artifact-server-thread', target=self._run)
        self.thread.setDaemon(True)

    def _run(self):
        self.ioloop = tornado.ioloop.IOLoop()
        self.app = tornado.web.Application([
            (r'/artifact/(.*)', tornado.web.StaticFileHandler, dict(path=self.root_dir))
        ])
        self.server = tornado.httpserver.HTTPServer(self.app)
        self.server.add_sockets(self.sockets)
        if self._running.acquire(False):
            self.is_running = True
            self._check_done = tornado.ioloop.PeriodicCallback(self._finished, 100, io_loop=self.ioloop)
            self._check_done.start()
            self.ioloop.start()
        else:
            raise ValueError('Tried to start an artifact server that is already running ?')

    def _finished(self):
        if self._running.acquire(False):
            self.ioloop.stop()
            self.is_running = False

    @property
    def base_uri(self):
        port = self.sockets[0].getsockname()[1]
        hostname = socket.gethostname()
        return 'http://%s:%d/artifact' % (hostname, port)

    def artifact_uri_resolver(self):
        """Return an object that is able to resovle files to the artifact server

        Returns
        -------
        artifact_resolver: callable
            Callable that can be used to resolve artifacts
        """
        return ArtifactResolver(self.base_uri + '/%s')

    def __str__(self):
        return 'ArtifactServer {dir=%s, base_uri=%s}' % (self.root_dir, self.base_uri)

    def __enter__(self):
        self.thread.start()
        return self

    def __exit__(self, _exc_type, _exc_val, _exc_tb):
        if self.is_running:
            self._running.release()
            self.thread.join()
