#
#  This file is part of Oracle NoSQL Database
#  Copyright (C) 2011, 2015 Oracle and/or its affiliates.  All rights reserved.
#
# If you have received this file as part of Oracle NoSQL Database the
# following applies to the work as a whole:
#
#   Oracle NoSQL Database server software is free software: you can
#   redistribute it and/or modify it under the terms of the GNU Affero
#   General Public License as published by the Free Software Foundation,
#   version 3.
#
#   Oracle NoSQL Database is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#   Affero General Public License for more details.
#
# If you have received this file as part of Oracle NoSQL Database Client or
# distributed separately the following applies:
#
#   Oracle NoSQL Database client software is free software: you can
#   redistribute it and/or modify it under the terms of the Apache License
#   as published by the Apache Software Foundation, version 2.0.
#
# You should have received a copy of the GNU Affero General Public License
# and/or the Apache License in the LICENSE file along with Oracle NoSQL
# Database client or server distribution.  If not, see
# <http://www.gnu.org/licenses/>
# or
# <http://www.apache.org/licenses/LICENSE-2.0>.
#
# An active Oracle commercial licensing agreement for this product supersedes
# these licenses and in such case the license notices, but not the copyright
# notice, may be removed by you in connection with your distribution that is
# in accordance with the commercial licensing terms.
#
# For more information please contact:
#
# berkeleydb-info_us@oracle.com
#
from nosqldb import Store
from nosqldb import ConnectionException
from nosqldb import IllegalArgumentException
from nosqldb import RequestTimeoutException
from nosqldb import ONDB_RESULT
from testSetup import get_store
from testSetup import add_runtime_params
from testSetup import table_name

import unittest
import json


class TestExecuteSync(unittest.TestCase):

    def setUp(self):
        self.store = get_store()
        self.table = table_name + "TableTest"

    def tearDown(self):
        self.store.close()

    def testExecuteCreateTable(self):
        self.store.execute_sync("DROP TABLE IF EXISTS " + self.table + ".c1")
        self.store.execute_sync("DROP TABLE IF EXISTS " + self.table + ".c2")
        self.store.execute_sync("DROP TABLE IF EXISTS " + self.table)
        res = self.store.execute_sync(
            "create table if not exists " + self.table + " (" +
            "id INTEGER, prod_name STRING, days_in_shelf INTEGER, " +
            "PRIMARY KEY (id), COMMENT \"table created from Python API\" )")
        self.store.refresh_tables()
        expected = "{"\
          "'type' : 'table',"\
          "'name' : '" + self.table + "',"\
          "'owner' : null,"\
          "'comment' : 'table created from Python API',"\
          "'shardKey' : [ 'id' ],"\
          "'primaryKey' : [ 'id' ],"\
          "'fields' : [ {"\
          "  'name' : 'id',"\
          "  'type' : 'INTEGER',"\
          "  'nullable' : true,"\
          "  'default' : null"\
          "}, {"\
          "  'name' : 'prod_name',"\
          "  'type' : 'STRING',"\
          "  'nullable' : true,"\
          "  'default' : null"\
          "}, {"\
          "  'name' : 'days_in_shelf',"\
          "  'type' : 'INTEGER',"\
          "  'nullable' : true,"\
          "  'default' : null"\
          "} ]"\
        "}"
        res = self.store.execute_sync("desc as json table " + self.table)
        self.store.execute_sync("drop table if exists " + self.table)
        self.store.refresh_tables()
        self.assertEqual(expected.replace("\n", "").replace(" ", ""),
            str(res[ONDB_RESULT].get_string_result()).replace("\n", "").
            replace(" ", "").replace("\"", "'"))

    def testExecuteAlterTable(self):
        self.store.execute_sync("DROP TABLE IF EXISTS " + self.table + ".c1")
        self.store.execute_sync("DROP TABLE IF EXISTS " + self.table + ".c2")
        self.store.execute_sync("DROP TABLE IF EXISTS " + self.table)
        res = self.store.execute_sync(
            "create table if not exists " + self.table + " (" +
            "id INTEGER, prod_name STRING, days_in_shelf INTEGER, " +
            "PRIMARY KEY (id) )")
        self.store.refresh_tables()
        res = self.store.execute_sync(
            "alter table " + self.table + " (" +
            " ADD date_of_sale RECORD(day_of_week ENUM( sunday, monday," +
            " tuesday, wednesday, thursday, friday, saturday)," +
            " month INTEGER, day INTEGER, year INTEGER)," +
            " DROP days_in_shelf" +
            ")")
        expected = "{"\
          "'type' : 'table',"\
          "'name' : '" + self.table + "',"\
          "'owner' : null,"\
          "'comment' : null,"\
          "'shardKey' : [ 'id' ],"\
          "'primaryKey' : [ 'id' ],"\
          "'fields' : [ {"\
          "  'name' : 'id',"\
          "  'type' : 'INTEGER',"\
          "  'nullable' : true,"\
          "  'default' : null"\
          "}, {"\
          "  'name' : 'prod_name',"\
          "  'type' : 'STRING',"\
          "  'nullable' : true,"\
          "  'default' : null"\
          "}, {"\
          "  'name' : 'date_of_sale',"\
          "  'type' : 'RECORD',"\
          "  'fields' : [ {"\
          "    'name' : 'day_of_week',"\
          "    'type' : 'ENUM',"\
          "    'enum_name': 'day_of_week',"\
          "    'symbols' : ['sunday','monday','tuesday',"\
          "'wednesday','thursday','friday','saturday'],"\
          "    'nullable' : true,"\
          "    'default' : null"\
          "  }, { "\
          "    'name' : 'month',"\
          "    'type' : 'INTEGER',"\
          "    'nullable' : true,"\
          "    'default' : null"\
          "  }, { "\
          "    'name' : 'day',"\
          "    'type' : 'INTEGER',"\
          "    'nullable' : true,"\
          "    'default' : null"\
          "  }, { "\
          "    'name' : 'year',"\
          "    'type' : 'INTEGER',"\
          "    'nullable' : true,"\
          "    'default' : null"\
          "  }],"\
          "  'nullable' : true,"\
          "  'default' : null"\
          "} ]"\
        "}"
        res = self.store.execute_sync("desc as json table " + self.table)
        self.store.execute_sync("drop table if exists " + self.table)
        self.store.refresh_tables()
        self.assertEqual(expected.replace("\n", "").replace(" ", ""),
            str(res[ONDB_RESULT].get_string_result()).replace("\n", "").
            replace(" ", "").replace("\"", "'"))

    def testExecuteSyncDesc(self):
        self.store.execute_sync("DROP TABLE IF EXISTS " + self.table + ".c1")
        self.store.execute_sync("DROP TABLE IF EXISTS " + self.table + ".c2")
        self.store.execute_sync("DROP TABLE IF EXISTS " + self.table)
        self.store.execute_sync(
            "CREATE TABLE IF NOT EXISTS " + self.table + " (" +
            "shardKey INTEGER, id INTEGER, s STRING, " +
            "PRIMARY KEY (SHARD(shardKey), id) )")
        self.store.refresh_tables()
        self.store.execute_sync(
            "CREATE TABLE IF NOT EXISTS " + self.table + ".c1 (" +
            "idc1 INTEGER, s STRING, PRIMARY KEY (idc1) )")
        self.store.refresh_tables()
        self.store.execute_sync(
            "CREATE TABLE IF NOT EXISTS " + self.table + ".c2 (" +
            "idc2 INTEGER, s STRING, PRIMARY KEY (idc2) )")
        self.store.refresh_tables()
        res = self.store.execute_sync("Desc as json table " + self.table)
        expected = "{"\
          "'type' : 'table',"\
          "'name' : '" + self.table + "',"\
          "'owner' : null,"\
          "'comment' : null,"\
          "'shardKey' : [ 'shardKey' ],"\
          "'primaryKey' : [ 'shardKey', 'id' ],"\
          "'children' : [ 'c1', 'c2' ],"\
          "'fields' : [ {"\
          "  'name' : 'shardKey',"\
          "  'type' : 'INTEGER',"\
          "  'nullable' : true,"\
          "  'default' : null"\
          "}, {"\
          "  'name' : 'id',"\
          "  'type' : 'INTEGER',"\
          "  'nullable' : true,"\
          "  'default' : null"\
          "}, {"\
          "  'name' : 's',"\
          "  'type' : 'STRING',"\
          "  'nullable' : true,"\
          "  'default' : null"\
          "} ]"\
        "}"
        self.store.execute_sync("DROP TABLE IF EXISTS " + self.table + ".c1")
        self.store.execute_sync("DROP TABLE IF EXISTS " + self.table + ".c2")
        self.store.execute_sync("DROP TABLE IF EXISTS " + self.table)
        self.store.refresh_tables()
        self.assertEqual(expected.replace("\n", "").replace(" ", ""),
            str(res[ONDB_RESULT].get_string_result()).replace("\n", "").
            replace("\"", "'").replace(" ", ""))

    def testExecuteSyncShowTables(self):
        self.store.execute_sync("DROP TABLE IF EXISTS " + self.table + ".c1")
        self.store.execute_sync("DROP TABLE IF EXISTS " + self.table + ".c2")
        self.store.execute_sync("DROP TABLE IF EXISTS " + self.table)
        self.store.execute_sync(
            "CREATE TABLE IF NOT EXISTS " + self.table + " (" +
            "shardKey INTEGER, id INTEGER, s STRING, " +
            "PRIMARY KEY (SHARD(shardKey), id) )")
        self.store.refresh_tables()
        self.store.execute_sync(
            "CREATE TABLE IF NOT EXISTS " + self.table + ".c1 (" +
            "idc1 INTEGER, s STRING, PRIMARY KEY (idc1) )")
        self.store.refresh_tables()
        self.store.execute_sync(
            "CREATE TABLE IF NOT EXISTS " + self.table + ".c2 (" +
            "idc2 INTEGER, s STRING, PRIMARY KEY (idc2) )")
        self.store.refresh_tables()
        res = self.store.execute_sync("show as json tables")
        res = self.store.execute("show as json tables")
        json_res = json.loads(
            str(res.get_statement_result()[ONDB_RESULT].get_string_result()))
        tables_res = set(json_res['tables'])
        expected_set = set([self.table, self.table + ".c1", self.table + ".c2"])
        self.store.execute_sync("DROP TABLE IF EXISTS " + self.table + ".c1")
        self.store.execute_sync("DROP TABLE IF EXISTS " + self.table + ".c2")
        self.store.execute_sync("DROP TABLE IF EXISTS " + self.table)
        self.store.refresh_tables()
        self.assertTrue(expected_set.issubset(tables_res))

    def testExecuteSyncNoCommand(self):
        # test execute() with a empty command
        # expects an IllegalArgumentException
        self.assertRaises(IllegalArgumentException,
            self.store.execute_sync,
            "")

    def testExecuteSyncNoneCommand(self):
        # test execute_future_get() with an invalid
        # execution_id
        self.assertRaises(IllegalArgumentException,
            self.store.execute_sync,
            None)


if __name__ == '__main__':
    add_runtime_params()
    unittest.main()
