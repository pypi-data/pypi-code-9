from odio.text import (
    H, P, Span, TextWriter, TextReader, Title, Paragraph, Emphasis,
    StrongEmphasis, Heading1)
from odio.spreadsheet import (
    SpreadsheetWriter, SpreadsheetReader, Formula)

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions


__all__ = [
    H, P, Span, Title, StrongEmphasis, Paragraph, Heading1, Emphasis,
    SpreadsheetWriter, SpreadsheetReader, TextWriter, TextReader, Formula]
