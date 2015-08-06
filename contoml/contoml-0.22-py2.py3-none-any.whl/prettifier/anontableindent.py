
from contoml.elements import traversal as t


def anon_table_indent(toml_file):
    """
    Rule: Anonymous table should never be indented.
    """
    toml_file_elements = toml_file.elements

    if not toml_file_elements or not t.predicates.table(toml_file_elements[0]):
        return

    elements = toml_file_elements[0].sub_elements

    # Must delete zero-length whitespaces first
    _drop_empty_whitespace_element(elements)

    i = None

    def first_indent():
        return t.find_following(elements, t.predicates.whitespace, i)

    def next_non_metadata():
        return t.find_following(elements, t.predicates.non_metadata, i)

    def next_newline():
        return t.find_following(elements, t.predicates.newline, next_non_metadata())

    while next_non_metadata() >= 0:
        if first_indent() < next_non_metadata() < next_newline():
            del elements[first_indent():next_non_metadata()]
        i = next_newline()


def _drop_empty_whitespace_element(table_elements):

    def next_zero_whitespace_i():
        try:
            return next(i for (i, e) in enumerate(table_elements) if t.predicates.whitespace(e) and e.length == 0)
        except StopIteration:
            return None

    while next_zero_whitespace_i() is not None:
        del table_elements[next_zero_whitespace_i()]
