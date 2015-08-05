"""Contains classes allowing the user to read data from various spreadsheet formats in a unified
manner.
"""

from .base import CellMode, Cell, WorksheetBase, WorkbookBase
from .csv import CSVWorkbook
from .excel import ExcelWorkbook
from .open_document import OpenDocumentWorkbook
