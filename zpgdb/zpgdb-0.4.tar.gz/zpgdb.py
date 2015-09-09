# -*- coding: utf-8 -*-

"""This module provides a thin wrapper to access a PostgreSQL database,
with functions to create a connection per thread, context managers to
wrap transactions, dealing with disconnects, etc"""

import logging
import threading

from contextlib import contextmanager
from time import sleep

import psycopg2
import psycopg2.extras

log = logging.getLogger(__name__)
logFormat = logging.Formatter(
    fmt='%(asctime)s.%(msecs)03d %(levelname).3s | %(name)s | %(message)s',
    datefmt='%Y/%m/%d %H:%M:%S')
log.setLevel(logging.WARNING)
logHandler = logging.StreamHandler()
logHandler.setFormatter(logFormat)
log.addHandler(logHandler)

#log.setLevel(logging.DEBUG)

__VERSION__ = '0.4'
__AUTHOR__ = 'Antonio Zanardo <zanardo@gmail.com>'

_HOST = _PORT = _DB = _USER = _PASS = None

_local = threading.local()

def config_connection(host, port, user, password, database):
    log.debug("configuring connection:")
    log.debug("  host = %s", host)
    log.debug("  port = %d", port)
    log.debug("  user = %s", user)
    log.debug("  db   = %s", database)
    global _HOST, _PORT, _USER, _PASS, _DB
    _HOST = host
    _PORT = port
    _USER = user
    _PASS = password
    _DB = database

def getdb():
    if not hasattr(_local, 'dbh'):
        log.debug("opening a new database connection")
        _local.dbh = psycopg2.connect(host=_HOST, port=_PORT,
            database=_DB, user=_USER, password=_PASS,
            cursor_factory=psycopg2.extras.DictCursor)
        _local.trans = 0
    else:
        log.debug("reusing database connection %s", id(_local.dbh))
    return _local.dbh

def deldbh():
    if hasattr(_local, 'dbh'):
        log.debug("forcing disconnection of %s", id(_local.dbh))
        try:
            _local.dbh.close()
        except psycopg2.Error:
            pass
        del _local.dbh

@contextmanager
def trans():
    log.debug("starting new trans() context")

    if not hasattr(_local, 'trans'):
        _local.trans = 0

    if _local.trans == 0:
        # Checking if connection to database is alive. We will reconnect in
        # case the connection was lost. This will add latency but can deal
        # with persistent connection problems after PostgreSQL is restarted.
        tries = 0
        while True:
            try:
                log.debug("checking if database connection is alive")
                dbh = getdb()
                c = dbh.cursor()
                c.execute('select 1')
                c.fetchone()
            except psycopg2.Error:
                log.debug("database connection is lost")
                log.exception("exception: ")
                deldbh()
                tries += 1
            else:
                break

            if tries > 10:
                log.debug("aborting reconnection atempt")
                break
            else:
                log.debug("sleeping for 1 second before trying to reconnect")
                sleep(1)

    _local.trans += 1
    log.debug("open transactions: %d", _local.trans)

    # Wrapping a transaction.
    try:
        log.debug("entering user context")
        dbh = getdb()
        c = dbh.cursor()
        yield c
        log.debug("returning from user context")
    except:
        log.debug("exception caught, lets rollback")
        try:
            dbh.rollback()
            dbh.close()
        except psycopg2.Error:
            log.debug("error trying to rollback")
            pass
        deldbh()
        raise
    else:
        _local.trans -= 1
        if _local.trans == 0:
            dbh.commit()
            log.debug("commiting")
