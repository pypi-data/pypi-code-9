"""the module wrapt main entrance

"""

from tingyun.api.tracert.mongo_trace import wrap_mongo_trace
from tingyun.api.tracert.function_trace import wrap_function_trace
import logging

_logger = logging.getLogger(__name__)
_methods = ['save', 'insert', 'update', 'drop', 'reindex', 'index_information', 'count', 'create_index', 'ensure_index',
            'drop_indexes', 'drop_index', 'remove', 'find_one', 'find', 'options', 'group', 'rename', 'distinct',
            'map_reduce', 'inline_map_reduce', 'find_and_modify']


def detect_connection(module):
    """
    :param module:
    :return:
    """
    if hasattr(module, "Connection"):
        wrap_function_trace(module, 'Connection.__init__', name='%s:Connection.__init__' % module.__name__)


def detect_mongo_client(module):
    """
    :param module:
    :return:
    """
    if hasattr(module, "MongoClient"):
        wrap_function_trace(module, "MongoClient.__init__", name="%s.MongoClient.__init__" % module.__name__)


def detect_collection(module):
    """
    :param module:
    :return:
    """
    def collection_name(collection, *args, **kwargs):
        """ we get the full name include the database name with dot separated
        :param collection:
        :param args:
        :param kwargs:
        :return:
        """
        return collection.full_name

    if not hasattr(module, "Collection"):
        _logger.info("module(%s) has not Collection object.", module)
        return

    for m in _methods:
        if not hasattr(module.Collection, m):
            _logger.info("Collection has not %s method", m)
            continue

        wrap_mongo_trace(module, "Collection.%s" % m, schema=collection_name, method=m)
