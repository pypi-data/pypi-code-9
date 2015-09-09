# -*- coding: utf-8 -*-
# :Progetto:  raccoon.frontend -- async tests
# :Creato:    ven 10 lug 2015 13:01:56 CEST
# :Autore:    Lele Gaifax <lele@metapensiero.it>
# :Licenza:   GNU General Public License version 3 or later
#

import pytest

from sqlalchemy import MetaData, Table, Column, Integer, String
from sqlalchemy.schema import CreateTable, DropTable


db_url = 'mysql+pymysql://localhost/test'


@pytest.mark.asyncio
def test_connect(engine):
    conn = yield from engine.connect()
    with conn:
        pass
    assert conn._connection.closed


@pytest.mark.asyncio
def test_insert_select_delete(engine):
    with (yield from engine.connect()) as conn:
        metadata = MetaData()
        users = Table("users", metadata,
                      Column("id", Integer(), primary_key=True),
                      Column("name", String(20)),
                      Column("gender", String(1),
                             nullable=False, default="X"))

        yield from conn.execute(CreateTable(users))

        try:
            with (yield from conn.begin()) as trans:
                yield from conn.execute(users.insert()
                                        .values(id=42, name="Async",))
            assert not trans._transaction.is_active

            res = yield from conn.execute(users.select()
                                          .where(users.c.id == 42))
            rows = yield from res.fetchall()
            assert len(rows) == 1
            assert rows[0].name == 'Async'
            assert rows[0].gender == 'X'

            res = yield from conn.execute(users.delete()
                                          .where(users.c.id == 42))
            assert res.rowcount == 1
        finally:
            yield from conn.execute(DropTable(users))
