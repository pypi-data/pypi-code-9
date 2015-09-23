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
async def test_connect_35(engine):
    conn = await engine.connect()
    async with conn:
        pass
    assert conn._connection.closed


@pytest.mark.asyncio
async def test_insert_select_delete_35(engine):
    async with await engine.connect() as conn:
        metadata = MetaData()
        users = Table("users", metadata,
                      Column("id", Integer(), primary_key=True),
                      Column("name", String(20)),
                      Column("gender", String(1),
                             nullable=False, default="X"))

        await conn.execute(CreateTable(users))

        try:
            async with await conn.begin() as trans:
                await conn.execute(users.insert()
                                   .values(id=42, name="Async",))
            assert not trans._transaction.is_active

            res = await conn.execute(users.select()
                                     .where(users.c.id == 42))
            rows = await res.fetchall()
            assert len(rows) == 1
            assert rows[0].name == 'Async'
            assert rows[0].gender == 'X'

            res = await conn.execute(users.delete()
                                     .where(users.c.id == 42))
            assert res.rowcount == 1
        finally:
            await conn.execute(DropTable(users))
