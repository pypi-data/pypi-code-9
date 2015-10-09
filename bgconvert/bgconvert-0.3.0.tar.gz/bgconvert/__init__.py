import bz2
import gzip
import lzma

from collections import defaultdict
from os.path import dirname, join, exists

# Default map version to use
DEFAULT_MAP_VERSION = 'ensembl75'

# All available maps
MAP_VERSION_FILES = {
    'ensembl75': join(dirname(__file__), 'datasets', 'ensembl75_to_symbol.txt.xz'),
    'intogen-201412': join(dirname(__file__), 'datasets', 'intogen-201412_ensembl_to_symbol.txt.xz')
}

# Singleton instances
CONVERTER_MAP = None
CONVERTER_INSTANCE = None


def register_ensembl_symbol_map(map_version, map_file):
    """
    Register a map file to convert ENSEMBL to HUGO symbols

    :param map_version: Map version name
    :param map_file: Absolute path to a file with the elements map
    """

    if not exists(map_file):
        raise FileNotFoundError("Map file '{}' not found".format(map_file))

    MAP_VERSION_FILES[map_version] = map_file


def use_ensembl_symbol_map(map_version=None):
    """
    Sets the map version to use as converter. If you don't want to use the default
    map, you must call this function just before using any convertion function.

    :param map_version: The map name to use
    :return: The converter
    """
    global CONVERTER_MAP, CONVERTER_INSTANCE

    if map_version is None:
        if CONVERTER_MAP is None:
            map_version = DEFAULT_MAP_VERSION
        else:
            map_version = CONVERTER_MAP

    if map_version != CONVERTER_MAP:
        CONVERTER_MAP = map_version
        CONVERTER_INSTANCE = BgConverter(map_version=CONVERTER_MAP)

    return CONVERTER_INSTANCE


def ensembl_to_symbol(ensembl_id, separator=', ', no_match=''):
    """
    Converts an ENSEMBL gene id to a HUGO symbol id

    :param ensembl_id: ENSEMBL gene id
    :param separator: If there are multiple symbols with the given id it will join them using this separator.
    Default is using a comma. It can also be a callable function that receive a list and returns whatever you
    want. As an example if you simply want a list or a set you can put 'separator=list' or 'separator=set'.
    :param no_match: Value to return if there is no match. If it's a function then this function will be call
    with the ensembl_id value

    :return: The matching HUGO symbols ids.
    """
    return use_ensembl_symbol_map().ensembl_to_symbol(ensembl_id, separator=separator, no_match=no_match)


def symbol_to_ensembl(symbol_id, separator=', ', no_match=''):
    """
    Converts a gene HUGO symbol to a ENSEMBL gene id

    :param symbol_id: HUGO symbol id
    :param separator: If there are multiple ensembl ids with the given symbol it will join them using this separator.
    Default is using a comma. It can also be a callable function that receive a list and returns whatever you
    want. As an example if you simply want a list or a set you can put 'separator=list' or 'separator=set'
    :param no_match: Value to return if there is no match. If it's a function then this function will be call
    with the ensembl_id value

    :return: The matching ENSEMBL ids
    """
    return use_ensembl_symbol_map().symbol_to_ensembl(symbol_id, separator=separator, no_match=no_match)


class BgConverter(object):

    def __init__(self, map_version=DEFAULT_MAP_VERSION):

        # Load map
        self.ensembl_to_symbol_map = defaultdict(list)
        self.symbol_to_ensembl_map = defaultdict(list)

        if map_version not in MAP_VERSION_FILES:
            raise AssertionError("Unknown map '{}'\n\nAvailable maps:\n{}".format(map_version, '\n'.join(MAP_VERSION_FILES.keys())))

        map_file = MAP_VERSION_FILES[map_version]
        if map_file.endswith(".gz"):
            fd = gzip.open(map_file, "rt")
        elif map_file.endswith(".bz2"):
            fd = bz2.open(map_file, "rt")
        elif map_file.endswith(".xz"):
            fd = lzma.open(map_file, "rt")
        else:
            fd = open(map_file, "rt")

        for line in fd:
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

    @staticmethod
    def _no_match(value, no_match):
        if hasattr(no_match, '__call__'):
            return no_match(value)
        return no_match

    def _map(self, map_dict, value, separator, no_match):
        values = map_dict.get(value.strip().upper(), [])
        if len(values) == 0:
            return self._no_match(value, no_match)
        return self._join(values, separator)

    def ensembl_to_symbol(self, ensembl, separator=', ', no_match=''):
        return self._map(self.ensembl_to_symbol_map, ensembl, separator, no_match)

    def symbol_to_ensembl(self, symbol, separator=', ', no_match=''):
        return self._map(self.symbol_to_ensembl_map, symbol, separator, no_match)