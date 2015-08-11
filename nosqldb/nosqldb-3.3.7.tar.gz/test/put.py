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
from nosqldb import StoreConfig
from nosqldb import Row
from nosqldb import Durability
from nosqldb import WriteOptions
from nosqldb import ConnectionException
from nosqldb import IllegalArgumentException
from nosqldb import ProxyException
from nosqldb import COMMIT_SYNC
from nosqldb import COMMIT_NO_SYNC
from nosqldb import COMMIT_WRITE_NO_SYNC
from nosqldb import ONDB_MASTER_SYNC
from nosqldb import ONDB_REPLICA_SYNC
from nosqldb import ONDB_REPLICA_ACK
from nosqldb import ONDB_DURABILITY
from nosqldb import ONDB_RETURN_CHOICE
from nosqldb import ONDB_TIMEOUT
from testSetup import get_store
from testSetup import get_kvstore_config
from testSetup import get_kvproxy_config
from testSetup import add_runtime_params
from testSetup import table_name
from testSetup import host_port

import unittest


class TestPut(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._store = get_store()
        cls._store.execute_sync("DROP TABLE IF EXISTS " + table_name)
        cls._store.refresh_tables()
        cls._store.execute_sync(
            "CREATE TABLE " + table_name + " (" +
            "id INTEGER, s STRING, l LONG, d DOUBLE, bool BOOLEAN, " +
            "bin BINARY, fbin BINARY(10), f FLOAT, arrStr ARRAY(STRING), " +
            "e ENUM(A, B, C, D), PRIMARY KEY (id) )")
        cls._store.refresh_tables()

    @classmethod
    def tearDownClass(cls):
        cls._store.execute_sync("DROP TABLE IF EXISTS " + table_name)
        cls._store.refresh_tables()
        cls._store.close()

    def setUp(self):
        s_conf = get_kvstore_config()
        p_conf = get_kvproxy_config()
        s_conf.set_durability({
            'master_sync': 'SYNC',
            'replica_sync': 'NO_SYNC',
            'replica_ack': 'ALL'})
        StoreConfig.change_log('DEBUG', None)
        self.store = Factory.open(host_port, s_conf, p_conf)
        self.table = table_name
        self.row = Row({'id': 100, 's': 'String value', 'l': 1234567890,
                    'd': 123.456, 'bool': True,
                    'bin': self.store.encode_base_64('binarydata'),
                    'fbin': self.store.encode_base_64('fixedfixed'),
                    'f': 1.2345, 'arrStr': ['X', 'Y', 'Z'],
                    'e': 'A'})

    def tearDown(self):
        self.store.delete(self.table, Row({'id': 100}))
        self.store.close()

    def testPutNormal(self):
        # test with normal values and no writeopts
        version, oldrow = self.store.put(self.table, self.row)
        primarykey = Row({'id': 100})
        newrow = self.store.get(self.table, primarykey)
        self.assertEqual(self.row, newrow)

    def testPutNsyNsyAll(self):
        # test with normal values and durabilityopts=NoSYNC, NoSYNC and All,
        # and return_value_version = NONE
        durability = Durability(
            {ONDB_MASTER_SYNC: 'NO_SYNC', ONDB_REPLICA_SYNC: 'NO_SYNC',
             ONDB_REPLICA_ACK: 'ALL'})
        writeopts = WriteOptions(
            {ONDB_DURABILITY: durability,
             ONDB_RETURN_CHOICE: 'NONE'})
        version, oldrow = self.store.put(self.table, self.row, writeopts)
        primarykey = Row({'id': 100})
        newrow = self.store.get(self.table, primarykey)
        self.assertEqual(self.row, newrow)

    def testPutNsyNsyNon(self):
        # test with normal values and durabilityopts=NoSYNC, NoSYNC and None,
        # and return_value_version = NONE
        durability = Durability(
            {ONDB_MASTER_SYNC: 'NO_SYNC', ONDB_REPLICA_SYNC: 'NO_SYNC',
             ONDB_REPLICA_ACK: 'NONE'})
        writeopts = WriteOptions(
            {ONDB_DURABILITY: durability,
             ONDB_RETURN_CHOICE: 'NONE'})
        version, oldrow = self.store.put(self.table, self.row, writeopts)
        primarykey = Row({'id': 100})
        newrow = self.store.get(self.table, primarykey)
        self.assertEqual(self.row, newrow)

    def testPutNsyNsySim(self):
        # test with normal values and durabilityopts=NoSYNC, NoSYNC
        # and SIMPLE_MAJORITY, and return_value_version = NONE
        durability = Durability(
            {ONDB_MASTER_SYNC: 'NO_SYNC', ONDB_REPLICA_SYNC: 'NO_SYNC',
             ONDB_REPLICA_ACK: 'SIMPLE_MAJORITY'})
        writeopts = WriteOptions(
            {ONDB_DURABILITY: durability,
             ONDB_RETURN_CHOICE: 'NONE'})
        version, oldrow = self.store.put(self.table, self.row, writeopts)
        primarykey = Row({'id': 100})
        newrow = self.store.get(self.table, primarykey)
        self.assertEqual(self.row, newrow)

    def testPutSynNsyAll(self):
        # test with normal values and durabilityopts=SYNC, NoSYNC and All,
        # and return_value_version = NONE
        durability = Durability(
            {ONDB_MASTER_SYNC: 'SYNC', ONDB_REPLICA_SYNC: 'NO_SYNC',
             ONDB_REPLICA_ACK: 'ALL'})
        writeopts = WriteOptions(
            {ONDB_DURABILITY: durability,
             ONDB_RETURN_CHOICE: 'NONE'})
        version, oldrow = self.store.put(self.table, self.row, writeopts)
        primarykey = Row({'id': 100})
        newrow = self.store.get(self.table, primarykey)
        self.assertEqual(self.row, newrow)

    def testPutSynNsyNon(self):
        # test with normal values and durabilityopts=SYNC, NoSYNC and None,
        # and return_value_version = NONE
        durability = Durability(
            {ONDB_MASTER_SYNC: 'SYNC', ONDB_REPLICA_SYNC: 'NO_SYNC',
             ONDB_REPLICA_ACK: 'NONE'})
        writeopts = WriteOptions(
            {ONDB_DURABILITY: durability,
             ONDB_RETURN_CHOICE: 'NONE'})
        version, oldrow = self.store.put(self.table, self.row, writeopts)
        primarykey = Row({'id': 100})
        newrow = self.store.get(self.table, primarykey)
        self.assertEqual(self.row, newrow)

    def testPutSynNsySim(self):
        # test with normal values and durabilityopts=SYNC, NoSYNC
        # and SIMPLE_MAJORITY and return_value_version = NONE
        durability = Durability(
            {ONDB_MASTER_SYNC: 'SYNC', ONDB_REPLICA_SYNC: 'NO_SYNC',
             ONDB_REPLICA_ACK: 'SIMPLE_MAJORITY'})
        writeopts = WriteOptions(
            {ONDB_DURABILITY: durability,
             ONDB_RETURN_CHOICE: 'NONE'})
        version, oldrow = self.store.put(self.table, self.row, writeopts)
        primarykey = Row({'id': 100})
        newrow = self.store.get(self.table, primarykey)
        self.assertEqual(self.row, newrow)

    def testPutNsySynAll(self):
        # test with normal values and durabilityopts=NoSYNC, SYNC and All,
        # and return_value_version = NONE
        durability = Durability(
            {ONDB_MASTER_SYNC: 'NO_SYNC', ONDB_REPLICA_SYNC: 'SYNC',
             ONDB_REPLICA_ACK: 'ALL'})
        writeopts = WriteOptions(
            {ONDB_DURABILITY: durability,
             ONDB_RETURN_CHOICE: 'NONE'})
        version, oldrow = self.store.put(self.table, self.row, writeopts)
        primarykey = Row({'id': 100})
        newrow = self.store.get(self.table, primarykey)
        self.assertEqual(self.row, newrow)

    def testPutNsySynNon(self):
        # test with normal values and durabilityopts=NoSYNC, SYNC and None,
        # and return_value_version = NONE
        durability = Durability(
            {ONDB_MASTER_SYNC: 'NO_SYNC', ONDB_REPLICA_SYNC: 'SYNC',
             ONDB_REPLICA_ACK: 'NONE'})
        writeopts = WriteOptions(
            {ONDB_DURABILITY: durability,
             ONDB_RETURN_CHOICE: 'NONE'})
        version, oldrow = self.store.put(self.table, self.row, writeopts)
        primarykey = Row({'id': 100})
        newrow = self.store.get(self.table, primarykey)
        self.assertEqual(self.row, newrow)

    def testPutNsySynSim(self):
        # test with normal values and durabilityopts=NoSYNC, SYNC
        # and SIMPLE_MAJORITY, and return_value_version = NONE
        durability = Durability(
            {ONDB_MASTER_SYNC: 'NO_SYNC', ONDB_REPLICA_SYNC: 'SYNC',
             ONDB_REPLICA_ACK: 'SIMPLE_MAJORITY'})
        writeopts = WriteOptions(
            {ONDB_DURABILITY: durability,
             ONDB_RETURN_CHOICE: 'NONE'})
        version, oldrow = self.store.put(self.table, self.row, writeopts)
        primarykey = Row({'id': 100})
        newrow = self.store.get(self.table, primarykey)
        self.assertEqual(self.row, newrow)

    def testPutSynSynAll(self):
        # test with normal values and durabilityopts=SYNC, SYNC and All,
        # and return_value_version = NONE
        durability = Durability(
            {ONDB_MASTER_SYNC: 'SYNC', ONDB_REPLICA_SYNC: 'SYNC',
             ONDB_REPLICA_ACK: 'ALL'})
        writeopts = WriteOptions(
            {ONDB_DURABILITY: durability,
             ONDB_RETURN_CHOICE: 'NONE'})
        version, oldrow = self.store.put(self.table, self.row, writeopts)
        primarykey = Row({'id': 100})
        newrow = self.store.get(self.table, primarykey)
        self.assertEqual(self.row, newrow)

    def testPutSynSynNon(self):
        # test with normal values and durabilityopts=SYNC, SYNC and None,
        # and return_value_version = NONE
        durability = Durability(
            {ONDB_MASTER_SYNC: 'SYNC', ONDB_REPLICA_SYNC: 'SYNC',
             ONDB_REPLICA_ACK: 'NONE'})
        writeopts = WriteOptions(
            {ONDB_DURABILITY: durability,
             ONDB_RETURN_CHOICE: 'NONE'})
        version, oldrow = self.store.put(self.table, self.row, writeopts)
        primarykey = Row({'id': 100})
        newrow = self.store.get(self.table, primarykey)
        self.assertEqual(self.row, newrow)

    def testPutSynSynSim(self):
        # test with normal values and durabilityopts=SYNC, SYNC
        # and SIMPLE_MAJORITY, and return_value_version = NONE
        durability = Durability(
            {ONDB_MASTER_SYNC: 'SYNC', ONDB_REPLICA_SYNC: 'SYNC',
             ONDB_REPLICA_ACK: 'SIMPLE_MAJORITY'})
        writeopts = WriteOptions(
            {ONDB_DURABILITY: durability,
             ONDB_RETURN_CHOICE: 'NONE'})
        version, oldrow = self.store.put(self.table, self.row, writeopts)
        primarykey = Row({'id': 100})
        newrow = self.store.get(self.table, primarykey)
        self.assertEqual(self.row, newrow)

    def testPutValue(self):
        # test with Durability.COMMIT_NO_SYNC and return_value_version = VALUE
        version1, oldrow = self.store.put(self.table, self.row)
        writeopts = WriteOptions({
            ONDB_DURABILITY:
            COMMIT_NO_SYNC,
            ONDB_RETURN_CHOICE: 'VALUE'})
        self.row['bool'] = False
        version2, oldrow = self.store.put(self.table, self.row, writeopts)
        primarykey = Row({'id': 100})
        self.store.get(self.table, primarykey)
        self.row['bool'] = True
        self.assertEqual(self.row, oldrow)

    def testPutVersion(self):
        # test with Durability.COMMIT_NO_SYNC and
        # return_value_version = VERSION
        version1, oldrow = self.store.put(self.table, self.row)
        writeopts = WriteOptions({
            ONDB_DURABILITY:
            COMMIT_SYNC,
            ONDB_RETURN_CHOICE: 'VERSION'})
        self.row['bool'] = False
        version2, oldrow = self.store.put(self.table, self.row, writeopts)
        primarykey = Row({'id': 100})
        self.store.get(self.table, primarykey)
        self.row['bool'] = True
        self.assertEqual(version1, oldrow.get_version())

    def testPutValueVersion(self):
        # test with Durability.COMMIT_NO_SYNC and return_value_version = ALL
        version1, oldrow = self.store.put(self.table, self.row)
        writeopts = WriteOptions({
            ONDB_DURABILITY:
            COMMIT_WRITE_NO_SYNC,
            ONDB_RETURN_CHOICE: 'ALL'})
        self.row['bool'] = False
        version2, oldrow = self.store.put(self.table, self.row, writeopts)
        primarykey = Row({'id': 100})
        self.store.get(self.table, primarykey)
        self.row['bool'] = True
        self.assertEqual(self.row, oldrow)
        self.assertEqual(version1, oldrow.get_version())

    def testPutSecondTimeout(self):
        # test with Durability.COMMIT_NO_SYNC, return_value_version = VALUE
        # and timeout = 1000 ms
        writeopts = WriteOptions({
            ONDB_DURABILITY:
            COMMIT_WRITE_NO_SYNC,
            ONDB_TIMEOUT: 1000,
            ONDB_RETURN_CHOICE: 'ALL'})
        version2, oldrow = self.store.put(self.table, self.row, writeopts)
        primarykey = Row({'id': 100})
        newrow = self.store.get(self.table, primarykey)
        self.assertEqual(self.row, newrow)

    def testPutNoTable(self):
        # test with an invalid table name
        self.assertRaises(IllegalArgumentException, self.store.put,
                          'NotValidTable', self.row, None)

    def testPutNegativeTimeout(self):
        # test with a negative timeout
        self.assertRaises(IllegalArgumentException, self.store.put,
                          self.table, self.row,
                          WriteOptions({ONDB_TIMEOUT: -1}))

    def testPutInvalidFields(self):
        # test with invalid fields in the row
        self.assertRaises(IllegalArgumentException, self.store.put,
                          self.table, {'invalidField': 'someValue'})

if __name__ == '__main__':
    add_runtime_params()
    unittest.main()
