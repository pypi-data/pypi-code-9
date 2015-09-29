import asyncio
from abc import abstractmethod, ABC


class AbstractStore(ABC):

    @abstractmethod
    @asyncio.coroutine
    def get(self, key, client_id):
        pass

    @abstractmethod
    @asyncio.coroutine
    def set(self, key, value, client_id):
        pass

    @abstractmethod
    @asyncio.coroutine
    def delete(self, key, client_id):
        pass


class MongoDBStore(AbstractStore):

    def __init__(self, mongodb, table_name="clients"):
        super().__init__()
        self.mongodb = mongodb
        self.table_name = table_name

    @asyncio.coroutine
    def set(self, key, value, client_id):
        clients = self.mongodb.default_database[self.table_name]
        yield from clients.remove(self.id_query(client_id))
        yield from clients.insert(value)

    @asyncio.coroutine
    def get(self, key, client_id):
        clients = self.mongodb.default_database[self.table_name]
        return (yield from clients.find_one(self.id_query(client_id)))

    @asyncio.coroutine
    def delete(self, key, client_id):
        clients = self.mongodb.default_database[self.table_name]
        yield from clients.remove(self.id_query(client_id))

    @staticmethod
    def id_query(client_id):
        return {"id": client_id}

