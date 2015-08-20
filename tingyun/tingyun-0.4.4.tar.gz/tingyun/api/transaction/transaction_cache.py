
import logging
import sys
import threading
import weakref
import thread


_logger = logging.getLogger(__name__)


class TransactionCache(object):
    """
    """
    def __init__(self):
        self._cache = weakref.WeakValueDictionary()
        _logger.debug("init transaction cache with thread %s", thread.get_ident())

    def current_thread_id(self):
        """get the current thread id
        :return: thread id
        """
        greenlet = sys.modules.get('greenlet')

        if greenlet:
            # Compatible greenlet frame
            current = greenlet.getcurrent()
            if current is not None and current.parent:
                return id(current)

        return thread.get_ident()

    def save_transaction(self, transaction):
        """
        :param transaction:
        :return:
        """
        if transaction.thread_id in self._cache:
            raise RuntimeError("transaction already exist.")

        self._cache[transaction.thread_id] = transaction

    def get_active_threads(self):
        """
        """
        for thread_id, frame in sys._current_frames().items():
            transaction = self._cache.get(thread_id)
            if transaction is not None:
                if transaction.background_task:
                    yield transaction, thread_id, 'Background', frame
                else:
                    yield transaction, thread_id, 'Web', frame
            else:
                active_thread = threading._active.get(thread_id)
                if active_thread is not None and active_thread.getName().startswith('TingYun-'):
                    yield None, thread_id, 'Agent', frame
                else:
                    yield None, thread_id, 'Other', frame

    def drop_transaction(self, transaction):
        """
        """
        thread_id = transaction.thread_id

        if thread_id not in self._cache:
            RuntimeError('no active transaction')

        current = self._cache.get(thread_id, None)
        if transaction != current:
            raise RuntimeError('not the current transaction')

        del self._cache[thread_id]

    def current_transaction(self):
        """Return the transaction object if one exists for the currently executing thread.
        """
        thread_id = self.current_thread_id()
        
        return self._cache.get(thread_id, None)

_transaction_cache = TransactionCache()


def transaction_cache():
    """
    """
    return _transaction_cache