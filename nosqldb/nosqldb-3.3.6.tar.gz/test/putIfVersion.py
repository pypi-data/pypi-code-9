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
from testSetup import add_runtime_params
from testSetup import table_name

import unittest


class TestPutIfVersion(unittest.TestCase):
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
        self.store = get_store()
        self.table = table_name
        self.row = Row({'id': 100, 's': 'String value', 'l': 1234567890,
            'd': 123.456, 'bool': True,
            'bin': self.store.encode_base_64('binarydata'),
            'fbin': self.store.encode_base_64('fixedfixed'),
            'f': 1.2345, 'arrStr': ['X', 'Y', 'Z'],
            'e': 'A'})
        self.version, self.oldrow = self.store.put(self.table, self.row)

    def tearDown(self):
        self.store.delete(self.table, Row({'id': 100}))
        self.store.close()

    def testPutIVNormal(self):
        # test with normal values and no special writeopts
        version, oldrow = self.store.put_if_version(
            self.table, self.row, self.version)
        primarykey = Row({'id': 100})
        newrow = self.store.get(self.table, primarykey)
        self.assertEqual(self.row, newrow)

    def testPutIVNsyNsyAll(self):
        # test with normal values and durabilityopts=NoSYNC, NoSYNC and All,
        # and returnValueVersion = NONE
        durability = Durability({
            ONDB_MASTER_SYNC: 'NO_SYNC',
            ONDB_REPLICA_SYNC: 'NO_SYNC',
            ONDB_REPLICA_ACK: 'ALL'})
        writeopts = WriteOptions({
            ONDB_DURABILITY: durability,
            ONDB_RETURN_CHOICE: 'NONE'})
        version, oldrow = self.store.put_if_version(
            self.table, self.row, self.version, writeopts)
        primarykey = Row({'id': 100})
        newrow = self.store.get(self.table, primarykey)
        self.assertEqual(self.row, newrow)

    def testPutIVNsyNsyNon(self):
        # test with normal values and durabilityopts=NoSYNC, NoSYNC and None,
        # and returnValueVersion = NONE
        durability = Durability({
            ONDB_MASTER_SYNC: 'NO_SYNC',
            ONDB_REPLICA_SYNC: 'NO_SYNC',
            ONDB_REPLICA_ACK: 'NONE'})
        writeopts = WriteOptions({
            ONDB_DURABILITY: durability,
            ONDB_RETURN_CHOICE: 'NONE'})
        version, oldrow = self.store.put_if_version(
            self.table, self.row, self.version, writeopts)
        primarykey = Row({'id': 100})
        newrow = self.store.get(self.table, primarykey)
        self.assertEqual(self.row, newrow)

    def testPutIVNsyNsySim(self):
        # test with normal values and durabilityopts=NoSYNC, NoSYNC
        # and SIMPLE_MAJORITY, and returnValueVersion = NONE
        durability = Durability({
            ONDB_MASTER_SYNC: 'NO_SYNC',
            ONDB_REPLICA_SYNC: 'NO_SYNC',
            ONDB_REPLICA_ACK: 'SIMPLE_MAJORITY'})
        writeopts = WriteOptions({
            ONDB_DURABILITY: durability,
            ONDB_RETURN_CHOICE: 'NONE'})
        version, oldrow = self.store.put_if_version(
            self.table, self.row, self.version, writeopts)
        primarykey = Row({'id': 100})
        newrow = self.store.get(self.table, primarykey)
        self.assertEqual(self.row, newrow)

    def testPutIVSynNsyAll(self):
        # test with normal values and durabilityopts=SYNC, NoSYNC and All,
        # and returnValueVersion = NONE
        durability = Durability({
            ONDB_MASTER_SYNC: 'SYNC',
            ONDB_REPLICA_SYNC: 'NO_SYNC',
            ONDB_REPLICA_ACK: 'ALL'})
        writeopts = WriteOptions({
            ONDB_DURABILITY: durability,
            ONDB_RETURN_CHOICE: 'NONE'})
        version, oldrow = self.store.put_if_version(
            self.table, self.row, self.version, writeopts)
        primarykey = Row({'id': 100})
        newrow = self.store.get(self.table, primarykey)
        self.assertEqual(self.row, newrow)

    def testPutIVSynNsyNon(self):
        # test with normal values and durabilityopts=SYNC, NoSYNC and None,
        # and returnValueVersion = NONE
        durability = Durability({
            ONDB_MASTER_SYNC: 'SYNC',
            ONDB_REPLICA_SYNC: 'NO_SYNC',
            ONDB_REPLICA_ACK: 'NONE'})
        writeopts = WriteOptions({
            ONDB_DURABILITY: durability,
            ONDB_RETURN_CHOICE: 'NONE'})
        version, oldrow = self.store.put_if_version(
            self.table, self.row, self.version, writeopts)
        primarykey = Row({'id': 100})
        newrow = self.store.get(self.table, primarykey)
        self.assertEqual(self.row, newrow)

    def testPutIVSynNsySim(self):
        # test with normal values and durabilityopts=SYNC, NoSYNC
        # and SIMPLE_MAJORITY and returnValueVersion = NONE
        durability = Durability({
            ONDB_MASTER_SYNC: 'SYNC',
            ONDB_REPLICA_SYNC: 'NO_SYNC',
            ONDB_REPLICA_ACK: 'SIMPLE_MAJORITY'})
        writeopts = WriteOptions({
            ONDB_DURABILITY: durability,
            ONDB_RETURN_CHOICE: 'NONE'})
        version, oldrow = self.store.put_if_version(
            self.table, self.row, self.version, writeopts)
        primarykey = Row({'id': 100})
        newrow = self.store.get(self.table, primarykey)
        self.assertEqual(self.row, newrow)

    def testPutIVNsySynAll(self):
        # test with normal values and durabilityopts=NoSYNC, SYNC and All,
        # and returnValueVersion = NONE
        durability = Durability({
            ONDB_MASTER_SYNC: 'NO_SYNC',
            ONDB_REPLICA_SYNC: 'SYNC',
            ONDB_REPLICA_ACK: 'ALL'})
        writeopts = WriteOptions({
            ONDB_DURABILITY: durability,
            ONDB_RETURN_CHOICE: 'NONE'})
        version, oldrow = self.store.put_if_version(
            self.table, self.row, self.version, writeopts)
        primarykey = Row({'id': 100})
        newrow = self.store.get(self.table, primarykey)
        self.assertEqual(self.row, newrow)

    def testPutIVNsySynNon(self):
        # test with normal values and durabilityopts=NoSYNC, SYNC and None,
        # and returnValueVersion = NONE
        durability = Durability({
            ONDB_MASTER_SYNC: 'NO_SYNC',
            ONDB_REPLICA_SYNC: 'SYNC',
            ONDB_REPLICA_ACK: 'NONE'})
        writeopts = WriteOptions({
            ONDB_DURABILITY: durability,
            ONDB_RETURN_CHOICE: 'NONE'})
        version, oldrow = self.store.put_if_version(
            self.table, self.row, self.version, writeopts)
        primarykey = Row({'id': 100})
        newrow = self.store.get(self.table, primarykey)
        self.assertEqual(self.row, newrow)

    def testPutIVNsySynSim(self):
        # test with normal values and durabilityopts=NoSYNC, SYNC
        # and SIMPLE_MAJORITY, and returnValueVersion = NONE
        durability = Durability({
            ONDB_MASTER_SYNC: 'NO_SYNC',
            ONDB_REPLICA_SYNC: 'SYNC',
            ONDB_REPLICA_ACK: 'SIMPLE_MAJORITY'})
        writeopts = WriteOptions({
            ONDB_DURABILITY: durability,
            ONDB_RETURN_CHOICE: 'NONE'})
        version, oldrow = self.store.put_if_version(
            self.table, self.row, self.version, writeopts)
        primarykey = Row({'id': 100})
        newrow = self.store.get(self.table, primarykey)
        self.assertEqual(self.row, newrow)

    def testPutIVSynSynAll(self):
        # test with normal values and durabilityopts=SYNC, SYNC and All,
        # and returnValueVersion = NONE
        durability = Durability({
            ONDB_MASTER_SYNC: 'SYNC',
            ONDB_REPLICA_SYNC: 'SYNC',
            ONDB_REPLICA_ACK: 'ALL'})
        writeopts = WriteOptions({
            ONDB_DURABILITY: durability,
            ONDB_RETURN_CHOICE: 'NONE'})
        version, oldrow = self.store.put_if_version(
            self.table, self.row, self.version, writeopts)
        primarykey = Row({'id': 100})
        newrow = self.store.get(self.table, primarykey)
        self.assertEqual(self.row, newrow)

    def testPutIVSynSynNon(self):
        # test with normal values and durabilityopts=SYNC, SYNC and None,
        # and returnValueVersion = NONE
        durability = Durability({
            ONDB_MASTER_SYNC: 'SYNC',
            ONDB_REPLICA_SYNC: 'SYNC',
            ONDB_REPLICA_ACK: 'NONE'})
        writeopts = WriteOptions({
            ONDB_DURABILITY: durability,
            ONDB_RETURN_CHOICE: 'NONE'})
        version, oldrow = self.store.put_if_version(
            self.table, self.row, self.version, writeopts)
        primarykey = Row({'id': 100})
        newrow = self.store.get(self.table, primarykey)
        self.assertEqual(self.row, newrow)

    def testPutIVSynSynSim(self):
        # test with normal values and durabilityopts=SYNC, SYNC
        # and SIMPLE_MAJORITY, and returnValueVersion = NONE
        durability = Durability({
            ONDB_MASTER_SYNC: 'SYNC',
            ONDB_REPLICA_SYNC: 'SYNC',
            ONDB_REPLICA_ACK: 'SIMPLE_MAJORITY'})
        writeopts = WriteOptions({
            ONDB_DURABILITY: durability,
            ONDB_RETURN_CHOICE: 'NONE'})
        version, oldrow = self.store.put_if_version(
            self.table, self.row, self.version, writeopts)
        primarykey = Row({'id': 100})
        newrow = self.store.get(self.table, primarykey)
        self.assertEqual(self.row, newrow)

    def testPutIVValue(self):
        # test with Durability.COMMIT_NO_SYNC and returnValueVersion = VALUE
        # according to documentation this kind of put doesn't return value nor
        # version so expect None
        writeopts = WriteOptions({
            ONDB_DURABILITY: COMMIT_NO_SYNC,
            ONDB_RETURN_CHOICE: 'VALUE'})
        self.row['bool'] = False
        version2, oldrow = self.store.put_if_version(
            self.table, self.row, self.version, writeopts)
        self.row['bool'] = True
        self.assertEqual({}, oldrow)

    def testPutIVVersion(self):
        # test with Durability.COMMIT_SYNC and returnValueVersion = VERSION
        # according to documentation this kind of put doesn't return value nor
        # version so expect None
        writeopts = WriteOptions({
            ONDB_DURABILITY: COMMIT_SYNC,
            ONDB_RETURN_CHOICE: 'VERSION'})
        self.row['bool'] = False
        version2, oldrow = self.store.put_if_version(
            self.table, self.row, self.version, writeopts)
        self.row['bool'] = True
        self.assertEqual(None, oldrow.get_version())

    def testPutIVValueVersion(self):
        # test with Durability.COMMIT_WRITE_NO_SYNC and returnValueVersion = ALL
        # according to documentation this kind of put doesn't return value nor
        # version so expect None
        writeopts = WriteOptions({ONDB_DURABILITY: COMMIT_WRITE_NO_SYNC,
            ONDB_RETURN_CHOICE: 'ALL'})
        self.row['bool'] = False
        version2, oldrow = self.store.put_if_version(
            self.table, self.row, self.version, writeopts)
        self.row['bool'] = True
        self.assertEqual({}, oldrow)
        self.assertEqual(None, oldrow.get_version())

    def testPutIVSecondTimeout(self):
        # test with Durability.COMMIT_NO_SYNC, returnValueVersion = VALUE
        # and timeout = 1000 ms
        writeopts = WriteOptions({ONDB_DURABILITY: COMMIT_WRITE_NO_SYNC,
            ONDB_TIMEOUT: 1000,
            ONDB_RETURN_CHOICE: 'ALL'})
        version2, oldrow = self.store.put_if_version(
            self.table, self.row, self.version, writeopts)
        primarykey = Row({'id': 100})
        newrow = self.store.get(self.table, primarykey)
        self.assertEqual(self.row, newrow)

    def testPutIVNoTable(self):
        # test with an invalid table name
        self.assertRaises(IllegalArgumentException, self.store.put_if_version,
                          'NotValidTable', self.row, self.version)

    def testPutIVNegativeTimeout(self):
        # test with a negative timeout
        writeopts = {ONDB_TIMEOUT: -1}
        self.assertRaises(IllegalArgumentException, self.store.put_if_version,
                          self.table, self.row, self.version, writeopts)

    def testPutIVInvalidFields(self):
        # test with invalid fields in the row
        self.assertRaises(KeyError, self.store.put_if_version,
                          self.table, self.row, self.version,
                          {'invalidField': 'someValue'})

    def testPutIVDiffVersion(self):
        # test with a different version, expect None as result
        version2, midverrow = self.store.put(self.table, self.row)
        version3, oldrow2 = self.store.put_if_version(
            self.table, self.row, self.version)
        self.assertEqual(None, version3)

if __name__ == '__main__':
    add_runtime_params()
    unittest.main()
