import asyncio
import logging
import sqlalchemy as sa
from aiopg.sa import create_engine
from sqlalchemy.schema import CreateTable
from sqlalchemy.exc import ProgrammingError

from aiohttp_ac_hipchat.store import AbstractStore

log = logging.getLogger(__name__)

def create_postgre_store(dsn, table_name="clients", loop=None):
    log.info(loop == None)
    if loop == None:
        loop = asyncio.get_event_loop()

    store = loop.run_until_complete(init_postgre(dsn, table_name))
    return store

@asyncio.coroutine
def init_postgre(dsn, table_name):        
    engine = yield from create_engine(dsn)
    store = PostgreStore(engine, table_name)
    store.init_table()
    return store

    
class PostgreStore(AbstractStore):

    def __init__(self, postgres, table_name="clients"):
        super().__init__()

        # expected this to be a aiopg.sa.engine
        self.postgres = postgres
        self.table_name = table_name

        metadata = sa.MetaData()
        self.table = sa.Table(self.table_name, metadata,
            sa.Column('id', sa.String, primary_key=True),
            sa.Column('token_url', sa.String),
            sa.Column('group_name', sa.String),
            sa.Column('room_id', sa.Integer),
            sa.Column('capabilities_url', sa.String),
            sa.Column('homepage', sa.String),
            sa.Column('secret', sa.String),
            sa.Column('group_id', sa.Integer))

    @asyncio.coroutine
    def init_table(self):
        log.info("init_table")
        try:
            with (yield from self.postgres) as connection:
                loop = asyncio.get_event_loop()
                tasks = asyncio.gather(*connection.execute(CreateTable(self.table)))
                loop.run_until_complete(tasks)
        except ProgrammingError as ex:
            log.info("Error: %s" % ex)


    @asyncio.coroutine
    def set(self, key, value, client_id):
        assert value is not None
        assert client_id is not None
        value["id"] = client_id
        yield from self.delete(key, client_id)
        with (yield from self.postgres) as conn:
            log.info("inserting %s" % client_id)
            yield from conn.execute(self.table.insert(), value)


    @asyncio.coroutine
    def get(self, key, client_id):
        log.info("get client_id %s" % client_id)

        assert client_id is not None
        with (yield from self.postgres) as conn:
            result = yield from conn.execute(
                self.table.select().where(self.table.c.id == client_id))
            client = yield from result.fetchone()

            if client:
                log.info("found client_id %s" % client_id)
                return dict(
                    id=client.id,
                    token_url=client.token_url,
                    group_name=client.group_name,
                    room_id=client.room_id,
                    capabilities_url=client.capabilities_url,
                    homepage=client.homepage,
                    secret=client.secret,
                    group_id=client.group_id)
            else:
                log.info("didn't find client_id %s" % client_id)
                return None

    @asyncio.coroutine
    def delete(self, key, client_id):
        assert client_id is not None
        with (yield from self.postgres) as conn:
            yield from conn.execute(
                self.table.delete().where(self.table.c.id == client_id))
