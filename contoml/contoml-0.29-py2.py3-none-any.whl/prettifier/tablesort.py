
from contoml.elements.table import TableElement
from contoml.elements import traversal as t, factory as element_factory


def sort_table_entries(toml_file):
    for element in toml_file.elements:
        if isinstance(element, TableElement):
            __do_table(element)


def __do_table(table):

    elements = table.sub_elements

    def line_ranges():
        # Returns [start, stop) indices of lines in the table
        next_start = 0
        while t.find_following(elements, t.predicates.newline, next_start-1) >= 0:
            next_stop = t.find_following(elements, t.predicates.newline, next_start-1)
            yield (next_start, next_stop+1)
            next_start = next_stop + 1

    def line_key(line_start, line_stop):
        # Returns the key to sort the lines by
        i = t.find_following(elements, t.predicates.non_metadata, line_start-1)
        if -1 < i < line_stop:
            return elements[i].value
        else:
            return 'z'*20   # Empty line should be at the end

    old_elements = table.elements[:]
    sorted_ranges = sorted(tuple(line_ranges()), key=lambda r: line_key(*r))

    del table.elements[:]
    for (start, stop) in sorted_ranges:
        for e in old_elements[start:stop]:
            table.elements.append(e)

