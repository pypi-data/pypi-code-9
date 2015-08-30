from contoml.elements.table import TableElement
from contoml.errors import NoArrayFoundError, InvalidValueError
from contoml.file import structurer, entries, raw
from contoml.file.array import ArrayOfTables
from contoml.file.entries import TableEntry
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

        # Setting an array-of-tables
        if key and isinstance(value, (tuple, list)) and value and all(isinstance(v, dict) for v in value):
            for table in value:
                self.array(key).append(table)

        # Or setting a whole single table
        elif isinstance(value, dict):
            if key in self._navigable:
                index = self._elements.index(self._navigable[key])
                self._elements = self._elements[:index] + [element_factory.create_table(value)] + self._elements[index+1:]
            else:
                if key:
                    self._elements.append(element_factory.create_table_header_element(key))
                self._elements.append(element_factory.create_table(value))
                # self._elements.append(element_factory.create_newline_element())

        # Or updating the anonymous section table
        else:
            # It's mea
            self[''][key] = value

        self._on_element_change()

    def _update_table_fallbacks(self):
        """
        Updates the fallbacks on all the table elements to make relative table access possible.
        """

        if len(self.elements) <= 1:
            return

        table_entries = tuple(e for e in entries.extract(self.elements) if isinstance(e, TableEntry))

        def parent_of(entry):
            # Returns an Entry parent of the given entry, or None.
            for parent_entry in table_entries:
                if entry.name.sub_names[:-1] == parent_entry.name.sub_names:
                    return parent_entry

        for entry in table_entries:
            if entry.name.is_relative:
                parent = parent_of(entry)
                if parent:
                    parent.table_element.set_fallback(
                        {entry.name.without_prefix(parent.name).sub_names[0]: entry.table_element})

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

    def _on_element_change(self):
        self._recreate_navigable()
        self._update_table_fallbacks()

    def append_elements(self, elements):
        """
        Appends more elements to the contained internal elements.
        """
        self._elements = self._elements + list(elements)
        self._on_element_change()

    def prepend_elements(self, elements):
        """
        Prepends more elements to the contained internal elements.
        """
        self._elements = list(elements) + self._elements
        self._on_element_change()

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
        raw_container = raw.to_raw(self._navigable)

        # Collapsing the anonymous table onto the top-level container is present
        if '' in raw_container:
            raw_container.update(raw_container[''])
        del raw_container['']

        return raw_container

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

    def __str__(self):

        is_empty = (not self['']) and (not tuple(k for k in self.keys() if k))

        def key_name(key):
            return '[ANONYMOUS]' if not key else key

        def pair(key, value):
            return '%s = %s' % (key_name(key), str(value))

        content_text = '' if is_empty else \
            '\n\t' + ',\n\t'.join(pair(k, v) for (k, v) in self.items() if v) + '\n'

        return "TOMLFile{%s}" % content_text

    def __repr__(self):
        return str(self)
