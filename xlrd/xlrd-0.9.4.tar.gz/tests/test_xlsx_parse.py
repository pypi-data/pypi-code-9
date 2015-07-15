###############################################################################
#
# Test the parsing of problematic xlsx files from bug reports.
#

import unittest
import xlrd
from .base import from_this_dir


class TestXlsxParse(unittest.TestCase):
    # Test parsing of problematic xlsx files. These are usually submitted
    # as part of bug reports as noted below.

    def test_for_github_issue_96(self):
        # Test for non-Excel file with forward slash file separator and
        # lowercase names. https://github.com/python-excel/xlrd/issues/96
        workbook = xlrd.open_workbook(from_this_dir('apachepoi_49609.xlsx'))
        worksheet = workbook.sheet_by_index(0)

        # Test reading sample data from the worksheet.
        cell = worksheet.cell(0, 1)
        self.assertEqual(cell.value, 'Cycle')
        self.assertEqual(cell.ctype, xlrd.book.XL_CELL_TEXT)

        cell = worksheet.cell(1, 1)
        self.assertEqual(cell.value, 1)
        self.assertEqual(cell.ctype, xlrd.book.XL_CELL_NUMBER)

    def test_for_github_issue_101(self):
        # Test for non-Excel file with forward slash file separator
        # https://github.com/python-excel/xlrd/issues/101
        workbook = xlrd.open_workbook(from_this_dir('self_evaluation_report_2014-05-19.xlsx'))
        worksheet = workbook.sheet_by_index(0)

        # Test reading sample data from the worksheet.
        cell = worksheet.cell(0, 0)
        self.assertEqual(cell.value, 'one')
        self.assertEqual(cell.ctype, xlrd.book.XL_CELL_TEXT)
