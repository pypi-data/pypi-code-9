# -*- coding: utf-8 -*-
# :Progetto:  arstecnica.sqlalchemy.async
# :Creato:    ven 10 lug 2015 00:20:18 CEST
# :Autore:    Alberto Berti <alberto@metapensiero.it>
# :Licenza:   GNU General Public License version 3 or later
#

import asyncio
import functools

import sqlalchemy as sa
from sqlalchemy.engine.base import Engine
from sqlalchemy.engine.strategies import DefaultEngineStrategy

AIO_STRATEGY = "_aio"


def create_engine(url, **kwargs):
    """Wrap SA ``create_engine()`` to inject our strategy."""

    kwargs['strategy'] = AIO_STRATEGY
    return sa.create_engine(url, **kwargs)


@sa.log.class_logger
class AIOEngine(object):
    """Asyncio wrapper around SA Engine."""

    def __init__(self, pool, dialect, url, echo=False,
                 loop=None, executor=None, **kwargs):
        if loop is None:
            raise ValueError('You must supply an event loop')

        self._loop = loop
        self._engine = Engine(pool, dialect, url, echo=echo, **kwargs)
        self._executor = executor

    @asyncio.coroutine
    def _run_in_executor(self, f, *args, **kwargs):
        if kwargs:
            f = functools.partial(f, **kwargs)
        return (yield from self._loop.run_in_executor(
            self._executor, f, *args))

    @property
    def dialect(self):
        return self._engine.dialect

    @property
    def _has_events(self):
        return self._engine._has_events

    @property
    def _execution_options(self):
        return self._engine._execution_options

    def _should_log_info(self):
        return self._engine._should_log_info()

    @asyncio.coroutine
    def connect(self):
        conn = yield from self._run_in_executor(self._engine.connect)
        return AIOConnection(conn, self)

    @asyncio.coroutine
    def execute(self, *args, **kwargs):
        result = yield from self._run_in_executor(
            self._engine.execute, *args, **kwargs)
        return AIOResultProxy(result, self)

    @asyncio.coroutine
    def has_table(self, table_name, schema=None):
        return self._run_in_executor(self._engine.has_table,
                                     table_name, schema)

    @asyncio.coroutine
    def table_names(self, schema=None, connection=None):
        if connection is not None:
            connection = connection._connection
        return (yield from self._run_in_executor(
            self._engine.table_names, schema, connection))


class AIOConnection(object):
    """Asyncio wrapper around a SA Connection."""

    def __init__(self, connection, engine):
        self._connection = connection
        self._engine = engine

    @asyncio.coroutine
    def execute(self, *args, **kwargs):
        result = yield from self._engine._run_in_executor(
            self._connection.execute, *args, **kwargs)
        return AIOResultProxy(result, self._engine)

    @asyncio.coroutine
    def close(self):
        return (yield from self._engine._run_in_executor(
            self._connection.close))

    @property
    def closed(self):
        return self._connection.closed

    @asyncio.coroutine
    def begin(self, *args, **kwargs):
        tran = yield from self._engine._run_in_executor(
            self._connection.begin, *args, **kwargs)
        return AIOTransaction(tran, self._engine)

    @asyncio.coroutine
    def execution_options(self, **kwargs):
        return (yield from self._engine._run_in_executor(
            self._connection.execution_options, **kwargs))

    def in_transaction(self):
        return self._connection.in_transaction()

    # Looking forward to use Python 3.5 new __aenter__ and __aexit__
    # to properly implement the async aware context manager...
    # For now, simply break the contract and immediately close the
    # connection.

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self._connection.close()


class AIOTransaction(object):
    """Asyncio wrapper around a SA Transaction."""

    def __init__(self, transaction, engine):
        self._transaction = transaction
        self._engine = engine

    @asyncio.coroutine
    def commit(self):
        return (yield from self._engine._run_in_executor(
            self._transaction.commit))

    @asyncio.coroutine
    def rollback(self):
        return (yield from self._engine._run_in_executor(
            self._transaction.rollback))

    @asyncio.coroutine
    def close(self):
        return (yield from self._engine._run_in_executor(
            self._transaction.close))

    # Looking forward to use Python 3.5 new __aenter__ and __aexit__
    # to properly implement the async aware context manager...
    # For now, simply break the contract and mimic SA blocking
    # behaviour.

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        transaction = self._transaction
        if type is None and transaction.is_active:
            try:
                transaction.commit()
            except:
                transaction.rollback()
        else:
            transaction.rollback()


class AIOResultProxy(object):
    """Asyncio wrapper around a SA ResultProxy."""

    def __init__(self, result_proxy, engine):
        self._result_proxy = result_proxy
        self._engine = engine

    @asyncio.coroutine
    def fetchone(self):
        return (yield from self._engine._run_in_executor(
            self._result_proxy.fetchone))

    @asyncio.coroutine
    def fetchall(self):
        return (yield from self._engine._run_in_executor(
            self._result_proxy.fetchall))

    @asyncio.coroutine
    def scalar(self):
        return (yield from self._engine._run_in_executor(
            self._result_proxy.scalar))

    @asyncio.coroutine
    def first(self):
        return (yield from self._engine._run_in_executor(
            self._result_proxy.first))

    @asyncio.coroutine
    def keys(self):
        return (yield from self._engine._run_in_executor(
            self._result_proxy.keys))

    @property
    def returns_rows(self):
        return self._result_proxy.returns_rows

    @property
    def rowcount(self):
        return self._result_proxy.rowcount

    @property
    def inserted_primary_key(self):
        return self._result_proxy.inserted_primary_key


class AIOEngineStrategy(DefaultEngineStrategy):
    """An EngineStrategy for use with AsyncIO."""

    name = AIO_STRATEGY
    engine_cls = AIOEngine

AIOEngineStrategy()
