# -*- coding: utf-8 -*-
# :Progetto:  metapensiero.sqlalchemy.proxy -- Async tests
# :Creato:    ven 10 lug 2015 20:29:12 CEST
# :Autore:    Lele Gaifax <lele@metapensiero.it>
# :Licenza:   GNU General Public License version 3 or later
#

import asyncio

from sqlalchemy import (Column, Integer, MetaData, String, Table, select)
from sqlalchemy.schema import CreateTable, DropTable

from nose.tools import assert_equal, assert_greater, assert_in, assert_not_in

from metapensiero.sqlalchemy.proxy.async import AsyncProxiedQuery

from arstecnica.sqlalchemy.async import create_engine
from arstecnica.sqlalchemy.async.tests import AsyncTestBase


class TestAsync(AsyncTestBase):
    def test_async_proxied_query(self):
        @asyncio.coroutine
        def go():
            conn = yield from self.connect()
            yield from conn.execution_options(autocommit=True)

            metadata = MetaData()
            persons = Table('persons', metadata,
                            Column('id', Integer, primary_key=True),
                            Column('firstname', String),
                            Column('lastname', String,
                                   info={ 'label': "Last name",
                                          'hint': "This is the person's family name." }),
                            )

            yield from conn.execute(CreateTable(persons))

            yield from conn.execute(persons.insert().values(id=42,
                                                            firstname="Level",
                                                            lastname="Fortytwo"))
            yield from conn.execute(persons.insert().values(id=451,
                                                            firstname="Fahrenheit",
                                                            lastname="Fourhundredfiftyone"))

            proxy = AsyncProxiedQuery(persons.select(), loop=self.loop)

            result = yield from proxy(conn)
            assert len(result) == 2
            assert 42 in [r['id'] for r in result]

            result = yield from proxy(conn, limit=1, asdict=True)
            assert len(result) == 1
            assert 'id' in result[0]

            result = yield from proxy(conn, result='rows', count='count')
            assert result['message'] == 'Ok'
            assert len(result['rows']) == result['count']

            result = yield from proxy(conn, result=False, metadata='metadata')
            assert result['metadata']['primary_key'] == 'id'
            for finfo in result['metadata']['fields']:
                if finfo['name'] == 'lastname':
                    assert finfo['label'] == 'Last name'
                    break
            else:
                assert False, "Metadata about 'lastname' is missing!"

            result = yield from proxy(conn, sort='[{"property":"lastname","direction":"DESC"}]')
            assert len(result) == 2
            assert 451 == result[0]['id']

            result = yield from proxy(conn, sort=[{"property":"lastname","direction":"ASC"}])
            assert len(result) == 2
            assert 42 == result[0]['id']

            result = yield from proxy(conn, filters=[dict(property='firstname',
                                                          value="Level",
                                                          operator="=")])
            assert len(result) == 1
            assert 42 == result[0]['id']

            yield from conn.execute(DropTable(persons))

        self.loop.run_until_complete(go())
