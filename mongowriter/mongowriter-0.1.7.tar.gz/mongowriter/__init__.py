"""Inserts documents passed through a queue into a mongo db. The queue
must contain tuples of (collection_name, document) that can be
directly inserted in mongo."""

import logging
import random
import socket
from Queue import Empty
from collections import defaultdict
from threading import Thread, current_thread
from time import sleep, time


from pymongo import MongoClient
from pymongo.errors import AutoReconnect, ConnectionFailure, OperationFailure

logger = logging.getLogger(__name__)


def retry_on_exception(retries, exc, pause):
    def retry_on_exception_decorator(func):
        def wrapped(*fargs, **fkwargs):
            for _ in xrange(retries):
                try:
                    return func(*fargs, **fkwargs)
                except exc:
                    sleep(pause)
            else:
                return func(*fargs, **fkwargs)
        return wrapped
    return retry_on_exception_decorator


# replica set might be changing primary
@retry_on_exception(
    retries=14,
    exc=(ConnectionFailure, OperationFailure, socket.timeout),
    pause=5)
def init_client(**client_kwargs):
    return MongoClient(**client_kwargs)


@retry_on_exception(
    retries=14,
    exc=(ConnectionFailure, OperationFailure, socket.timeout),
    pause=5)
def authenticate_db(client, dbname, username, password):
    db = client[dbname]
    db.authenticate(username, password)
    return db


class MongoWriter(object):
    def __init__(self, queue, dbname, username, password=None, num_workers=10,
                 max_reorder=0, manipulate=True, **client_kwargs):
        self.stopping = False
        self.queue = queue
        self.manipulate = manipulate
        self.max_reorder = max_reorder

        client_kwargs.setdefault('maxPoolSize', num_workers)
        client_kwargs.setdefault('socketTimeoutMS', 5000)

        self.client = init_client(**client_kwargs)
        self.db = authenticate_db(self.client, dbname, username, password)

        self.num_workers = num_workers
        self.workers = []

    def start(self):
        assert not len(self.workers)
        self.workers = [
            Thread(target=self.run)
            for _ in xrange(self.num_workers)]
        for w in self.workers:
            w.daemon = True
            w.start()

    def _do_stop(self):
        if not self.stopping:
            return False
        return self.queue.empty() or time() > self.stopping

    def get_stats(self):
        return dict(
            inserted=sum(getattr(w, 'inserted', 0) for w in self.workers),
            failed=sum(getattr(w, 'failed', 0) for w in self.workers),
        )

    def stop(self):
        self.stopping = time() + 5
        self.workers = []

    def run(self):
        current_thread().inserted = 0
        current_thread().failed = 0
        while not self._do_stop():
            collections = defaultdict(list)

            try:
                collection, document = self.queue.get(timeout=5)
                collections[collection].append(document)
                for _ in range(self.max_reorder):
                    collection, document = self.queue.get(block=False)
                    collections[collection].append(document)
            except Empty:
                pass
            finally:
                for collection, documents in collections.items():
                    try:
                        self._insert_lines(collection, documents)
                        current_thread().inserted += len(documents)
                    except Exception as e:
                        logger.error(
                             'unknown exception ignored while inserting data: %r',  # noqa
                             e,
                             exc_info=1)
                        current_thread().failed += len(documents)
                    finally:
                        for _ in documents:
                            self.queue.task_done()

    def _insert_lines(self, collection, data):
        while not self.queue.full():
            try:
                # if data is a list, Mongo will automatically do a bulk insert
                self.db[collection].insert(data, manipulate=self.manipulate)
                return
            except AutoReconnect:
                sleep(random.uniform(0.2, 1.0))
        logger.warning('Overloaded; dropping data %s', data)
        current_thread().failed += len(data)
