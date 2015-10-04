import os
import socket
import sys
import thread
import time
import re
import logging

from sqlalchemy import event
from sqlalchemy.engine import url as _url

from . import client
from . import stats
from zkcluster import util

log = logging.getLogger(__name__)


class CMWrapper(object):
    @classmethod
    def get_dialect_cls(cls, url):
        new_url = _url.URL(re.sub(r'.connmon', '', url.drivername))

        addr = url.query.pop('connmon_addr', None)
        service = url.query.pop('connmon_service', None)
        config = url.query.pop('connmon_config', None)
        if addr:
            host, port = addr.split(':')
            url._connmon_info = {"host": host, "port": port, "config": config}
        elif service:
            url._connmon_info = {"service": service, "config": config}
        else:
            url._connmon_info = {"service": "default", "config": config}
        return new_url.get_dialect()

    @classmethod
    def engine_created(cls, engine):
        connect_info = engine.url._connmon_info
        ConnectionPoolAnalyzer(connect_info, engine)


class ConnectionPoolAnalyzer(object):

    def __init__(self, connect_info, engine):
        self.connect_info = connect_info
        self.async_suite = util.async_suite(green=False)
        self.lock = self.async_suite.lock()
        self.hostname = socket.gethostname()
        self.progname = sys.argv[0]
        self.ppid = os.getppid()
        self.pid = os.getpid()
        self.client = None

        event.listen(engine, "connect", self._connect_evt)
        event.listen(engine, "checkout", self._checkout_evt)
        event.listen(engine, "checkin", self._checkin_evt)
        event.listen(engine, "invalidate", self._invalidate_evt)
        event.listen(engine, "soft_invalidate", self._invalidate_evt)

        self._patch_pool(engine.pool)

    def _get_client(self):
        pid = os.getpid()

        if self.client is not None and pid == self.pid:
            return self.client

        with self.lock:
            if self.client is None or pid != self.pid:
                # adjust for new subprocess
                self.pid = pid
                self.client = client.StatsClient.from_connect_info(
                    self.connect_info,
                    self.hostname, self.progname, self.pid
                )
            return self.client

    def _connect_evt(self, dbapi_conn, connection_rec):
        self._send_evt(dbapi_conn, stats.CONNECT)

    def _checkout_evt(self, dbapi_conn, connection_rec, connection_proxy):
        self._send_evt(dbapi_conn, stats.CHECKOUT)

    def _checkin_evt(self, dbapi_conn, connection_rec):
        self._send_evt(dbapi_conn, stats.CHECKIN)

    def _invalidate_evt(self, dbapi_conn, connection_rec, exception):
        self._send_evt(dbapi_conn, stats.INVALIDATE)

    def _close_connection(self, dbapi_conn):
        self._pool_close_connection(dbapi_conn)
        self._send_evt(dbapi_conn, stats.CLOSE)

    def _send_evt(self, dbapi_conn, action):
        client = self._get_client()

        evt = stats.ConnectionEvent(
            self.hostname, self.progname, self.pid, self.ppid,
            thread.get_ident(), repr(dbapi_conn), time.time(), action
        )
        client.send(evt)

    def _recreate_pool(self):
        recreated = self._pool_recreate()
        self._patch_pool(recreated)
        return recreated

    def _patch_pool(self, pool):
        self._pool_close_connection = pool._close_connection
        self._pool_recreate = pool.recreate
        pool._close_connection = self._close_connection
        pool.recreate = self._recreate_pool

    def close(self):
        if self.client is not None:
            self.client.close()
            self.client = None

