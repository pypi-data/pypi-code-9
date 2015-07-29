# -*- encoding: utf-8 -*-
import six
import logging

from any2 import TypeTransformer
from any2 import recursive_getattr
from any2 import ColumnMappingError

log = logging.getLogger(__name__)


class Listlike2List(object):
    """an adapter that transforms an objet to list
    mainly useful for SQLAlchemy request results
    """

    def __init__(self, iterator, transformer=None):
        self.iterator = iterator
        if not transformer:
            transformer = TypeTransformer()

        self.transformer = transformer

    def __iter__(self):
        """sqlalchemy result proxies for sql expressions give dict like objects
        that also are iterable like lists... Unfortunately openpyxl needs
        instances of list or tuple... let's make it happy
        """
        transformer = self.transformer
        for row in self.iterator:
            yield [
                transformer.apply(item, index=i) for i, item in enumerate(row)
            ]


class DictAdapter(object):
    """An adapter that will make sure the provided object exposes
    attributes and methods that are useable by a DictWriter instance,
    basically adapting any python object to give it a dictionary signature.
    """

    def __init__(self, obj, column_mappings, encoding):
        """Initialize a CSVAddon
        @param obj: The object to be adapted.
        @type obj: any python object instance

        @param column_mappings:
        @type column_mappings: list of dictionary

        @param encoding: Encoding to use to encode all string values
        before serializing
        @type encoding: String
        """
        self.obj = obj
        self.column_mappings = column_mappings
        self.encoding = encoding

        self.__col_maps = dict()
        self.__init_column_maps()

    def __init_column_maps(self):
        for colmap in self.column_mappings:
            self.__col_maps[colmap['colname']] = colmap

    def __iter__(self):
        """Dictionary method needed by the DictWriter
        """
        for k in self.__col_maps.keys():
            yield k

    def keys(self):
        """Dictionary method needed by the DictWriter
        """
        return self.__col_maps.keys()

    def get(self, column_name, default_value):
        """Dictionary method needed by the DictWriter
        """
        column_mapping = self.__col_maps[column_name]
        attr = column_mapping.get('attr', None)
        renderer = column_mapping.get('renderer', None)

        if attr is not None:
            value = recursive_getattr(self.obj, attr, default_value)

        else:
            value = None

        if renderer is not None:
            if callable(renderer):
                # those imports are here because the renderer can be a
                # one liner # function defined by someone who
                # cannot import those. don't remove the unused imports
                import decimal
                import datetime
                try:
                    value = renderer(value=value)
                except Exception as e:
                    msg = 'Error during rendering %s with value %s : %s' % (
                        column_name, value, e
                    )
                    log.exception(msg)

            elif (
                    isinstance(renderer, six.string_types)
            ):
                # case when the caller has defined a renderer as a static
                # string effectively ignoring the real value
                value = renderer
            else:
                msg = 'Renderer should be callable or string, not %s' % type(
                    renderer)
                raise ColumnMappingError(msg)

        if value is None:
            # TODO: should we REALLY return an empty string here?
            value = u''

        return value
