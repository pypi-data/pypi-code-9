### -*- coding: utf-8 -*- ####################################################
##############################################################################
#
# Copyright (c) 2008-2009 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################


import logging
logger = logging.getLogger('ZTFY (SQLAlchemy)')

from datetime import datetime
from persistent import Persistent
from persistent.dict import PersistentDict
import sqlalchemy
from sqlalchemy.event import listen
from sqlalchemy.orm import scoped_session, sessionmaker, class_mapper
from sqlalchemy.pool import Pool
from threading import Thread, Lock
import time

# import Zope3 interfaces
from zope.security.interfaces import NoInteraction

# import local interfaces
from ztfy.alchemy.interfaces import IAlchemyEngineUtility, REQUEST_SESSION_KEY

# import Zope3 packages
from zope.container.contained import Contained
from zope.interface import implements
from zope.component import getUtility
from zope.schema.fieldproperty import FieldProperty

# import local packages
from ztfy.alchemy.datamanager import ZopeTransactionExtension, join_transaction, \
                                     _SESSION_STATE, STATUS_ACTIVE, STATUS_READONLY
from ztfy.utils.request import getRequest, getRequestData, setRequestData


CONNECTIONS_TIMESTAMP = {}
CONNECTIONS_LOCK = Lock()


def handle_pool_checkout(connection, record, proxy):
    """Pool connection checkout

    Called when a connection is retrieved from the pool.
    If the connection record is already marked, we remove it from the mapping.
    """
    with CONNECTIONS_LOCK:
        if record in CONNECTIONS_TIMESTAMP:
            logger.debug("Removing timestamp for checked-out connection {0!r} ({1!r})".format(connection, record))
            del CONNECTIONS_TIMESTAMP[record]

listen(Pool, 'checkout', handle_pool_checkout)


def handle_pool_checkin(connection, record):
    """Pool connection checkin

    Called when a connection returns to the pool.
    We apply a timestamp on the connection record to be able to close it automatically
    after 5 minutes without being used.
    """
    with CONNECTIONS_LOCK:
        logger.debug("Setting inactivity timestamp for checked-in connection {0!r} ({1!r})".format(connection, record))
        CONNECTIONS_TIMESTAMP[record] = datetime.utcnow()

listen(Pool, 'checkin', handle_pool_checkin)


class ConnectionCleanerThread(Thread):
    """Background thread used to clean unused database connections

    Each connection is referenced in CONNECTION_TIMESTAMP on checkin and is invalidated
    if not being used after 5 minutes
    """
    timeout = 300

    def run(self):
        while True:
            now = datetime.utcnow()
            for connection, value in list(CONNECTIONS_TIMESTAMP.items()):
                delta = now - value
                if delta.total_seconds() > self.timeout:
                    logger.info("Invalidating unused connection {0!r} from pool".format(connection))
                    with CONNECTIONS_LOCK:
                        connection.invalidate()
                        del CONNECTIONS_TIMESTAMP[connection]
            time.sleep(60)

logger.info("Starting pool connections management thread")
cleaner_thread = ConnectionCleanerThread()
cleaner_thread.daemon = True
cleaner_thread.start()


class AlchemyEngineUtility(Persistent):
    """A persistent utility providing a database engine"""

    implements(IAlchemyEngineUtility)

    name = FieldProperty(IAlchemyEngineUtility['name'])
    dsn = FieldProperty(IAlchemyEngineUtility['dsn'])
    echo = FieldProperty(IAlchemyEngineUtility['echo'])
    pool_size = FieldProperty(IAlchemyEngineUtility['pool_size'])
    pool_recycle = FieldProperty(IAlchemyEngineUtility['pool_recycle'])
    register_geotypes = FieldProperty(IAlchemyEngineUtility['register_geotypes'])
    register_opengis = FieldProperty(IAlchemyEngineUtility['register_opengis'])
    encoding = FieldProperty(IAlchemyEngineUtility['encoding'])
    convert_unicode = FieldProperty(IAlchemyEngineUtility['convert_unicode'])

    def __init__(self, name=u'', dsn=u'', echo=False, pool_size=25, pool_recycle=-1,
                 register_geotypes=False, register_opengis=False, encoding='utf-8', convert_unicode=False, **kw):
        self.name = name
        self.dsn = dsn
        self.encoding = encoding
        self.convert_unicode = convert_unicode
        self.echo = echo
        self.pool_size = pool_size
        self.pool_recycle = pool_recycle
        self.register_geotypes = register_geotypes
        self.register_opengis = register_opengis
        self.kw = PersistentDict()
        self.kw.update(kw)

    def __setattr__(self, name, value):
        super(AlchemyEngineUtility, self).__setattr__(name, value)
        if (name != '_v_engine') and hasattr(self, '_v_engine'):
            delattr(self, '_v_engine')

    def getEngine(self):
        engine = getattr(self, '_v_engine', None)
        if engine is not None:
            return engine
        kw = {}
        kw.update(self.kw)
        self._v_engine = sqlalchemy.create_engine(str(self.dsn),
                                                  echo=self.echo,
                                                  pool_size=self.pool_size,
                                                  pool_recycle=self.pool_recycle,
                                                  encoding=self.encoding,
                                                  convert_unicode=self.convert_unicode,
                                                  strategy='threadlocal', **kw)
        if self.register_geotypes:
            try:
                import psycopg2
                import psycopg2.extensions as psycoext
                from GeoTypes import initialisePsycopgTypes
                url = self._v_engine.url
                initialisePsycopgTypes(psycopg_module=psycopg2,
                                       psycopg_extensions_module=psycoext,
                                       connect_string='host=%(host)s port=%(port)s dbname=%(dbname)s user=%(user)s password=%(password)s' % \
                                                      {'host': url.host,
                                                       'port': url.port,
                                                       'dbname': url.database,
                                                       'user': url.username,
                                                       'password': url.password},
                                       register_opengis_types=self.register_opengis)
            except:
                pass
        return self._v_engine

    def _resetEngine(self):
        engine = getattr(self, '_v_engine', None)
        if engine is not None:
            engine.dispose()
            self._v_engine = None


class PersistentAlchemyEngineUtility(AlchemyEngineUtility, Contained):
    """A persistent implementation of AlchemyEngineUtility stored into ZODB"""


def getEngine(engine):
    if isinstance(engine, (str, unicode)):
        engine = getUtility(IAlchemyEngineUtility, engine).getEngine()
    return engine


def getSession(engine, join=True, status=STATUS_ACTIVE, request=None, alias=None,
               twophase=True, use_zope_extension=True):
    """Get a new SQLAlchemy session
    
    Session is stored in request and in a sessions storage"""
    session = None
    if request is None:
        try:
            request = getRequest()
        except NoInteraction:
            pass
    if not alias:
        alias = engine
    if request is not None:
        session_data = getRequestData(REQUEST_SESSION_KEY, request, {})
        session = session_data.get(alias)
    if session is None:
        _engine = getEngine(engine)
        if use_zope_extension:
            factory = scoped_session(sessionmaker(bind=_engine, twophase=twophase,
                                                  extension=ZopeTransactionExtension()))
        else:
            factory = sessionmaker(bind=_engine, twophase=twophase)
        session = factory()
        if join:
            join_transaction(session, initial_state=status)
        if status != STATUS_READONLY:
            _SESSION_STATE[id(session)] = status
        if (request is not None) and (session is not None):
            session_data[alias] = session
            setRequestData(REQUEST_SESSION_KEY, session_data, request)
    return session


def getUserSession(engine, join=True, status=STATUS_ACTIVE, request=None, alias=None,
                   twophase=True, use_zope_extension=True):
    """Shortcut function to get user session"""
    if isinstance(engine, basestring):
        session = getSession(engine, join=join, status=status, request=request, alias=alias,
                             twophase=twophase, use_zope_extension=use_zope_extension)
    else:
        session = engine
    return session


class MetadataManager(object):
    """A manager for metadata management, to be able to use the same table name
    in different databases
    """

    def __init__(self):
        self.metadata = {}

    def getTable(self, engine, table, fallback):
        md = self.metadata.get(engine)
        if md and table in md.tables:
            return md.tables[table]
        if fallback and engine:
            md = self.metadata.get('')
        if md and table in md.tables:
            return md.tables[table]
        return None

    def __call__(self, engine=''):
        md = self.metadata.get(engine)
        if md is None:
            md = self.metadata[engine] = sqlalchemy.MetaData()
        return md

metadata = MetadataManager()


_tableToEngine = {}
_classToEngine = {}

def _assignTable(table, engine, session=None):
    _table = metadata.getTable(engine, table, True)
    util = getUtility(IAlchemyEngineUtility, name=engine)
    if session is None:
        session = getSession(engine)
    session.bind_table(_table, util.getEngine())


def assignTable(table, engine, immediate=True):
    _tableToEngine[table] = engine
    if immediate:
        _assignTable(table, engine)


def _assignClass(class_, engine, session=None):
    _mapper = class_mapper(class_)
    util = getUtility(IAlchemyEngineUtility, name=engine)
    if session is None:
        session = getSession(engine)
    session.bind_mapper(_mapper, util.getEngine())


def assignClass(class_, engine, immediate=True):
    _classToEngine[class_] = engine
    if immediate:
        _assignClass(class_, engine)
