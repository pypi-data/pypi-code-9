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
from testSetup import get_store
from testSetup import add_runtime_params
from testSetup import table_name
from testSetup import table_name2

import unittest


class TestTableKeysIterator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._store = get_store()
        cls._store.execute_sync("DROP INDEX IF EXISTS LastName ON " +
            table_name2 + "testTable")
        cls._store.execute_sync("DROP TABLE IF EXISTS " +
            table_name + "testTable")
        cls._store.execute_sync("DROP TABLE IF EXISTS " +
            table_name2 + "testTable")
        cls._store.refresh_tables()
        cls._store.execute_sync(
            "CREATE TABLE IF NOT EXISTS " + table_name + "testTable (" +
            "shardKey INTEGER, id INTEGER, s STRING, " +
            "PRIMARY KEY (SHARD(shardKey), id) )")
        cls._store.execute_sync(
            "CREATE TABLE IF NOT EXISTS " + table_name2 + "testTable" +
            " (id INTEGER, firstname STRING, lastname STRING, age INTEGER, " +
            "PRIMARY KEY (id) )")
        cls._store.execute_sync("CREATE INDEX IF NOT EXISTS LastName ON " +
            table_name2 + "testTable (lastname)")
        cls._store.refresh_tables()
        shardkeys = list(range(100))
        ids = list(range(100))
        ss = 'string'
        for sk in shardkeys:
            for i in ids:
                row = Row({'id': i,
                    's': ss + str(i * sk),
                    'shardKey': sk})
                cls._store.put(table_name + "testTable", row)
        cls._store.put(table_name2 + "testTable",
            Row({'id': 1, 'firstname': 'John',
                'lastname': 'Smith', 'age': 30}))
        cls._store.put(table_name2 + "testTable",
            Row({'id': 2, 'firstname': 'Marky',
                'lastname': 'Mark', 'age': 35}))
        cls._store.put(table_name2 + "testTable",
            Row({'id': 3, 'firstname': 'James',
                'lastname': 'Bond', 'age': 29}))

    @classmethod
    def tearDownClass(cls):
        cls._store.execute_sync("DROP INDEX IF EXISTS LastName ON " +
            table_name2 + "testTable")
        cls._store.execute_sync("DROP TABLE IF EXISTS " +
            table_name + "testTable")
        cls._store.execute_sync("DROP TABLE IF EXISTS " +
            table_name2 + "testTable")
        cls._store.refresh_tables()
        cls._store.close()

    def setUp(self):
        self.store = get_store()
        self.table = table_name + "TestTable"
        self.table2 = table_name2 + "TestTable"

    def tearDown(self):
        self.store.close()

    def testTableKeysIteratorOneShardkey(self):
        # test with an existing data from one shardkey
        self.row = {'shardKey': 0}
        count = 0
        it = self.store.table_iterator(self.table, self.row, True)
        for i in it:
            count += 1
        self.assertEqual(count, 100)

    def testTableKeysIteratorNonExistentShardkey(self):
        # test with a non existent shardkey
        self.row = {'shardKey': 200}
        count = 0
        it = self.store.table_iterator(self.table, self.row, True)
        for i in it:
            count += 1
        self.assertEqual(count, 0)

    def testTableKeysIteratorIndex(self):
        # test with an index
        count = 0
        it = self.store.index_iterator(self.table2, 'LastName', None, True)
        for i in it:
            count += 1
        self.assertEqual(count, 3)


if __name__ == '__main__':
    add_runtime_params()
    unittest.main()
