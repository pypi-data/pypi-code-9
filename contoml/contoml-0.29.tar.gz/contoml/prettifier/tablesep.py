
from contoml.elements import traversal as t, factory as element_factory
from contoml.elements.metadata import WhitespaceElement, NewlineElement
from contoml.elements.table import TableElement


def table_separation(toml_file):
    """
    Rule: Tables should always be separated by an empty line.
    """
    toml_file_elements = toml_file.elements
    for element in toml_file_elements:
        if isinstance(element, TableElement):
            _do_table(element.sub_elements)


def _do_table(table_elements):

    while table_elements and isinstance(table_elements[-1], WhitespaceElement):
        del table_elements[-1]

    if not table_elements:
        return

    if isinstance(table_elements[-1], NewlineElement):
        last_non_metadata_i = t.find_previous(table_elements, t.predicates.non_metadata)
        del table_elements[last_non_metadata_i+1:]

    table_elements.append(element_factory.create_newline_element())
    table_elements.append(element_factory.create_newline_element())
