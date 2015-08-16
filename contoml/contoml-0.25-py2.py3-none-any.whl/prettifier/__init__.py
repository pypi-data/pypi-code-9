from . import anontableindent, tableindent, tableassignment
from contoml.prettifier import tablesep, commentspace, linelength, tablesort

"""
    TOMLFile prettifiers

    Each prettifier is a function that accepts the list of Element instances that make up the
    TOMLFile and it is allowed to modify it as it pleases.
"""


UNIFORM_TABLE_INDENTATION = tableindent.table_entries_should_be_uniformly_indented
UNIFORM_TABLE_ASSIGNMENT_SPACING = tableassignment.table_assignment_spacing
ANONYMOUS_TABLE_INDENTATION = anontableindent.anon_table_indent
COMMENT_SPACING = commentspace.comment_space
TABLE_SPACING = tablesep.table_separation
LINE_LENGTH_ENFORCERS = linelength.line_lingth_limiter
TABLE_ENTRY_SORTING = tablesort.sort_table_entries


ALL = (
    TABLE_SPACING,      # Must be before COMMENT_SPACING
    COMMENT_SPACING,    # Must be after TABLE_SPACING
    UNIFORM_TABLE_INDENTATION,
    UNIFORM_TABLE_ASSIGNMENT_SPACING,
    ANONYMOUS_TABLE_INDENTATION,
    LINE_LENGTH_ENFORCERS,
    TABLE_ENTRY_SORTING,
)


def prettify(toml_file, prettifiers=ALL):
    """
    Prettifies a TOMLFile instance according to pre-defined set of formatting rules.
    """
    for prettifier in prettifiers:
        prettifier(toml_file)
