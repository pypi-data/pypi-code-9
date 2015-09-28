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
"""Read stats from pg_stat_statements Postgresql extension

You may use a postgresql base to log info, in this case you'll need the
file schema.sql

"""
from psycopg2.extensions import AsIs

class ColumnDoesNotExists(Exception):
    pass

class TableDoesNotExists(Exception):
    pass


class PygCatalog(object):
    """Python library to read PostgreSQL internal catalog

    """

    def __init__(self, conn=None):
        self.conn = conn
        self.tables = None
        self.indexes = {}
        self.lastquery = None

    def _read_db(self, schema='public'):
        if self.tables is None:
            self.get_tables(schema)

    def analyze(self, table=None):
        """Run an ANALYZE over the database or a table
        """
        cur = self.conn.cursor()

        if table:
            qry = """ANALYZE %s"""
        else:
            qry = """ANALYZE"""

        return cur.execute(qry, (AsIs(table), ))


    def get_tables(self, schema='public'):
        """Return tables list
        """
        cur = self.conn.cursor()

        qry = """
              SELECT c.relname, c.reltuples::bigint, c.oid
              FROM pg_class AS c
              INNER JOIN pg_catalog.pg_namespace n ON c.relnamespace = n.oid
              WHERE relkind = 'r'
              AND n.nspname = %s
              """

        cur.execute(qry, (schema, ))

        self.tables = {}
        for row in cur.fetchall():
            self.tables[row[0]] = {'tuple': row[1],
                                   'oid': row[2],
                                   'columns': None}

        return self.tables

    def table_tuples(self, table, schema='public'):
        """Return the number of tuples in a table
        """
        self._read_db()
        return self.tables[table]['tuple']

    def get_table_columns(self, table, schema='public'):
        """Return all columns in a table
        """
        self._read_db()

        if self.tables.get(table):
            return self._get_columns(self.tables[table]['oid'])
        else:
            return None

    def _get_columns(self, oid):
        """Return columns for a table
        """
        cur = self.conn.cursor()

        qry = """
              SELECT attname, attnum
              FROM pg_catalog.pg_attribute AS a
              WHERE attrelid = %s
              AND attnum > 0
              AND attisdropped = false
              """

        cur.execute(qry, (oid, ))
        columns = []
        for row in cur.fetchall():
            columns.append(row[0])

        return columns

    def _execute_sql(self, qry, parms=None):
        """Execute a sql query
        """
        cur = self.conn.cursor()

        self.lastquery = cur.mogrify(qry, parms)

        cur.execute(qry, parms)

        return cur.fetchall()

    def get_indexes(self, schema='public'):
        """Return tables list
        """
        qry = """
              SELECT c.relname, c.reltuples::bigint, c.oid, i.indrelid,
              i.indkey
              FROM pg_class AS c
              INNER JOIN pg_catalog.pg_namespace n ON c.relnamespace = n.oid
              INNER JOIN pg_catalog.pg_index i ON c.oid = i.indexrelid
              WHERE c.relkind = 'i'
              AND n.nspname = %s
              """

        rows = self._execute_sql(qry, (schema, ))

        indexes = {}

        for row in rows:
            indexes[row[0]] = {'tuple': row[1],
                               'oid': row[2],
                               'columns': None,
                               'table': row[3]}
        return indexes

    def is_column_indexed(self, column_name, table_name, schema='public'):
        """Return true if a column is indexed
        """
        if not self.is_table_exists(table_name, schema):
            msg = "table %s does not exist in schema%s"
            raise TableDoesNotExists(msg % (schema, table_name))

        if not self.is_column_exists(column_name, table_name, schema):
            msg = "column %s does not exist in table %s.%s"
            raise ColumnDoesNotExists(msg % (column_name, schema, table_name))

        qry = """
        WITH cte AS (
        SELECT c.relname as indexname, c.oid, i.indrelid, unnest( i.indkey) as attnum

        FROM pg_class AS c

        INNER JOIN pg_catalog.pg_namespace n ON c.relnamespace = n.oid
        INNER JOIN pg_catalog.pg_index i ON c.oid = i.indexrelid

        WHERE c.relkind = 'i'
        AND n.nspname = %s
        )

        SELECT cte.*, a.attname, t.relname as tablename
        FROM cte
        INNER JOIN pg_class t ON cte.indrelid = t.oid
        INNER JOIN pg_catalog.pg_attribute a ON (cte.attnum = a.attnum AND a.attrelid = cte.indrelid)
        WHERE a.attname = %s AND t.relname = %s
        """

        rows = self._execute_sql(qry, (schema, column_name, table_name))

        return (len(rows) > 0)

    def is_column_exists(self, column_name, table_name, schema='public'):
        """Return true if a column exists in a table
        """
        qry = """
        SELECT 1
        FROM pg_catalog.pg_attribute a
        INNER JOIN pg_class t ON a.attrelid = t.oid
        INNER JOIN pg_catalog.pg_namespace n ON t.relnamespace = n.oid
        WHERE n.nspname = %s
        AND a.attname = %s
        AND t.relname = %s
        """

        rows = self._execute_sql(qry, (schema, column_name, table_name))

        return (len(rows) > 0)

    def is_table_exists(self, table_name, schema='public'):
        """Return true if a table exists
        """
        qry = """
        SELECT 1
        FROM pg_class t
        INNER JOIN pg_catalog.pg_namespace n ON t.relnamespace = n.oid
        WHERE n.nspname = %s
        AND t.relname = %s
        """
        rows = self._execute_sql(qry, (schema, table_name))

        return (len(rows) > 0)

