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
from nosqldb import Factory
from nosqldb import Store
from nosqldb import Row
from nosqldb import MultiRowOptions
from nosqldb import FieldRange
from nosqldb import ONDB_FIELD_RANGE
from nosqldb import ONDB_FIELD
from nosqldb import ONDB_START_VALUE
from nosqldb import ONDB_END_VALUE
from nosqldb import ONDB_START_INCLUSIVE
from nosqldb import ONDB_END_INCLUSIVE
from nosqldb import ConnectionException
from nosqldb import IllegalArgumentException
from nosqldb import RequestTimeoutException
from testSetup import get_store
from testSetup import get_kvstore_config
from testSetup import get_kvproxy_config
from testSetup import add_runtime_params
from testSetup import table_name
import unittest


class TestMultiGetKeys(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._store = get_store()
        cls._store.execute_sync("DROP TABLE IF EXISTS " + table_name +
            ".childTable")
        cls._store.execute_sync("DROP TABLE IF EXISTS " + table_name)
        cls._store.refresh_tables()
        cls._store.execute_sync(
            "CREATE TABLE IF NOT EXISTS " + table_name + " (" +
            "shardKey INTEGER, id INTEGER, s String, " +
            "PRIMARY KEY (SHARD(shardKey), id) )")
        cls._store.execute_sync(
            "CREATE TABLE IF NOT EXISTS " + table_name +
            ".childTable (cid INTEGER, notes STRING, " +
            "locations ARRAY(RECORD (shelf INTEGER, drawer INTEGER, " +
            "condition ENUM(Poor, Fair, Good))), " +
            "PRIMARY KEY(cid))")
        cls._store.refresh_tables()

    @classmethod
    def tearDownClass(cls):
        cls._store.execute_sync("DROP TABLE IF EXISTS " + table_name +
            ".childTable")
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
        self.products = ['strawberries', 'pears', 'apples', 'grapes',
            'lemons', 'oranges']
        self.notes = [
            'Locations and conditions for strawberries',
            'Locations and conditions for pearls',
            'Locations and conditions for apples',
            'Locations and conditions for grapes',
            'Locations and conditions for lemons',
            'Locations and conditions for oranges']
        self.loc_shelfs = [1, 1, 2, 4, 2, 1]
        self.loc_drawers = [1, 2, 1, 3, 2, 2]
        self.loc_conditions = ['Good', 'Good', 'Fair', 'Poor', 'Fair', 'Good']
        for sk in self.shardkeys:
            if (sk != 2):
                for i in self.ids:
                    self.row = Row({'id': i, 's': self.ss[i], 'shardKey': sk})
                    self.store.put(self.table, self.row)
            else:
                for i in self.ids:
                    self.row = Row({'id': i, 's': self.products[i],
                        'shardKey': sk})
                    self.row2 = Row({
                        'id': i,
                        'shardKey': sk,
                        'cid': 0,
                        'notes': self.notes[i],
                        'locations': [
                            {
                                'shelf': self.loc_shelfs[i],
                                'drawer': self.loc_drawers[i],
                                'condition': self.loc_conditions[i]
                            }
                        ]})
                    self.store.put(self.table, self.row)
                    self.store.put(self.table + ".childTable", self.row2)

    def tearDown(self):
        for sk in self.shardkeys:
            self.row = Row({'shardKey': sk})
            self.store.multi_delete(self.table, self.row)
        self.store.close()

    def testMultigetOnlyOneShardKey(self):
        # test to get all data in shardKey 0 and id 0
        self.row = Row({'shardKey': 0})
        res = self.store.multi_get(self.table, self.row, True)
        self.assertEqual(len(res), 6)

    def testMultigetOnlyOneId(self):
        # test to get all values with id: 4
        # expect IllegalArgumentException since ShardKey is missing from
        # the partial key
        self.row = Row({'id': 4})
        self.assertRaises(IllegalArgumentException, self.store.multi_get,
                          self.table, self.row, True)

    def testMultigetFieldRangeRegular(self):
        # test multiget with FieldRange regular
        multirowopts = MultiRowOptions({
            ONDB_FIELD_RANGE: FieldRange({
                ONDB_FIELD: 'id',
                ONDB_START_VALUE: '1',
                ONDB_END_VALUE: '3'})})
        self.row = Row({'shardKey': 0})
        res = self.store.multi_get(self.table, self.row, True, multirowopts)
        self.assertEqual(len(res), 1)

    def testMultigetFieldRangeInclusive(self):
        # test that ONDB_START_INCLUSIVE and ONDB_END_INCLUSIVE
        # actually forces to multiget to include both start and end
        # values
        multirowopts = MultiRowOptions({
            ONDB_FIELD_RANGE: FieldRange({
                ONDB_FIELD: 'id',
                ONDB_START_VALUE: '1',
                ONDB_END_VALUE: '3',
                ONDB_START_INCLUSIVE: True,
                ONDB_END_INCLUSIVE: True})})
        self.row = Row({'shardKey': 0})
        res = self.store.multi_get(self.table, self.row, True, multirowopts)
        all_good = True
        for r in res:
            if (r['id'] == 1):
                if (r['shardKey'] != 0):
                    all_good = False
                    break
            elif (r['id'] == 2):
                if (r['shardKey'] != 0):
                    all_good = False
                    break
            elif (r['id'] == 3):
                if (r['shardKey'] != 0):
                    all_good = False
                    break
        self.assertEqual(len(res), 3)
        self.assertTrue(all_good)

    def testMultigetFieldRangeStartOnly(self):
        multirowopts = MultiRowOptions({
            ONDB_FIELD_RANGE: FieldRange({
                ONDB_FIELD: 'id',
                ONDB_START_VALUE: '4'})})
        self.row = Row({'shardKey': 0})
        res = self.store.multi_get(self.table, self.row, True, multirowopts)
        all_good = True
        self.assertEqual(len(res), 1)
        for r in res:
            # expect to get only one row
            if (r['id'] != 5):
                all_good = False
            if (r['shardKey'] != 0):
                all_good = False
        self.assertTrue(all_good)

    def testMultigetFieldRangeEndOnly(self):
        multirowopts = MultiRowOptions({
            ONDB_FIELD_RANGE: FieldRange({
                ONDB_FIELD: 'id',
                ONDB_END_VALUE: '1'})})
        self.row = Row({'shardKey': 0})
        res = self.store.multi_get(self.table, self.row, True, multirowopts)
        all_good = True
        self.assertEqual(len(res), 1)
        for r in res:
            # expect to get only one row
            if (r['id'] != 0):
                all_good = False
            if (r['shardKey'] != 0):
                all_good = False
        self.assertTrue(all_good)

    def testMultigetDataRead(self):
        # test that multiget returns the expected data
        multirowopts = MultiRowOptions({
            ONDB_FIELD_RANGE: FieldRange({
                ONDB_FIELD: 'id',
                ONDB_START_VALUE: '0',
                ONDB_END_VALUE: '1',
                ONDB_START_INCLUSIVE: True})})
        self.row = Row({'shardKey': 1})
        res = self.store.multi_get(self.table, self.row, True, multirowopts)
        all_good = True
        self.assertEqual(len(res), 1)
        for r in res:
            # expect to get only one row
            if (r['id'] != 0):
                all_good = False
            if (r['shardKey'] != 1):
                all_good = False
        self.assertTrue(all_good)

    def testMultigetReadParentChildData(self):
        # test that multiget can get data from
        # a child table
        multirowopts = MultiRowOptions({
            ONDB_FIELD_RANGE: FieldRange({
                ONDB_FIELD: 'id',
                ONDB_START_VALUE: '0',
                ONDB_END_VALUE: '1',
                ONDB_START_INCLUSIVE: True})})
        self.row = Row({'shardKey': 2})
        res = self.store.multi_get(self.table + ".childTable", self.row, True,
            multirowopts)
        all_good = True
        self.assertEqual(len(res), 1)
        for r in res:
            # expect to get only one row
            if (r['id'] != 0):
                all_good = False
            if (r['shardKey'] != 2):
                all_good = False
            if (r['cid'] != 0):
                all_good = False
        self.assertTrue(all_good)

    def testMultigetNoStartEndValues(self):
        # test that when there is no ONDB_START_VALUE nor
        # ONDB_END_VALUE then multiget raises an IllegalArgumentException
        multirowopts = MultiRowOptions({
            ONDB_FIELD_RANGE: FieldRange({
                ONDB_FIELD: 'id',
                ONDB_START_INCLUSIVE: True})})
        self.row = Row({'shardKey': 0})
        self.assertRaises(IllegalArgumentException, self.store.multi_get,
            self.table, self.row, True, multirowopts)


if __name__ == '__main__':
    add_runtime_params()
    unittest.main()
