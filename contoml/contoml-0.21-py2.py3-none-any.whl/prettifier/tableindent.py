from contoml import tokens
from contoml.elements import traversal as t, factory as element_factory
from contoml.tokens import py2toml


def table_entries_should_be_uniformly_indented(toml_file):
    """
    Rule: Nth-level table sections should be indented by (N-1)*2 spaces
    """
    toml_file_elements = toml_file.elements
    for (i, e) in enumerate(toml_file_elements):
        if t.predicates.table_header(e):
            table = toml_file_elements[t.find_following(toml_file_elements, t.predicates.table, i)]
            _do_table_header(e)
            _do_table(table, len(e.names))


def _do_table_header(table_header):
    indent_start = 0
    indent_end = next(i for (i, token) in enumerate(table_header.tokens) if token.type != tokens.TYPE_WHITESPACE)

    del table_header.tokens[indent_start:indent_end]
    table_header.tokens.insert(0, py2toml.create_whitespace(' ' * ((len(table_header.names)-1) * 2)))


def _do_table(table_element, table_level):

    elements = table_element.sub_elements

    # Iterator index
    i = float('-inf')

    def first_indent():
        return t.find_following(elements, t.predicates.whitespace, i)

    def next_non_metadata():
        return t.find_following(elements, t.predicates.non_metadata, i)

    def next_newline():
        return t.find_following(elements, t.predicates.newline, next_non_metadata())

    while next_non_metadata() >= 0:
        if first_indent() >= 0:
            del elements[first_indent():next_non_metadata()]

        elements.insert(next_non_metadata(), element_factory.create_whitespace_element((table_level-1)*2))

        i = next_newline()
