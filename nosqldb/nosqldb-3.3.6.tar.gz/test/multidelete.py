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
from nosqldb import MultiRowOptions
from nosqldb import FieldRange
from nosqldb import ONDB_FIELD_RANGE
from nosqldb import ONDB_FIELD
from nosqldb import ONDB_START_VALUE
from nosqldb import ONDB_END_VALUE
from nosqldb import ConnectionException
from nosqldb import IllegalArgumentException
from nosqldb import RequestTimeoutException
from testSetup import get_store
from testSetup import add_runtime_params
from testSetup import table_name
import unittest


class testMultiDelete(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._store = get_store()
        cls._store.execute_sync("DROP TABLE IF EXISTS " + table_name)
        cls._store.refresh_tables()
        cls._store.execute_sync(
            "CREATE TABLE IF NOT EXISTS " + table_name + " (" +
            "shardKey INTEGER, id INTEGER, s String, " +
            "PRIMARY KEY (SHARD(shardKey), id) )")
        cls._store.refresh_tables()

    @classmethod
    def tearDownClass(cls):
        cls._store.execute_sync("DROP TABLE IF EXISTS " + table_name)
        cls._store.refresh_tables()
        cls._store.close()

    def setUp(self):
        self.store = get_store()
        self.table = table_name
        self.shardkeys = [0, 1, 2]
        self.ids = [0, 1, 2, 3, 4, 5]
        self.ss = ['string0', 'string1', 'string2', 'string3', 'string4',
                   'string5']
        for sk in self.shardkeys:
            for i in self.ids:
                self.row = Row({'id': i, 's': self.ss[i], 'shardKey': sk})
                self.store.put(self.table, self.row)

    def tearDown(self):
        for sk in self.shardkeys:
            self.row = {'shardKey': sk}
            self.store.multi_delete(self.table, self.row)
        self.store.close()

    def testMultideleteOnlyOneShardKey(self):
        # test to get all data in shardKey 0 and id 0
        self.row = Row({'shardKey': 0})
        res = self.store.multi_get(self.table, self.row, True)
        self.assertEqual(len(res), 6)

    def testMultigetdeleteOnlyOneId(self):
        # test to get all values with id: 4
        # expect IllegalArgumentException since ShardKey is missing from
        # the partial key
        self.row = Row({'id': 4})
        self.assertRaises(IllegalArgumentException, self.store.multi_delete,
                          self.table, self.row)

    def testMultigetdeleteFieldRangeRegular(self):
        # test multiget with FieldRange regular
        multirowopts = MultiRowOptions({
            ONDB_FIELD_RANGE: FieldRange({
                ONDB_FIELD: 'id',
                ONDB_START_VALUE: '1',
                ONDB_END_VALUE: '3'})})
        self.row = Row({'shardKey': 0})
        res = self.store.multi_delete(self.table, self.row, multirowopts)
        self.assertEqual(res, 1)

if __name__ == '__main__':
    add_runtime_params()
    unittest.main()
