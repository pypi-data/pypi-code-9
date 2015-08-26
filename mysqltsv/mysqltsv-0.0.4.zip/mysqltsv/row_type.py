import logging

from .util import read_row

logger = logging.getLogger("mysqltsv.row_type")

class AbstractRowType:

    def __init__(self, line):
        values = list(read_row(line, types=self._types))
        if self._headers and len(values) != len(self._headers):
            raise ValueError("Expected {0} values and got {1}."\
                             .format(len(self._headers), len(values)))

        self.__dict__['_values'] = values

    def __iter__(self):
        for value in self.__dict__['_values']:
            yield value

    def keys(self):
        return list(self._headers)

    def values(self):
        return self.__dict__['_values']

    def items(self):
        if self._headers:
            return ((h, v) for h, v in
                    zip(self._headers, self.__dict__['_values']))
        else:
            return ((i, v) for i, v in enumerate(self.__dict__['_values']))


    def __getitem__(self, key_or_index):

        index = self._internal_index(key_or_index)

        return self.__dict__['_values'][index]

    def __setitem__(self, key_or_index):
        raise TypeError("item assignment not supported")

    def __getattr__(self, key):
        index = self._internal_index(key)

        return self.__dict__['_values'][index]

    def __setattr__(self, key, value):
        raise TypeError("item assignment not supported")

    def _internal_index(self, key_or_index):
        if type(key_or_index) == int:
            index = key_or_index
        else:
            if key_or_index not in self._headers:
                raise KeyError(key_or_index)
            else:
                index = self._headers[key_or_index]

        return index

    def __ne__(self, other):
        return not self.__eq__(other)

    def __eq__(self, other):
        try:
            for p1, p2 in zip(self.iteritems(), other.iteritems()):
                if p1 != p2: return False

            return True
        except AttributeError:
            return False


def generate_row_type(headers, types=None):
    headers = list(headers) if headers is not None else None

    if types is not None:
        assert len(types) == len(headers), \
            "Length of types {0} must match headers {1}".format(len(types),
                                                                headers)

    class _RowType(AbstractRowType):
        _headers = dict((h, i) for i, h in enumerate(headers))
        _types = types

    return _RowType
