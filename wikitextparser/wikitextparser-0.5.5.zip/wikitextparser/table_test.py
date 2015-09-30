"""Specifically test the table.py module."""


import sys
import unittest


class Table(unittest.TestCase):

    """Test the table class."""

    def basics(self):
        wikitext = (
            '{|\n|Orange\n|Apple\n|-\n|Bread\n|Pie\n|-\n|'
            'Butter\n|Ice cream \n|}'
        )
        table = Table(wikitext)
        self.assertEqual(
            table.cols,
            2,
        )
        self.assertEqual(
            table.rows,
            3,
        )
        self.assertEqual(
            table.row(1),
            ('Apple', 'Orange'),
        )
        self.assertEqual(
            table.col(2),
            ('Orange', 'Bread', 'Butter'),
        )
        

if __name__ == '__main__':
    unittest.main()
