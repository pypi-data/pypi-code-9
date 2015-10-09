import lzma

from collections import defaultdict
from os.path import dirname, join

# Default map version to use
DEFAULT_MAP_VERSION = 'ensembl75'

# All available maps
MAP_VERSION_FILES = {
    'ensembl75': join(dirname(__file__), 'datasets', 'ensembl75_to_symbol.txt.xz')
}

# Singleton instances
CONVERTER_MAP = None
CONVERTER_INSTANCE = None


def set_converter(version=None):
    """
    Sets the map version to use as converter. If you don't want to use the default
    map, you must call this function just before using any convertion function.

    :param version: The map name to use
    :return: The converter
    """
    global CONVERTER_MAP, CONVERTER_INSTANCE

    if version is None:
        if CONVERTER_MAP is None:
            version = DEFAULT_MAP_VERSION
        else:
            version = CONVERTER_MAP

    if version != CONVERTER_MAP:
        CONVERTER_MAP = version
        CONVERTER_INSTANCE = BgConverter(map=CONVERTER_MAP)

    return CONVERTER_INSTANCE


def ensembl_to_symbol(ensembl_id, separator=', '):
    """
    Converts an ENSEMBL gene id to a HUGO symbol id

    :param ensembl_id: ENSEMBL gene id
    :param separator: If there are multiple symbols with the given id it will join them using this separator.
    Default is using a comma. It can also be a callable function that receive a list and returns whatever you
    want. As an example if you simply want a list or a set you can put 'separator=list' or 'separator=set'.

    :return: The matching HUGO symbols ids.
    """
    return set_converter().ensembl_to_symbol(ensembl_id, separator=separator)


def symbol_to_ensembl(symbol_id, separator=', '):
    """
    Converts a gene HUGO symbol to a ENSEMBL gene id

    :param symbol_id: HUGO symbol id
    :param separator: If there are multiple ensembl ids with the given symbol it will join them using this separator.
    Default is using a comma. It can also be a callable function that receive a list and returns whatever you
    want. As an example if you simply want a list or a set you can put 'separator=list' or 'separator=set'

    :return: The matching ENSEMBL ids
    """
    return set_converter().symbol_to_ensembl(symbol_id, separator=separator)


class BgConverter(object):

    def __init__(self, map=DEFAULT_MAP_VERSION):

        # Load map
        self.ensembl_to_symbol_map = defaultdict(list)
        self.symbol_to_ensembl_map = defaultdict(list)

        if map not in MAP_VERSION_FILES:
            raise AssertionError("Unknown map '{}'\n\nAvailable maps:\n{}".format(map, '\n'.join(MAP_VERSION_FILES.keys())))

        map_file = MAP_VERSION_FILES[map]
        for line in lzma.open(map_file, 'rt'):
            row = line.split("\t")

            # Parse ensembl and symbol ids
            ensembl = row[0].strip().upper()
            symbol = row[1].strip().upper()

            # Create two reverse dictionaries
            self.ensembl_to_symbol_map[ensembl].append(symbol)
            self.symbol_to_ensembl_map[symbol].append(ensembl)

    @staticmethod
    def _join(values, separator):

        # If the separator is a function use it to return
        # the values
        if hasattr(separator, '__call__'):
            return separator(values)

        # Otherwise we assume that is a string separator
        return separator.join(values)

    def ensembl_to_symbol(self, ensembl, separator=', '):
        return self._join(
            self.ensembl_to_symbol_map.get(ensembl.upper(), []),
            separator
        )

    def symbol_to_ensembl(self, symbol, separator=', '):
        return self._join(
            self.symbol_to_ensembl_map.get(symbol.upper(), []),
            separator
        )