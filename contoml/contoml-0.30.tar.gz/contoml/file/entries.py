"""
    File entries are named top-level sections in a TOML file.
"""


from contoml import elements
from contoml.elements import TableElement, TableHeaderElement
from contoml.file.peekableit import PeekableIterator


class Entry:

    def __init__(self, names, table_element):
        self._table_element = table_element
        self._names = EntryName(names)

    @property
    def table_element(self):
        return self._table_element

    @property
    def name(self):
        """
        The distinct name of a table entry as an EntryName instance.
        """
        return self._names


class EntryName:
    """
    An entry's name.
    """

    def __init__(self, names):
        self._names = names

    @property
    def sub_names(self):
        return self._names

    def drop(self, n=0):
        """
        Returns the name after dropping the first n entries of it.
        """
        return EntryName(names=self._names[n:])

    def is_prefixed_with(self, names):
        if isinstance(names, EntryName):
            return self.is_prefixed_with(names.sub_names)

        for i, name in enumerate(names):
            if self._names[i] != name:
                return False
        return True

    def without_prefix(self, names):
        if isinstance(names, EntryName):
            return self.without_prefix(names.sub_names)

        for i, name in enumerate(names):
            if name != self._names[i]:
                return EntryName(self._names[i:])
        return EntryName(names=self.sub_names[len(names):])

    @property
    def is_relative(self):
        return len(self._names) > 1

    def __str__(self):
        return '.'.join(self.sub_names)

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return str(self) == str(other)

    def __ne__(self, other):
        return not self.__eq__(other)


class AnonymousTableEntry(Entry):

    def __init__(self, table_element):
        Entry.__init__(self, ('',), table_element)


class TableEntry(Entry):

    def __init__(self, names, table_element):
        Entry.__init__(self, names=names, table_element=table_element)


class ArrayOfTablesEntry(Entry):

    def __init__(self, names, table_element):
        Entry.__init__(self, names=names, table_element=table_element)


def _anonymous_table(peekable_iter):
    """
    Returns the TableElement of the anonymous table, or raises a KeyError if not found.
    """
    try:
        first_table = peekable_iter.peek()
        if isinstance(first_table, TableElement):
            return first_table
        else:
            raise KeyError
    except StopIteration:
        raise KeyError


def _validate_file_elements(file_elements):
    pass


def extract(file_elements):
    """
    Outputs an ordered sequence of instances of Entry types.

    Elements start with an optional TableElement, followed by zero or more pairs of (TableHeaderElement, TableElement).
    """

    _validate_file_elements(file_elements)

    # An iterator over enumerate(the non-metadata) elements
    iterator = PeekableIterator((element_i, element) for (element_i, element) in enumerate(file_elements)
                                if element.type != elements.TYPE_METADATA)

    try:
        _, first_element = iterator.peek()
        if isinstance(first_element, TableElement):
            iterator.next()
            yield AnonymousTableEntry(first_element)
    except KeyError:
        pass
    except StopIteration:
        return

    for element_i, element in iterator:

        if not isinstance(element, TableHeaderElement):
            continue

        # If TableHeader of a regular table, return Table following it
        if not element.is_array_of_tables:
            table_element_i, table_element = next(iterator)
            yield TableEntry(names=element.names, table_element=table_element)

        # If TableHeader of an array of tables, do your thing
        else:
            table_element_i, table_element = next(iterator)
            yield ArrayOfTablesEntry(names=element.names, table_element=table_element)
