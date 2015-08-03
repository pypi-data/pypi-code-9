from contoml.file.entries import TableEntry, EntryName, AnonymousTableEntry
from contoml.file.cascadedict import CascadeDict


class NamedDict(dict):
    """
    A dict that can use EntryName instances as keys.
    """

    def __init__(self, other_dict=None):
        dict.__init__(self)
        if other_dict:
            for k, v in other_dict.items():
                self[k] = v

    def __setitem__(self, key, value):
        """
        key can be an EntryName instance.

        When key is a path in the form of an EntryName instance, all the parents and grandparents of the value are
        created along the way as instances of NamedDict. If the parent of the value exists, it is replaced with a
        CascadeDict() that cascades the old parent value with a new NamedDict that contains the given child name
        and value.
        """
        if isinstance(key, EntryName):

            if len(key.sub_names) == 1:
                name = key.sub_names[0]
                if name in self:
                    self[name] = CascadeDict(self[name], value)
                else:
                    self[name] = value

            elif len(key.sub_names) > 1:
                name = key.sub_names[0]
                rest_of_key = key.drop(1)
                if name in self:
                    named_dict = NamedDict()
                    named_dict[rest_of_key] = value
                    self[name] = CascadeDict(self[name], named_dict)
                else:
                    self[name] = NamedDict()
                    self[name][rest_of_key] = value
        else:
            return dict.__setitem__(self, key, value)

    def __contains__(self, item):
        try:
            _ = self[item]
            return True
        except KeyError:
            return False

    def append(self, key, value):
        """
        Makes sure the value pointed to by key exists and is a list and appends the given value to it.
        """
        if key in self:
            self[key].append(value)
        else:
            self[key] = [value]

    def __getitem__(self, item):

        if isinstance(item, EntryName):
            d = self
            for name in item.sub_names:
                d = d[name]
            return d
        else:
            return dict.__getitem__(self, item)


def structure(entries):
    """
    Accepts an ordered sequence of Entry instances and returns a navigable object structure representation of the
    TOML file.
    """

    entries = tuple(entries)
    obj = NamedDict()

    last_array_of_tables = None         # The EntryName of the last array-of-tables header

    for entry in entries:

        if isinstance(entry, AnonymousTableEntry):
            obj[''] = entry.table_element

        elif isinstance(entry, TableEntry):
            if last_array_of_tables and entry.name.is_prefixed_with(last_array_of_tables):
                seq = obj[last_array_of_tables]
                unprefixed_name = entry.name.without_prefix(last_array_of_tables)

                seq[-1] = CascadeDict(seq[-1], NamedDict({unprefixed_name: entry.table_element}))
            else:
                obj[entry.name] = entry.table_element
        else:    # It's an ArrayOfTablesEntry

            if last_array_of_tables and entry.name != last_array_of_tables and \
                    entry.name.is_prefixed_with(last_array_of_tables):

                seq = obj[last_array_of_tables]
                unprefixed_name = entry.name.without_prefix(last_array_of_tables)

                if unprefixed_name in seq[-1]:
                    seq[-1][unprefixed_name].append(entry.table_element)
                else:
                    cascaded_with = NamedDict({unprefixed_name: [entry.table_element]})
                    seq[-1] = CascadeDict(seq[-1], cascaded_with)

            else:
                obj.append(entry.name, entry.table_element)
                last_array_of_tables = entry.name

    return obj
