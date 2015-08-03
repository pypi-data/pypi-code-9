from contoml.errors import NoArrayFoundError, InvalidValueError
from contoml.file import structurer, entries, raw
from contoml.file.array import ArrayOfTables
from contoml.file.freshtable import FreshTable
import contoml.elements.factory as element_factory
from contoml import prettifier


class TOMLFile:
    """
    A TOMLFile object that tries its best to prserve formatting and order of mappings of the input source.

    Raises InvalidTOMLFileError on invalid input elements.
    """

    def __init__(self, _elements):
        self._elements = []
        self._navigable = {}
        self.append_elements(_elements)

    def __getitem__(self, item):
        try:
            value = self._navigable[item]
            if isinstance(value, (list, tuple)):
                return ArrayOfTables(parent=self, name=item, iterable=value)
            else:
                return value
        except KeyError:
            return FreshTable(parent=self, name=item, is_array=False)

    def __contains__(self, item):
        return item in self.keys()

    def __setitem__(self, key, value):

        if key and isinstance(value, (tuple, list)) and all(isinstance(v, dict) for v in value):
            for table in value:
                self.array(key).append(table)

        elif isinstance(value, dict):
            if key in self._navigable:
                index = self._elements.index(self._navigable[key])
                self._elements = self._elements[:index] + [element_factory.create_table(value)] + self._elements[index+1:]
            else:
                if key:
                    self._elements.append(element_factory.create_table_header_element(key))
                self._elements.append(element_factory.create_table(value))
                self._elements.append(element_factory.create_newline_element())

        else:
            raise InvalidValueError('Assigned value must be a dict or a sequence of dicts')

        self._recreate_navigable()

    def _recreate_navigable(self):
        if self._elements:
            self._navigable = structurer.structure(entries.extract(self._elements))

    def array(self, name):
        """
        Returns the array of tables with the given name.
        """
        if name in self._navigable:
            if isinstance(self._navigable[name], (list, tuple)):
                return self[name]
            else:
                raise NoArrayFoundError
        else:
            return ArrayOfTables(parent=self, name=name)

    def append_elements(self, elements):
        """
        Appends more elements to the contained internal elements.
        """
        self._elements = self._elements + list(elements)
        self._recreate_navigable()

    def prepend_elements(self, elements):
        """
        Prepends more elements to the contained internal elements.
        """
        self._elements = list(elements) + self._elements
        self._recreate_navigable()

    def dumps(self):
        """
        Returns the TOML file serialized back to str.
        """
        return ''.join(element.serialized() for element in self._elements)

    def dump(self, file_path):
        with open(file_path, mode='w') as fp:
            fp.write(self.dumps())

    def keys(self):
        return set(self._navigable.keys()) | {''}

    def values(self):
        return self._navigable.values()

    def items(self):
        items = self._navigable.items()

        def has_anonymous_entry():
            return any(key == '' for (key, _) in items)

        if has_anonymous_entry():
            return items
        else:
            return items + [('', self[''])]

    @property
    def primitive(self):
        """
        Returns a primitive object representation for this container (which is a dict).

        WARNING: The returned container does not contain any markup or formatting metadata.
        """
        return raw.to_raw(self._navigable)

    def append_fresh_table(self, fresh_table):
        """
        Gets called by FreshTable instances when they get written to.
        """
        if fresh_table.name:
            elements = []
            if fresh_table.is_array:
                elements += [element_factory.create_array_of_tables_header_element(fresh_table.name)]
            else:
                elements += [element_factory.create_table_header_element(fresh_table.name)]

            elements += [fresh_table, element_factory.create_newline_element()]
            self.append_elements(elements)

        else:
            # It's an anonymous table
            self.prepend_elements([fresh_table, element_factory.create_newline_element()])

    def prettify(self, prettifiers=prettifier.ALL):
        """
        Reformats this TOML file using the specified consistent set of formatting rules.
        """
        prettifier.prettify(self, prettifiers)
        self._recreate_navigable()

    @property
    def elements(self):
        return self._elements
