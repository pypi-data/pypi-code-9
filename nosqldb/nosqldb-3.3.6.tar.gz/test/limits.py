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
import unittest


class TestLimits(unittest.TestCase):
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

    def tearDown(self):
        self.store.delete(self.table, {'id': 100})
        self.store.close()

    def testMaxInt(self):
        self.row = {'id': 100, 's': 'String value',
                    'l': pow(2, 31) - 1,
                    'd': 123.456, 'bool': True,
                    'bin': self.store.encode_base_64('binarydata'),
                    'fbin': self.store.encode_base_64('fixedfixed'),
                    'f': 1.2345, 'arrStr': ['X', 'Y', 'Z'],
                    'e': 'A'}
        self.store.put(self.table, self.row)
        readField = self.store.get(self.table, {'id': 100})
        self.assertEqual(readField['l'], pow(2, 31) - 1)

    def testMaxIntPlusOne(self):
        self.row = {'id': 100, 's': 'String value',
                    'l': pow(2, 31),
                    'd': 123.456, 'bool': True,
                    'bin': self.store.encode_base_64('binarydata'),
                    'fbin': self.store.encode_base_64('fixedfixed'),
                    'f': 1.2345, 'arrStr': ['X', 'Y', 'Z'],
                    'e': 'A'}
        self.store.put(self.table, self.row)
        readField = self.store.get(self.table, {'id': 100})
        self.assertEqual(readField['l'], pow(2, 31))

    def testMaxLong(self):
        self.row = {'id': 100, 's': 'String value',
                    'l': pow(2, 63) - 1,
                    'd': 123.456, 'bool': True,
                    'bin': self.store.encode_base_64('binarydata'),
                    'fbin': self.store.encode_base_64('fixedfixed'),
                    'f': 1.2345, 'arrStr': ['X', 'Y', 'Z'],
                    'e': 'A'}
        self.store.put(self.table, self.row)
        readField = self.store.get(self.table, {'id': 100})
        self.assertEqual(readField['l'], pow(2, 63) - 1)

    def testMaxLongPlusOne(self):
        self.row = {'id': 100, 's': 'String value',
                    'l': pow(2, 63),
                    'd': 123.456, 'bool': True,
                    'bin': self.store.encode_base_64('binarydata'),
                    'fbin': self.store.encode_base_64('fixedfixed'),
                    'f': 1.2345, 'arrStr': ['X', 'Y', 'Z'],
                    'e': 'A'}
        self.assertRaises(IllegalArgumentException, self.store.put,
                          self.table, self.row)

if __name__ == '__main__':
    add_runtime_params()
    unittest.main()
