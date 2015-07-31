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
from nosqldb import TableIteratorOptions
from nosqldb import ONDB_DIRECTION
from nosqldb import ConnectionException
from nosqldb import IllegalArgumentException
from nosqldb import RequestTimeoutException
from testSetup import get_store
from testSetup import add_runtime_params
from testSetup import table_name
from testSetup import table_name2

import unittest


class TestIndexKeysIterator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._store = get_store()
        cls._store.execute_sync("DROP INDEX IF EXISTS LastName ON " +
            table_name + "testTable")
        cls._store.execute_sync("DROP TABLE IF EXISTS " + table_name +
            "testTable.addressesChildTable")
        cls._store.execute_sync("DROP TABLE IF EXISTS " + table_name +
            "testTable")
        cls._store.refresh_tables()
        cls._store.execute_sync(
            "CREATE TABLE IF NOT EXISTS " + table_name + "testTable (" +
            "id INTEGER, lastName STRING, surname STRING, age INTEGER, " +
            "arrNumbers ARRAY(INTEGER), mapNumbers MAP(INTEGER), " +
            "recNumbers RECORD(firstInt INTEGER, secondInt INTEGER), " +
            "PRIMARY KEY (id) )")
        cls._store.execute_sync(
            "CREATE TABLE IF NOT EXISTS " + table_name +
            "testTable.addressesChildTable " +
            "(addressName STRING, address STRING," +
            " zipCode INTEGER CHECK( zipCode > 0 and zipCode < 99999)," +
            " phone STRING,"
            " PRIMARY KEY (phone) )")
        cls._store.execute_sync("CREATE INDEX IF NOT EXISTS LastName ON " +
            table_name + "testTable (lastName)")
        cls._store.execute_sync("CREATE INDEX IF NOT EXISTS indexArrNumbers" +
            " ON " + table_name + "testTable (arrNumbers)")
        cls._store.execute_sync("CREATE INDEX IF NOT EXISTS indexMapNumbers" +
            " ON " + table_name + "testTable (KEYOF(mapNumbers)," +
            " ELEMENTOF(mapNumbers))")
        cls._store.execute_sync("CREATE INDEX IF NOT EXISTS indexRecNumbers" +
            " ON " + table_name + "testTable (recNumbers.firstInt)")
        cls._store.refresh_tables()
        names = ['John', 'Tod', 'Carl', 'Mike', 'Ralph']
        last_names = ['Smith', 'Doe', 'Roberts', 'Appleton', 'Harbor']
        ages = [30, 22, 31, 29, 25]
        number_arr = [[1, 2, 3, 4, 5], [5, 4, 3, 2, 1], [3, 1, 5, 2, 4],
            [2, 3, 4, 5, 1], [4, 5, 1, 2, 3]]
        number_map = [{'field1': 1, 'field2': 2, 'field3': 3}, {'field1': 3,
            'field2': 2, 'field3': 1}, {'field1': 4, 'field2': 5, 'field3': 6},
            {'field1': 6, 'field2': 5, 'field3': 4}, {'field1': 2,
            'field2': 4, 'field3': 6}]
        number_rec = [{'firstInt': 1, 'secondInt': 2},
            {'firstInt': 2, 'secondInt': 1}, {'firstInt': 3, 'secondInt': 4},
            {'firstInt': 4, 'secondInt': 3}, {'firstInt': 5, 'secondInt': 1}]
        addr_names = ['HOME', 'WORK']
        streets = ['First Avenue', 'Washington Street', 'Elm Street',
            'Evergreen Street', 'Baker Street']
        zips = [10001, 45066, 33170, 98712, 90210]
        phones = ['123-1234', '333-8127', '555-1234', '100-2200', '999-0011']
        names_size = len(names)
        lasts_size = len(last_names)
        ages_size = len(ages)
        num_arr_size = len(number_arr)
        num_map_size = len(number_map)
        num_rec_size = len(number_rec)
        streets_size = len(streets)
        zips_size = len(zips)
        phones_size = len(phones)
        addrs_size = len(addr_names)
        for i in range(names_size * lasts_size):
            row = Row({'id': i, 'lastName': last_names[i % lasts_size],
                'surname': names[i / names_size], 'age': ages[i % ages_size],
                'arrNumbers': number_arr[i / num_arr_size],
                'mapNumbers': number_map[i / num_map_size],
                'recNumbers': number_rec[i / num_rec_size]})
            cls._store.put(table_name + 'testTable', row)
            for j in range(addrs_size * streets_size):
                row2 = Row({
                    'id': i,
                    'addressName': addr_names[i % addrs_size],
                    'address': streets[i % streets_size],
                    'zipCode': zips[i % zips_size],
                    'phone': phones[i % phones_size]})
                cls._store.put(table_name + 'testTable.addressesChildTable',
                    row2)

    @classmethod
    def tearDownClass(cls):
        cls._store.execute_sync("DROP INDEX IF EXISTS LastName ON " +
            table_name + "testTable")
        cls._store.execute_sync("DROP INDEX IF EXISTS indexArrNumbers ON " +
            table_name + "testTable")
        cls._store.execute_sync("DROP INDEX IF EXISTS indexMapNumbers ON " +
            table_name + "testTable")
        cls._store.execute_sync("DROP INDEX IF EXISTS indexRecNumbers ON " +
            table_name + "testTable")
        cls._store.execute_sync("DROP TABLE IF EXISTS " +
            table_name + "testTable.addressesChildTable")
        cls._store.execute_sync("DROP TABLE IF EXISTS " +
            table_name + "testTable")
        cls._store.refresh_tables()
        cls._store.close()

    def setUp(self):
        self.store = get_store()
        self.table = table_name + "testTable"
        self.childTable = table_name + "testTable.addressesChildTable"

    def tearDown(self):
        self.store.close()

    def testIndexIteratorOneLastnameOnly(self):
        # test string index and one row
        row = {'lastName': 'Smith'}
        count = 0
        index = 'LastName'
        it = self.store.index_iterator(self.table, index, row, True)
        all_good = True
        for i in it:
            count += 1
            if (i['lastName'] != 'Smith'):
                all_good = False
                break
        self.assertTrue(all_good)
        self.assertEqual(count, 5)

    def testIndexIteratorNonExistentLastname(self):
        # test with string index and a non existent id
        row = {'lastName': 'Burns'}
        count = 0
        index = 'LastName'
        it = self.store.index_iterator(self.table, index, row, True)
        for i in it:
            count += 1
        self.assertEqual(count, 0)

    def testIndexIteratorNoRow(self):
        # test with string index and no row
        count = 0
        index = 'LastName'
        it = self.store.index_iterator(self.table, index, None, True)
        all_good = True
        for i in it:
            count += 1
            if (i['id'] == 0):
                if (i['lastName'] != 'Smith'):
                    all_good = False
                    break
            if (i['id'] == 24):
                if (i['lastName'] != 'Harbor'):
                    all_good = False
                    break
        self.assertTrue(all_good)
        self.assertEqual(count, 25)

    def testIndexIteratorOneArrayOnly(self):
        # test Array index and one row
        row = {'arrNumbers': [1]}
        count = 0
        index = 'indexArrNumbers'
        it = self.store.index_iterator(self.table, index, row, True)
        for i in it:
            count += 1
        self.assertEqual(count, 25)

    def testIndexIteratorNonExistentArray(self):
        # test with Array index and a non existent row
        row = {'arrNumbers': [101]}
        count = 0
        index = 'indexArrNumbers'
        it = self.store.index_iterator(self.table, index, row, True)
        for i in it:
            count += 1
        self.assertEqual(count, 0)

    def testIndexIteratorArrayNoRow(self):
        # test Array index and no row
        count = 0
        index = 'indexArrNumbers'
        it = self.store.index_iterator(self.table, index, None, True)
        for i in it:
            count += 1
        self.assertEqual(count, 125)

    def testIndexIteratorOneMapOnly(self):
        # test with Map index and a single row
        row = {'mapNumbers': {'field1': None, '[]': 3}}
        count = 0
        index = 'indexMapNumbers'
        it = self.store.index_iterator(self.table, index, row, True)
        for i in it:
            count += 1
        self.assertEqual(count, 5)

    def testIndexIteratorNonExistentMap(self):
        # test with Map index and a non existent row
        row = {'mapNumbers': {'field10': 10}}
        count = 0
        index = 'indexMapNumbers'
        it = self.store.index_iterator(self.table, index, row, True)
        for i in it:
            count += 1
        self.assertEqual(count, 0)

    def testIndexIteratorMapNoRow(self):
        # test with Map index and no row
        count = 0
        index = 'indexMapNumbers'
        it = self.store.index_iterator(self.table, index, None, True)
        for i in it:
            count += 1
        self.assertEqual(count, 75)

    def testIndexIteratorOneRecordOnly(self):
        # test with Record index and a single row
        row = {'recNumbers': {'firstInt': 3}}
        count = 0
        index = 'indexRecNumbers'
        it = self.store.index_iterator(self.table, index, row, True)
        all_good = True
        for i in it:
            count += 1
        self.assertTrue(all_good)
        self.assertEqual(count, 5)

    def testIndexIteratorNonExistentRecord(self):
        # test with Record index and a non existent row
        row = {'recNumbers': {'firstInt': 10}}
        count = 0
        index = 'indexRecNumbers'
        it = self.store.index_iterator(self.table, index, row, True)
        for i in it:
            count += 1
        self.assertEqual(count, 0)

    def testIndexIteratorRecordNoRow(self):
        # test with Record index and no row
        count = 0
        index = 'indexRecNumbers'
        it = self.store.index_iterator(self.table, index, None, True)
        for i in it:
            count += 1
        self.assertEqual(count, 25)

    def testIndexIteratorArrayNoRowForward(self):
        # test with Array index and forward
        count = 0
        index = 'indexArrNumbers'
        t_iterator_opts = TableIteratorOptions({
            ONDB_DIRECTION: {ONDB_DIRECTION: 'FORWARD'}})
        it = self.store.index_iterator(self.table, index, None, True,
            None, t_iterator_opts)
        all_ok = True
        old_int = -1
        for i in it:
            count += 1
            if (old_int > i['arrNumbers'][0]):
                all_ok = False
            old_int = i['arrNumbers'][0]
        self.assertTrue(all_ok)
        self.assertEqual(count, 125)

    def testIndexIteratorArrayNoRowReverse(self):
        # test with Array index and reverse
        count = 0
        index = 'indexArrNumbers'
        t_iterator_opts = TableIteratorOptions({
            ONDB_DIRECTION: {ONDB_DIRECTION: 'REVERSE'}})
        it = self.store.index_iterator(self.table, index, None, True,
            None, t_iterator_opts)
        all_ok = True
        old_int = 10000
        for i in it:
            count += 1
            if (old_int < i['arrNumbers'][0]):
                all_ok = False
            old_int = i['arrNumbers'][0]
        self.assertTrue(all_ok)
        self.assertEqual(count, 125)

    def testIndexIteratorArrayNoRowUnordered(self):
        # test with Array index and unordered
        count = 0
        index = 'indexArrNumbers'
        t_iterator_opts = TableIteratorOptions({
            ONDB_DIRECTION: {ONDB_DIRECTION: 'UNORDERED'}})
        it = self.store.index_iterator(self.table, index, None, True,
            None, t_iterator_opts)
        for i in it:
            count += 1
        self.assertEqual(count, 125)

    def testIndexIteratorMapNoRowForward(self):
        # test with Map index and forward
        count = 0
        index = 'indexMapNumbers'
        t_iterator_opts = TableIteratorOptions({
            ONDB_DIRECTION: {ONDB_DIRECTION: 'FORWARD'}})
        it = self.store.index_iterator(self.table, index, None, True,
            None, t_iterator_opts)
        all_ok = True
        old_key = 'field0None[]0'
        for i in it:
            count += 1
            this_key = ''
            for k, v in i['mapNumbers'].iteritems():
                this_key += str(k) + str(v)
            if (old_key > this_key):
                all_ok = False
            old_key = this_key
        self.assertTrue(all_ok)
        self.assertEqual(count, 75)

    def testIndexIteratorMapNoRowReverse(self):
        # test with Map index and reverse
        count = 0
        index = 'indexMapNumbers'
        t_iterator_opts = TableIteratorOptions({
            ONDB_DIRECTION: {ONDB_DIRECTION: 'REVERSE'}})
        it = self.store.index_iterator(self.table, index, None, True,
            None, t_iterator_opts)
        all_ok = True
        old_key = 'field4None[]7'
        for i in it:
            count += 1
            this_key = ''
            for k, v in i['mapNumbers'].iteritems():
                this_key += str(k) + str(v)
            if (old_key < this_key):
                all_ok = False
            old_key = this_key
        self.assertTrue(all_ok)
        self.assertEqual(count, 75)

    def testIndexIteratorMapNoRowUnordered(self):
        # test with Map index and unordered
        count = 0
        index = 'indexMapNumbers'
        t_iterator_opts = TableIteratorOptions({
            ONDB_DIRECTION: {ONDB_DIRECTION: 'UNORDERED'}})
        it = self.store.index_iterator(self.table, index, None, True,
            None, t_iterator_opts)
        for i in it:
            count += 1
        self.assertEqual(count, 75)

    def testIndexIteratorRecordNoRowForward(self):
        # test with Record index and forward
        count = 0
        index = 'indexRecNumbers'
        t_iterator_opts = TableIteratorOptions({
            ONDB_DIRECTION: {ONDB_DIRECTION: 'FORWARD'}})
        it = self.store.index_iterator(self.table, index, None, True,
            None, t_iterator_opts)
        all_ok = True
        old_id = -1
        old_int = -1
        for i in it:
            count += 1
            if (old_id > i['id'] or old_int > i['recNumbers']['firstInt']):
                all_ok = False
            old_id = i['id']
            old_int = i['recNumbers']['firstInt']
        self.assertTrue(all_ok)
        self.assertEqual(count, 25)

    def testIndexIteratorRecordNoRowReverse(self):
        # test with Record index and reverse
        count = 0
        index = 'indexRecNumbers'
        t_iterator_opts = TableIteratorOptions({
            ONDB_DIRECTION: {ONDB_DIRECTION: 'REVERSE'}})
        it = self.store.index_iterator(self.table, index, None, True,
            None, t_iterator_opts)
        all_ok = True
        old_id = 10000
        old_int = 10000
        for i in it:
            count += 1
            if (old_id < i['id'] or old_int < i['recNumbers']['firstInt']):
                all_ok = False
            old_id = i['id']
            old_int = i['recNumbers']['firstInt']
        self.assertTrue(all_ok)
        self.assertEqual(count, 25)

    def testIndexIteratorRecordNoRowUnordered(self):
        # test with Record index and unordered
        count = 0
        index = 'indexRecNumbers'
        t_iterator_opts = TableIteratorOptions({
            ONDB_DIRECTION: {ONDB_DIRECTION: 'UNORDERED'}})
        it = self.store.index_iterator(self.table, index, None, True,
            None, t_iterator_opts)
        for i in it:
            count += 1
        self.assertEqual(count, 25)


if __name__ == '__main__':
    add_runtime_params()
    unittest.main()
