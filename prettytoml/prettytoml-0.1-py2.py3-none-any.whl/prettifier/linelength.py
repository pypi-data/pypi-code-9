import six
from prettytoml.elements import traversal as t, factory as element_factory
from prettytoml.elements.array import ArrayElement
from prettytoml.elements.atomic import AtomicElement
from prettytoml.elements.inlinetable import InlineTableElement
from prettytoml.elements.table import TableElement


MAXIMUM_LINE_LENGTH = 120


def line_lingth_limiter(toml_file_elements):
    """
    Rule: Lines whose lengths exceed 120 characters whose values are strings, arrays, or inline tables
    should have the array or string value broken onto multiple lines and the inline table turned into
    a multiline table section so as to try to maintain a maximum line length of 120.
    """
    elements = toml_file_elements[:]

    all_new_tables = dict()

    for (i, element) in enumerate(elements):
        if isinstance(element, TableElement):
            new_tables = _do_table(element.sub_elements)
            if i > 0 and new_tables:
                table_names = elements[i-1].names if i > 0 else tuple()
                all_new_tables[table_names] = new_tables
                elements[i-1] = element_factory.create_whitespace_element(length=0)

    for (names, mapping) in all_new_tables.items():
        for name, value in mapping.items():
            names = list(names) + [name]
            elements.append(element_factory.create_table_header_element(names))
            elements.append(element_factory.create_table(value))

    return elements


def _do_table(table_elements):
    """
    Should return a dict mapping keys to values which are to be turned into top-level tables.
    """

    new_tables = dict()

    it = float('-inf')

    def next_newline():
        return t.find_following(table_elements, t.predicates.newline, it)

    def next_key():
        return t.find_following(table_elements, t.predicates.non_metadata, it)

    def next_value():
        return t.find_following(table_elements, t.predicates.non_metadata, next_key())

    def line_length():
        elements = table_elements[it:next_newline()] if it > float('-inf') else table_elements[:next_newline()]
        return len(''.join(e.serialized() for e in elements))

    while next_newline() >= 0:

        if line_length() > MAXIMUM_LINE_LENGTH and next_value() >= 0:
            value_i = next_value()
            value = table_elements[value_i]

            if isinstance(value, AtomicElement) and isinstance(value.value, six.string_types):
                table_elements[value_i] = element_factory.create_multiline_string(value.value, MAXIMUM_LINE_LENGTH)

            elif isinstance(value, ArrayElement):
                value.turn_into_multiline()

            elif isinstance(value, InlineTableElement):
                new_tables[table_elements[next_key()].value] = value.primitive_value
                if it > float('-inf'):
                    del table_elements[it:next_newline()]
                else:
                    del table_elements[:next_newline()]

        it = next_newline()

    return new_tables
