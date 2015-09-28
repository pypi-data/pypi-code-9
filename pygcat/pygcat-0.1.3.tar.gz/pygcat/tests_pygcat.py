# -*- coding: utf-8 -*-
#
# Copyright (c) 2015 Rodolphe Quiédeville <rodolphe@quiedeville.org>
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""

"""
from unittest import TestCase
import psycopg2
from pygcat import PygCatalog


class TestPygCatalog(TestCase):

    def setUp(self):
        self.conn = psycopg2.connect('')
        self.cat = PygCatalog(self.conn)

    def test_init(self):
        #
        dog = PygCatalog(None)
        self.assertEqual(dog.tables, None)
        self.assertEqual(len(dog.indexes), 0)

    def test_analyze(self):
        #
        dog = PygCatalog(self.conn)
        res = dog.analyze()
        
        self.assertEqual(res, None)


    # def test_analyze_alice(self):
    #     # Do an ANALYZE on a specific table
    #     dog = PygCatalog(self.conn)
    #     res = dog.analyze('alice.flower')
        
    #     self.assertEqual(res, None)

    def test_get_tables(self):
        # tables list from public schema
        conn = psycopg2.connect('')
        cat = PygCatalog(conn)
        
        cat.get_tables()
        tables = cat.tables
        self.assertEqual(len(tables), 2)
        self.assertEqual(tables['foo'].get('tuple'), 1000L )        

    def test_get_tables(self):
        # tables list from a specific schema
        conn = psycopg2.connect('')
        cat = PygCatalog(conn)
        
        cat.get_tables(schema='alice')
        tables = cat.tables
        self.assertEqual(len(tables), 1)
        self.assertEqual(tables['flower'].get('tuple'), 1L )        

    def test_table_tuples(self):
        #
        conn = psycopg2.connect('')
        cat = PygCatalog(conn)

        tuples = cat.table_tuples('foo')
        self.assertEqual(tuples, 1000L )        

    def test_get_table_columns(self):
        #
        conn = psycopg2.connect('')
        cat = PygCatalog(conn)

        cols = cat.get_table_columns('foo')
        self.assertEqual(cols, ['id', 'name', 'ratio', 'created_at'])

    def test_get_indexes(self):
        #
        cat = PygCatalog(self.conn)

        indexes = cat.get_indexes()
        tables = cat.get_tables()
        self.assertEqual(len(indexes), 2)
        self.assertEqual(tables['foo']['oid'], indexes['foo_name_ratio_idx']['table'])

    def test_get_indexes_schema(self):
        # Get all indexes in a specific schema
        # schema : alice
        cat = PygCatalog(self.conn)

        indexes = cat.get_indexes(schema='alice')
        self.assertEqual(len(indexes), 0)

    def test_is_column_exists(self):
        #
        cat = PygCatalog(self.conn)

        # this column is not indexed
        first  = cat.is_column_exists('created_at', 'foo')
        self.assertEqual(first, True)

    def test_column_does_not_exists(self):
        # the column does not exists
        cat = PygCatalog(self.conn)        
        second  = cat.is_column_exists('missing_column', 'foo')
        self.assertEqual(second, False)

    def test_column_exists_in_another_table(self):
        # the column does not exists in the table but in another one
        cat = PygCatalog(self.conn)        
        second  = cat.is_column_exists('properties', 'foo')
        self.assertEqual(second, False)
        
    def test_column_not_indexed(self):
        # The column is not present in any index
        cat = PygCatalog(self.conn)

        first  = cat.is_column_indexed('created_at', 'foo')

        self.assertEqual(first, 0)

    def test_column_indexed(self):
        # The column is present in one index
        cat = PygCatalog(self.conn)

        first  = cat.is_column_indexed('ratio', 'foo')

        self.assertEqual(first, True)

    def test_column_indexed_twice(self):
        # The column is present in two index
        cat = PygCatalog(self.conn)

        first  = cat.is_column_indexed('name', 'foo')
        self.assertEqual(first, True)

    def test_column_not_indexed(self):
        # The column is not present in any index
        res  = self.cat.is_column_indexed('properties', 'tools')

        self.assertEqual(res, False)

    def test_column_not_indexed_column_dne(self):
        # The column does not exists
        from pygcat import ColumnDoesNotExists
        
        with self.assertRaises(ColumnDoesNotExists):
            self.cat.is_column_indexed('missing_column', 'tools')

    def test_column_not_indexed_table_dne(self):
        # The table does not exists
        from pygcat import TableDoesNotExists
        
        with self.assertRaises(TableDoesNotExists):
            self.cat.is_column_indexed('name', 'missing_table')
