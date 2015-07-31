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
from nosqldb import StoreConfig
from nosqldb import Consistency
from nosqldb import Row
from nosqldb import ConnectionException
from nosqldb import IllegalArgumentException
from nosqldb import RequestTimeoutException
from nosqldb import ABSOLUTE
from nosqldb import NONE_REQUIRED
from nosqldb import NONE_REQUIRED_NO_MASTER
from nosqldb import ONDB_CONSISTENCY
from nosqldb import ONDB_TIME_CONSISTENCY
from nosqldb import ONDB_VERSION_CONSISTENCY
from nosqldb import ONDB_PERMISSIBLE_LAG
from nosqldb import ONDB_VERSION
from nosqldb import ONDB_TIMEOUT
from testSetup import get_store
from testSetup import get_kvstore_config
from testSetup import get_kvproxy_config
from testSetup import add_runtime_params
from testSetup import table_name
from testSetup import host_port
import unittest


class TestGet(unittest.TestCase):
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
        StoreConfig.change_log('DEBUG', 'local.log')
        self.store = Factory.open(host_port, s_conf, p_conf)
        self.table = table_name
        self.row = {'id': 100, 's': 'String value', 'l': 1234567890,
                    'd': 123.456, 'bool': True,
                    'bin': self.store.encode_base_64('binarydata'),
                    'fbin': self.store.encode_base_64('fixedfixed'),
                    'f': 1.2345, 'arrStr': ['X', 'Y', 'Z'],
                    'e': 'A'}
        self.version, old_row = self.store.put(self.table, self.row)

    def tearDown(self):
        self.store.delete(self.table, {'id': 100})
        self.store.close()

    def testGetNormal(self):
        # test with an existing data and no ReadOptions
        primarykey = {'id': 100}
        crow = self.store.get(self.table, primarykey)
        self.assertEqual(crow, self.row)

    def testGetNoneRequired(self):
        # test with ReadOptions.Consistency = NONE_REQUIRED
        primarykey = {'id': 100}
        ropts = {ONDB_CONSISTENCY: NONE_REQUIRED,
            ONDB_TIMEOUT: 0}
        crow = self.store.get(self.table, primarykey, ropts)
        self.assertEqual(crow, self.row)

    def testGetAbsolute(self):
        # test with ReadOptions.Consistency = ABSOLUTE
        primarykey = {'id': 100}
        ropts = {ONDB_CONSISTENCY: ABSOLUTE,
            ONDB_TIMEOUT: 0}
        crow = self.store.get(self.table, primarykey, ropts)
        self.assertEqual(crow, self.row)

    def testGetNoneRequiredNoMaster(self):
        # test with ReadOptions.Consistency = NONE_REQUIRED_NO_MASTER
        primarykey = {'id': 100}
        ropts = {ONDB_CONSISTENCY: NONE_REQUIRED_NO_MASTER,
            ONDB_TIMEOUT: 0}
        crow = self.store.get(self.table, primarykey, ropts)
        self.assertEqual(crow, self.row)

    def testGetTimeConsistency(self):
        # test with ReadOptions.time_consistency = {ONDB_PREMISSIBLE_LAG=500,
        # ONDB_TIMEOUT = 1000}
        primarykey = {'id': 100}
        ropts = {
            ONDB_CONSISTENCY: {ONDB_TIME_CONSISTENCY: {
                ONDB_PERMISSIBLE_LAG: 500,
                ONDB_TIMEOUT: 1000}},
            ONDB_TIMEOUT: 0}
        crow = self.store.get(self.table, primarykey, ropts)
        self.assertEqual(crow, self.row)

    def testGetVersionConsistency(self):
        # test with ReadOptions.version_consistency =
        # {ONDB_VERSION=version_from_put, and ONDB_TIMEOUT = 1000}
        primarykey = {'id': 100}
        ropts = {
            ONDB_CONSISTENCY: {ONDB_VERSION_CONSISTENCY: {
                ONDB_VERSION: self.version,
                ONDB_TIMEOUT: 1000}},
            ONDB_TIMEOUT: 0}
        crow = self.store.get(self.table, primarykey, ropts)
        self.assertEqual(crow, self.row)

    def testGetNonExisting(self):
        # test with non-existing data and no ReadOptions
        primarykey = {'id': 101}
        crow = self.store.get(self.table, primarykey)
        self.assertEqual(crow, None)

    def testGetNoTable(self):
        # test with non-existing table and no ReadOptions
        primarykey = {'id': 100}
        self.assertRaises(IllegalArgumentException, self.store.get,
                          'NotValidTable', primarykey)

    def testGetNegativeTimeout(self):
        # test with negative timeout
        primarykey = {'id': 100}
        ropts = {'timeout': -1}
        self.assertRaises(IllegalArgumentException, self.store.get,
                          self.table, primarykey, ropts)

    def testGetOneSecondTimeout(self):
        # test with timeout = 1000 ms
        primarykey = {'id': 100}
        ropts = {'timeout': 1000}
        crow = self.store.get(self.table, primarykey, ropts)
        self.assertEqual(crow, self.row)

    def testGetNoValidPrimarykey(self):
        # test with an invalid key in Row
        primarykey = {'code': 100}
        self.assertRaises(IllegalArgumentException, self.store.get,
                          self.table, primarykey)

if __name__ == '__main__':
    add_runtime_params()
    unittest.main()
