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
from nosqldb import Row
from nosqldb import ConnectionException
from nosqldb import IllegalArgumentException
from nosqldb import RequestTimeoutException
from nosqldb import TimeoutException
from nosqldb import ONDB_IS_DONE
from nosqldb import ONDB_IS_SUCCESSFUL
from nosqldb import ONDB_RESULT
from testSetup import get_store
from testSetup import add_runtime_params
from testSetup import table_name

import unittest
import json
import time


class TestExecute(unittest.TestCase):

    def setUp(self):
        self.store = get_store()
        self.table = table_name + "testTable"
        self.store.execute_sync("drop table if exists " + self.table + ".c1")
        self.store.execute_sync("drop table if exists " + self.table + ".c2")
        self.store.execute_sync("drop table if exists " + self.table)

    def tearDown(self):
        self.store.execute_sync("drop table if exists " + self.table + ".c1")
        self.store.execute_sync("drop table if exists " + self.table + ".c2")
        self.store.execute_sync("drop table if exists " + self.table)
        self.store.refresh_tables()
        self.store.close()

    def testExecuteDesc(self):
        self.store.execute_sync(
            "CREATE TABLE IF NOT EXISTS " + self.table + " (" +
            "shardKey INTEGER, id INTEGER, s STRING, " +
            "PRIMARY KEY (SHARD(shardKey), id) )")
        self.store.execute_sync(
            "CREATE TABLE IF NOT EXISTS " + self.table + ".c1 (" +
            "idc1 INTEGER, s STRING, PRIMARY KEY (idc1) )")
        self.store.execute_sync(
            "CREATE TABLE IF NOT EXISTS " + self.table + ".c2 (" +
            "idc2 INTEGER, s STRING, PRIMARY KEY (idc2) )")
        self.store.refresh_tables()
        res = self.store.execute("desc as json table " + self.table)
        expected = \
          "{'type' : 'table',"\
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
          "} ]}"
        self.store.execute_sync("DROP TABLE IF EXISTS " + self.table + ".c1")
        self.store.execute_sync("DROP TABLE IF EXISTS " + self.table + ".c2")
        self.store.execute_sync("DROP TABLE IF EXISTS " + self.table)
        self.store.refresh_tables()
        self.assertEqual(expected.replace("\n", "").replace(" ", ""),
            str(res.get_statement_result()[ONDB_RESULT].get_string_result()).
            replace("\n", "").replace("\"", "'").
            replace(" ", ""))

    def testExecuteStatusShowTables(self):
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
        res = self.store.execute("show as json tables")
        count = 0
        stmt_res = res.get_statement_result()
        while (not stmt_res[ONDB_IS_DONE] and count < 10):
            try:
                res.update_status()
                stmt_res = res.get_statement_result()
                time.sleep(1)
                count += 1
            except Exception, e:
                raise
        self.assertTrue(stmt_res[ONDB_IS_DONE] and stmt_res[ONDB_IS_SUCCESSFUL])
        json_res = json.loads(str(stmt_res[ONDB_RESULT].get_string_result()))
        tables_res = set(json_res['tables'])
        expected_set = set([self.table, self.table + ".c1", self.table + ".c2"])
        self.store.execute_sync("DROP TABLE IF EXISTS " + self.table + ".c1")
        self.store.execute_sync("DROP TABLE IF EXISTS " + self.table + ".c2")
        self.store.execute_sync("DROP TABLE IF EXISTS " + self.table)
        self.store.refresh_tables()
        self.assertTrue(expected_set.issubset(tables_res))

    def testExecuteFutureTimeoutCreateTable(self):
        res = self.store.execute(
            "create table if not exists " + self.table + " ( " +
            "id INTEGER, prod_name STRING, days_in_shelf INTEGER, " +
            "PRIMARY KEY (id), COMMENT \"table created from Python API\" )")
        stmt_res = res.get_statement_result()
        while (not stmt_res[ONDB_IS_DONE]):
            # wait 10 milliseconds before check again
            try:
                res.get(10)
                stmt_res = res.get_statement_result()
            except TimeoutException, te:
                # not yet ready
                pass
            except Exception, e:
                # something went wrong
                raise
        self.store.refresh_tables()
        expected = \
          "{'type' : 'table',"\
          "'name' : '" + self.table + "',"\
          "'owner': null,"\
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
        res = self.store.execute("DESC AS JSON TABLE " + self.table)
        stmt_res = res.get_statement_result()
        self.store.execute_sync("DROP TABLE IF EXISTS " + self.table)
        self.store.refresh_tables()
        self.assertEqual(expected.replace("\n", "").replace(" ", ""),
            str(stmt_res[ONDB_RESULT].get_string_result()).replace("\n", "").
            replace(" ", "").replace("\"", "'"))

    def testExecuteFutureCreateTableMap(self):
        stmt = "CREATE TABLE IF NOT EXISTS " + self.table + " ( "\
            "id INTEGER, myMap MAP(INTEGER), PRIMARY KEY (id) )"
        res = self.store.execute(stmt)
        stmt_res = res.get_statement_result()
        while (stmt_res[ONDB_IS_DONE] is not True):
            try:
                res.get()
                stmt_res = res.get_statement_result()
            except Exception, e:
                raise
        self.assertTrue(stmt_res[ONDB_IS_SUCCESSFUL])
        self.store.refresh_tables()
        row = Row({'id': 0, 'myMap': {'key1': 1, 'key2': 2}})
        self.store.put(self.table, row)
        p_key = Row({'id': 0})
        r_row = self.store.get(self.table, p_key)
        self.store.execute_sync("DROP TABLE IF EXISTS " + self.table)
        self.store.refresh_tables()
        self.assertEquals(r_row['myMap']['key1'], 1)
        self.assertEquals(r_row['myMap']['key2'], 2)

    def testExecuteFutureCancel(self):
        res = self.store.execute(
            "CREATE TABLE IF NOT EXISTS " + self.table + " (" +
            "shardKey INTEGER, id INTEGER, s STRING, " +
            "d DOUBLE, b BOOLEAN, date_of_sale RECORD(day_of_week ENUM(" +
            "sunday, monday,tuesday, wednesday, thursday, friday, saturday)," +
            " month INTEGER, day INTEGER, year INTEGER)," +
            "PRIMARY KEY (SHARD(shardKey), id) )")
        cancelled = res.cancel(True)
        self.assertTrue(cancelled)

    def testExecuteGetExecutionFuture(self):
        # test that get_execution_future() can build a
        # ExecutionFuture object from an execution_id
        res = self.store.execute("SHOW AS JSON TABLES")
        exec_id = res.get_execution_id()
        new_res = self.store.get_execution_future(exec_id)
        self.assertEqual(new_res.get_statement_result(), None)
        self.assertEqual(new_res.get_statement(), None)
        self.assertEqual(new_res.get_execution_id(), exec_id)

    def testExecuteGetExecutionFutureCheckStatus(self):
        # test that a reconstructed ExecutionFuture can be used
        # to check the status of the original call
        res = self.store.execute("SHOW AS JSON TABLES")
        exec_id = res.get_execution_id()
        new_res = self.store.get_execution_future(exec_id)
        new_res.update_status()
        stmt_res = new_res.get_statement_result()
        self.assertEqual(res.get_execution_id(), new_res.get_execution_id())
        self.assertEqual(res.get_statement(), new_res.get_statement())
        self.assertTrue(new_res.get_statement_result()[ONDB_IS_DONE])
        self.assertEqual(new_res.get_statement_result()[ONDB_IS_DONE],
            stmt_res[ONDB_IS_DONE])

    def testExecuteGetExecutionFutureErrorAtRetry(self):\
        # test that a reconstructed ExecutionFuture
        # return a ONDB_IS_DONE = True for a already
        # finished statement
        res = self.store.execute("SHOW AS JSON TABLES")
        exec_id = res.get_execution_id()
        new_res = self.store.get_execution_future(exec_id)
        new_res.get()
        stmt_res = new_res.get_statement_result()
        self.assertEqual(res.get_execution_id(), new_res.get_execution_id())
        self.assertEqual(res.get_statement(), new_res.get_statement())
        self.assertTrue(new_res.get_statement_result()[ONDB_IS_DONE])
        self.assertEqual(new_res.get_statement_result()[ONDB_IS_DONE],
            stmt_res[ONDB_IS_DONE])

    def testExecuteEmptyCommand(self):
        # test execute() with a empty command
        # expects an IllegalArgumentException
        self.assertRaises(IllegalArgumentException,
            self.store.execute,
            "")

    def testExecuteNoneCommand(self):
        # test execute() with a empty command
        # expects an IllegalArgumentException
        self.assertRaises(IllegalArgumentException,
            self.store.execute,
            None)


if __name__ == '__main__':
    add_runtime_params()
    unittest.main()
