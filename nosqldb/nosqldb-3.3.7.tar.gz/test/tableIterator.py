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
from nosqldb import TableIteratorOptions
from nosqldb import ONDB_INCLUDED_TABLES
from nosqldb import ONDB_DIRECTION
from nosqldb import ONDB_READ_OPTIONS
from nosqldb import ONDB_CONSISTENCY
from nosqldb import ABSOLUTE
from nosqldb import NONE_REQUIRED
from nosqldb import NONE_REQUIRED_NO_MASTER
from nosqldb import ONDB_TIMEOUT
from nosqldb import ConnectionException
from nosqldb import IllegalArgumentException
from nosqldb import RequestTimeoutException
from testSetup import get_store
from testSetup import get_kvstore_config
from testSetup import get_kvproxy_config
from testSetup import add_runtime_params
from testSetup import table_name
from testSetup import host_port

import unittest


class TestTableIterator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._store = get_store()
        cls._store.execute_sync("DROP TABLE IF EXISTS " +
            table_name + "testTable.childTable.grandChildTable")
        cls._store.execute_sync("DROP TABLE IF EXISTS " +
            table_name + "testTable.childTable")
        cls._store.execute_sync("DROP TABLE IF EXISTS " +
            table_name + "testTable")
        cls._store.refresh_tables()
        cls._store.execute_sync(
            "CREATE TABLE IF NOT EXISTS " + table_name + "testTable (" +
            "shardKey INTEGER, id INTEGER, s STRING, " +
            "PRIMARY KEY (SHARD(shardKey), id) )")
        cls._store.execute_sync(
            "CREATE TABLE IF NOT EXISTS " + table_name +
            "testTable.childTable (" +
            "cid INTEGER, phoneCat ENUM (Home, Office, Cell, Other), " +
            "phone STRING, PRIMARY KEY (cid))")
        cls._store.execute_sync(
            "CREATE TABLE IF NOT EXISTS " + table_name +
            "testTable.childTable.grandChildTable (" +
            "bid INTEGER, billAddress STRING, billAmount DOUBLE," +
            "PRIMARY KEY(bid))")
        cls._store.refresh_tables()
        shardkeys = list(range(50))
        ids = list(range(50))
        ss = ['John', 'Mike', 'Jen', 'Rossy']
        phoneCats = ['Office', 'Other', 'Home', 'Cell']
        phones = ['123-1234', '555-2375', '111-0987', '1010-2442']
        billAddresses = ['123 First Ave', '301 Lake Rd', '789 Grand St',
            '555 Fourth St']
        billAmounts = [399.99, 149.99, 129.99, 269.99]
        for sk in shardkeys:
            for i in ids:
                row = Row({
                    'id': i,
                    's': ss[i % len(ss)] + str((i * sk) % len(ss)),
                    'shardKey': sk})
                cls._store.put(table_name + "testTable", row)
                row2 = Row({
                    'id': i,
                    'shardKey': sk,
                    'cid': 0,
                    'phoneCat': phoneCats[i % len(phoneCats)],
                    'phone': phones[i % len(phones)]})
                cls._store.put(table_name + "testTable.childTable", row2)
                row3 = Row({
                    'id': i,
                    'shardKey': sk,
                    'cid': 0,
                    'bid': 0,
                    'billAddress': billAddresses[i % len(billAddresses)],
                    'billAmount': billAmounts[i % len(billAmounts)]})
                cls._store.put(
                    table_name + "testTable.childTable.grandChildTable",
                    row3)

    @classmethod
    def tearDownClass(cls):
        cls._store.execute_sync("DROP TABLE IF EXISTS " +
            table_name + "testTable.childTable.grandChildTable")
        cls._store.execute_sync("DROP TABLE IF EXISTS " +
            table_name + "testTable.childTable")
        cls._store.execute_sync("DROP TABLE IF EXISTS " +
            table_name + "testTable")
        cls._store.refresh_tables()
        cls._store.close()

    def setUp(self):
        s_config = get_kvstore_config()
        p_config = get_kvproxy_config()
        s_config.set_max_results(25)
        s_config.set_request_timeout(100)
        self.store = Factory.open(host_port, s_config, p_config)
        self.table = table_name + "testTable"

    def tearDown(self):
        self.store.close()

    def testTableIteratorOneShardkey(self):
        # test with an existing data from one shardkey
        self.row = {'shardKey': 0}
        count = 0
        it = self.store.table_iterator(self.table, self.row, False)
        for i in it:
            count += 1
        self.assertEqual(count, 50)

    def testTableIteratorNonExistentShardkey(self):
        # test with a non existent shardkey
        row = {'shardKey': 200}
        count = 0
        it = self.store.table_iterator(self.table, row, False)
        for i in it:
            count += 1
        self.assertEqual(count, 0)

    def testTableIteratorReadParentChildData(self):
        # test that multiget can get data from
        # parent and child tables
        multirowopts = MultiRowOptions({
            ONDB_INCLUDED_TABLES: [self.table + '.childTable']
            })
        self.row = Row({'shardKey': 2})
        res = self.store.table_iterator(self.table, self.row, False,
            multirowopts)
        all_good = True
        count1 = 0
        count2 = 0
        for r in res:
            # check the first and the last of both tables
            if (r.get_table_name() == self.table):
                count1 += 1
                if (r['id'] == 0):
                    if (r['shardKey'] != 2):
                        all_good = False
                        break
                    if (r['s'] != 'John0'):
                        all_good = False
                        break
                elif (r['id'] == 49):
                    if (r['shardKey'] != 2):
                        all_good = False
                        break
                    if (r['s'] != 'Mike2'):
                        all_good = False
                        break
            elif (r.get_table_name() == self.table + '.childTable'):
                count2 += 1
                if(r['id'] == 0):
                    if (r['shardKey'] != 2):
                        all_good = False
                        break
                    if (r['cid'] != 0):
                        all_good = False
                        break
                    if (r['phoneCat'] != 'Office'):
                        all_good = False
                        break
                    if (r['phone'] != '123-1234'):
                        all_good = False
                        break
                elif (r['id'] == 49):
                    if (r['shardKey'] != 2):
                        all_good = False
                        break
                    if (r['cid'] != 0):
                        all_good = False
                        break
                    if (r['phoneCat'] != 'Other'):
                        all_good = False
                        break
                    if (r['phone'] != '555-2375'):
                        all_good = False
                        break
        self.assertEqual(count1, 50)
        self.assertEqual(count2, 50)
        self.assertTrue(all_good)

    def testTableIteratorReadAllTablesData(self):
        # test that multiget can get data from
        # parent and all descendants
        multirowopts = MultiRowOptions({
            ONDB_INCLUDED_TABLES: [self.table + '.childTable',
                self.table + '.childTable.grandChildTable']
            })
        self.row = Row({'shardKey': 2})
        res = self.store.table_iterator(self.table, self.row, False,
            multirowopts)
        all_good = True
        count1 = 0
        count2 = 0
        count3 = 0
        for r in res:
            # check the first and the last of both tables
            if (r.get_table_name() == self.table):
                count1 += 1
                if (r['id'] == 0):
                    if (r['shardKey'] != 2):
                        all_good = False
                        break
                    if (r['s'] != 'John0'):
                        all_good = False
                        break
                elif (r['id'] == 49):
                    if (r['shardKey'] != 2):
                        all_good = False
                        break
                    if (r['s'] != 'Mike2'):
                        all_good = False
                        break
            elif (r.get_table_name() == self.table + '.childTable'):
                count2 += 1
                if(r['id'] == 0):
                    if (r['shardKey'] != 2):
                        all_good = False
                        break
                    if (r['cid'] != 0):
                        all_good = False
                        break
                    if (r['phoneCat'] != 'Office'):
                        all_good = False
                        break
                    if (r['phone'] != '123-1234'):
                        all_good = False
                        break
                elif (r['id'] == 49):
                    if (r['shardKey'] != 2):
                        all_good = False
                        break
                    if (r['cid'] != 0):
                        all_good = False
                        break
                    if (r['phoneCat'] != 'Other'):
                        all_good = False
                        break
                    if (r['phone'] != '555-2375'):
                        all_good = False
                        break
            elif (r.get_table_name() == self.table +
                '.childTable.grandChildTable'):
                    count3 += 1
                    if(r['id'] == 0):
                        if (r['shardKey'] != 2):
                            all_good = False
                            break
                        if (r['bid'] != 0):
                            all_good = False
                            break
                        if (r['billAddress'] != '123 First Ave'):
                            all_good = False
                            break
                        if (r['billAmount'] != 399.99):
                            all_good = False
                            break
                    elif (r['id'] == 49):
                        if (r['shardKey'] != 2):
                            all_good = False
                            break
                        if (r['bid'] != 0):
                            all_good = False
                            break
                        if (r['billAddress'] != '301 Lake Rd'):
                            all_good = False
                            break
                        if (r['billAmount'] != 149.99):
                            all_good = False
                            break
        self.assertEqual(count1, 50)
        self.assertEqual(count2, 50)
        self.assertEqual(count3, 50)
        self.assertTrue(all_good)

    def testTableIteratorReadFromChild(self):
        # test that multiget can get data from
        # parent and all descendants
        multirowopts = MultiRowOptions({
            ONDB_INCLUDED_TABLES: [self.table,
                self.table + '.childTable.grandChildTable']
            })
        self.row = Row({'shardKey': 2})
        res = self.store.table_iterator(self.table + ".childTable",
            self.row, False,
            multirowopts)
        all_good = True
        count1 = 0
        count2 = 0
        count3 = 0
        for r in res:
            # check the first and the last of both tables
            if (r.get_table_name() == self.table):
                count1 += 1
                if (r['id'] == 0):
                    if (r['shardKey'] != 2):
                        all_good = False
                        break
                    if (r['s'] != 'John0'):
                        all_good = False
                        break
                elif (r['id'] == 49):
                    if (r['shardKey'] != 2):
                        all_good = False
                        break
                    if (r['s'] != 'Mike2'):
                        all_good = False
                        break
            elif (r.get_table_name() == self.table + '.childTable'):
                count2 += 1
                if(r['id'] == 0):
                    if (r['shardKey'] != 2):
                        all_good = False
                        break
                    if (r['cid'] != 0):
                        all_good = False
                        break
                    if (r['phoneCat'] != 'Office'):
                        all_good = False
                        break
                    if (r['phone'] != '123-1234'):
                        all_good = False
                        break
                elif (r['id'] == 49):
                    if (r['shardKey'] != 2):
                        all_good = False
                        break
                    if (r['cid'] != 0):
                        all_good = False
                        break
                    if (r['phoneCat'] != 'Other'):
                        all_good = False
                        break
                    if (r['phone'] != '555-2375'):
                        all_good = False
                        break
            elif (r.get_table_name() == self.table +
                '.childTable.grandChildTable'):
                    count3 += 1
                    if(r['id'] == 0):
                        if (r['shardKey'] != 2):
                            all_good = False
                            break
                        if (r['bid'] != 0):
                            all_good = False
                            break
                        if (r['billAddress'] != '123 First Ave'):
                            all_good = False
                            break
                        if (r['billAmount'] != 399.99):
                            all_good = False
                            break
                    elif (r['id'] == 49):
                        if (r['shardKey'] != 2):
                            all_good = False
                            break
                        if (r['bid'] != 0):
                            all_good = False
                            break
                        if (r['billAddress'] != '301 Lake Rd'):
                            all_good = False
                            break
                        if (r['billAmount'] != 149.99):
                            all_good = False
                            break
        self.assertEqual(count1, 50)
        self.assertEqual(count2, 50)
        self.assertEqual(count3, 50)
        self.assertTrue(all_good)

    def testTableIteratorReadFromGrandChild(self):
        # test that multiget can get data from
        # parent and all descendants
        multirowopts = MultiRowOptions({
            ONDB_INCLUDED_TABLES: [self.table,
                self.table + '.childTable']
            })
        self.row = Row({'shardKey': 2})
        res = self.store.table_iterator(
            self.table + ".childTable.grandChildTable",
            self.row, False,
            multirowopts)
        all_good = True
        count1 = 0
        count2 = 0
        count3 = 0
        for r in res:
            # check the first and the last of both tables
            if (r.get_table_name() == self.table):
                count1 += 1
                if (r['id'] == 0):
                    if (r['shardKey'] != 2):
                        all_good = False
                        break
                    if (r['s'] != 'John0'):
                        all_good = False
                        break
                elif (r['id'] == 49):
                    if (r['shardKey'] != 2):
                        all_good = False
                        break
                    if (r['s'] != 'Mike2'):
                        all_good = False
                        break
            elif (r.get_table_name() == self.table + '.childTable'):
                count2 += 1
                if(r['id'] == 0):
                    if (r['shardKey'] != 2):
                        all_good = False
                        break
                    if (r['cid'] != 0):
                        all_good = False
                        break
                    if (r['phoneCat'] != 'Office'):
                        all_good = False
                        break
                    if (r['phone'] != '123-1234'):
                        all_good = False
                        break
                elif (r['id'] == 49):
                    if (r['shardKey'] != 2):
                        all_good = False
                        break
                    if (r['cid'] != 0):
                        all_good = False
                        break
                    if (r['phoneCat'] != 'Other'):
                        all_good = False
                        break
                    if (r['phone'] != '555-2375'):
                        all_good = False
                        break
            elif (r.get_table_name() == self.table +
                '.childTable.grandChildTable'):
                    count3 += 1
                    if(r['id'] == 0):
                        if (r['shardKey'] != 2):
                            all_good = False
                            break
                        if (r['bid'] != 0):
                            all_good = False
                            break
                        if (r['billAddress'] != '123 First Ave'):
                            all_good = False
                            break
                        if (r['billAmount'] != 399.99):
                            all_good = False
                            break
                    elif (r['id'] == 49):
                        if (r['shardKey'] != 2):
                            all_good = False
                            break
                        if (r['bid'] != 0):
                            all_good = False
                            break
                        if (r['billAddress'] != '301 Lake Rd'):
                            all_good = False
                            break
                        if (r['billAmount'] != 149.99):
                            all_good = False
                            break
        self.assertEqual(count1, 50)
        self.assertEqual(count2, 50)
        self.assertEqual(count3, 50)
        self.assertTrue(all_good)

    def testTableIteratorForward(self):
        # test with ONDB_DIRECTION = FORWARD
        self.row = {'shardKey': 0}
        t_iterator_opts = TableIteratorOptions({
            ONDB_DIRECTION: {ONDB_DIRECTION: 'FORWARD'}
            })
        count = 0
        it = self.store.table_iterator(self.table, self.row, False, None,
            t_iterator_opts)
        old_id = -1
        all_good = True
        for i in it:
            count += 1
            if (i['id'] < old_id):
                all_good = False
                break
            else:
                old_id = i['id']
        self.assertTrue(all_good)
        self.assertEqual(count, 50)

    def testTableIteratorReverse(self):
        # test with ONDB_DIRECTION = REVERSE
        self.row = {'shardKey': 0}
        t_iterator_opts = TableIteratorOptions({
            ONDB_DIRECTION: {ONDB_DIRECTION: 'REVERSE'}
            })
        count = 0
        it = self.store.table_iterator(self.table, self.row, False, None,
            t_iterator_opts)
        old_id = 10000
        all_good = True
        for i in it:
            count += 1
            if (i['id'] > old_id):
                all_good = False
                #break
            else:
                old_id = i['id']
        self.assertTrue(all_good)
        self.assertEqual(count, 50)

    def testTableIteratorUnordered(self):
        # test with ONDB_DIRECTION = UNORDERED
        self.row = {'shardKey': 0}
        t_iterator_opts = TableIteratorOptions({
            ONDB_DIRECTION: {ONDB_DIRECTION: 'UNORDERED'}
            })
        count = 0
        it = self.store.table_iterator(self.table, self.row, False, None,
            t_iterator_opts)
        for i in it:
            count += 1
        self.assertEqual(count, 50)

    def testTableIteratorConsistencyAbsolute(self):
        # test with ONDB_CONSISTENCY = ABSOLUTE
        self.row = {'shardKey': 0}
        t_iterator_opts = TableIteratorOptions({
            ONDB_DIRECTION: {ONDB_DIRECTION: 'FORWARD'},
            ONDB_READ_OPTIONS: {ONDB_CONSISTENCY: ABSOLUTE}
            })
        count = 0
        it = self.store.table_iterator(self.table, self.row, False, None,
            t_iterator_opts)
        for i in it:
            count += 1
        self.assertEqual(count, 50)

    def testTableIteratorConsistencyNoneRequired(self):
        # test with ONDB_READ_OPTIONS = NONE_REQUIRED
        self.row = {'shardKey': 0}
        t_iterator_opts = TableIteratorOptions({
            ONDB_DIRECTION: {ONDB_DIRECTION: 'FORWARD'},
            ONDB_READ_OPTIONS: {ONDB_CONSISTENCY: NONE_REQUIRED}
            })
        count = 0
        it = self.store.table_iterator(self.table, self.row, False, None,
            t_iterator_opts)
        for i in it:
            count += 1
        self.assertEqual(count, 50)

    def testTableIteratorConsistencyNoneRequiredNoMaster(self):
        # test with ONDB_READ_OPTIONS = NONE_REQUIRED_NO_MASTER
        self.row = {'shardKey': 0}
        t_iterator_opts = TableIteratorOptions({
            ONDB_DIRECTION: {ONDB_DIRECTION: 'FORWARD'},
            ONDB_READ_OPTIONS: {ONDB_CONSISTENCY: NONE_REQUIRED_NO_MASTER}
            })
        count = 0
        it = self.store.table_iterator(self.table, self.row, False, None,
            t_iterator_opts)
        for i in it:
            count += 1
        self.assertEqual(count, 50)

    def testTableIteratorTimeout(self):
        # test with ONDB_TIMEOUT = 10
        self.row = {'shardKey': 0}
        t_iterator_opts = TableIteratorOptions({
            ONDB_DIRECTION: {ONDB_DIRECTION: 'FORWARD'},
            ONDB_READ_OPTIONS: {ONDB_TIMEOUT: 10}
            })
        count = 0
        it = self.store.table_iterator(self.table, self.row, False, None,
            t_iterator_opts)
        for i in it:
            count += 1
        self.assertEqual(count, 50)


if __name__ == '__main__':
    add_runtime_params()
    unittest.main()
