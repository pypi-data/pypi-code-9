# -*- coding: utf-8 -*-
import inspect
import psutil
from os import getpid
import re
import time
import zope.component
import ZODB.interfaces
from Zope2 import app as App
from zc.z3monitor.interfaces import IZ3MonitorPlugin
from cStringIO import StringIO

from Products.ZNagios import get_refcount, get_conflictInfo, get_activity


def zc_uptime(connection):
    """uptime of the zope instance in seconds"""
    app = App()
    elapsed = time.time() - app.Control_Panel.process_start
    print >> connection, elapsed
    app._p_jar.close()


def zc_dbsize(connection, database='main'):
    """size of the database (default=main) in bytes"""
    app = App()
    db = app.Control_Panel.Database[database]
    print >> connection, db._p_jar.db().getSize()


def zc_objectcount(connection, database='main'):
    """number of object in the database (default=main)"""
    db = zope.component.getUtility(ZODB.interfaces.IDatabase, database)
    print >> connection, db.objectCount()


def zc_refcount(connection):
    """the total amount of object reference counts"""
    app = App()
    print >> connection, get_refcount(app)
    app._p_jar.close()


def zc_errorcount(connection, objectId=None):
    """number of error present in error_log (default in the root).

    You can also provide the objectId of the object that contains another error_log
    """
    app = App()
    if objectId is not None:
        app = getattr(app, objectId)
    print >> connection, len(app.error_log._getLog())
    app._p_jar.close()


def zc_conflictcount(connection):
    """number of all conflict errors since startup"""
    print >> connection, get_conflictInfo().conflict_errors


def zc_unresolved_conflictcount(connection):
    """number of all unresolved conflict errors since startup"""
    print >> connection, get_conflictInfo().unresolved_conflict_errors


def zc_dbactivity(connection, database='main', last_minutes=60 * 5):
    """number of load, store and connections on database (default=main) for the last x minutes (default=5)"""
    app = App()
    db = app.Control_Panel.Database[database]
    activity = get_activity(db)
    print >> connection, activity['total_load_count'], " ", activity['total_store_count'], " ", activity['total_connections']
    app._p_jar.close()


def zc_requestqueue_size(connection):
    """number of requests waiting in the queue to be handled by zope threads"""
    from ZServer.PubCore import _handle
    queue_size = 0
    if _handle is not None:  # no request yet
        zrendevous = _handle.im_self
        queue_size = len(zrendevous._lists[1])
    print >> connection, queue_size


def zc_memory_percent(connection):
    pid = getpid()
    p = psutil.Process(pid)
    print >> connection, p.memory_percent()


def zc_cpu_times(connection):
    pid = getpid()
    p = psutil.Process(pid)
    cpu_times = p.cpu_times()
    print >> connection, cpu_times.user, cpu_times.system


GAUGE_RETURNS = {'cpu_times': ['user', 'system'],
                 'dbactivity': ['load_count', 'store_count', 'total_connections']}


def return_values(stream, prefix):
    values = re.split(' +', stream.getvalue().strip())
    return dict(zip(GAUGE_RETURNS.get(prefix, ['']), values))


def beautify_return_values(connection, tempStream, name, dbname=None):
    values = return_values(tempStream, name)
    if dbname is not None:
        prefix = '%s.%s' % (dbname, name)
    else:
        prefix = name
    for probe_detail, value in values.items():
        if len(values) > 1:
            print >> connection, str("%s.%s : %s" % (prefix, probe_detail, value))
        else:
            print >> connection, str("%s : %s" % (prefix, value))


def stats(connection):
    app = App()
    dbs = app.Control_Panel.Database.getDatabaseNames()
    dbs.remove('temporary')
    for name, probe in zope.component.getUtilitiesFor(IZ3MonitorPlugin):
        if name in ['help', 'stats']:
            continue
        argspec = inspect.getargspec(probe)
        if 'database' in argspec.args:
            for dbname in dbs:
                try:
                    tempStream = StringIO()
                    probe(tempStream, dbname)
                    beautify_return_values(connection, tempStream, name, dbname)
                except:
                    pass
        elif 'connection' in argspec.args:
            tempStream = StringIO()
            probe(tempStream)
            beautify_return_values(connection, tempStream, name)
