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
# Note that since Factory.connect() was replaced by Factory.open() with only
# two parameters, this testcase is going to use such call instead.

from nosqldb import Factory
from nosqldb import Store
from nosqldb import ConnectionException
from nosqldb import IllegalArgumentException
from nosqldb import RequestTimeoutException
from testSetup import get_store
from testSetup import get_store2
from testSetup import add_runtime_params
from testSetup import get_kvstore_config
from testSetup import get_kvproxy_config
from testSetup import host_port
from testSetup import host_port2
from testSetup import helper_host
from testSetup import helper_host2
from testSetup import user

import unittest
import time


class TestConnectClose(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        kvstore_config = get_kvstore_config()
        kvproxy_config = get_kvproxy_config()
        cls._store1 = Factory.open(host_port, kvstore_config,
            kvproxy_config)
        time.sleep(5)

    @classmethod
    def tearDownClass(cls):
        if (cls._store1 is not None):
            cls._store1.close()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testConnectNormalStartup(self):
        # check that connect cannot start the proxy
        kvstore_config = get_kvstore_config()
        try:
            store = Factory.open(host_port2, kvstore_config)
        except ConnectionException, ce:
            store = None
        if (store is not None):
            store.shutdown()
            store.close()
            time.sleep(5)
        self.assertRaises(ConnectionException, Factory.open,
                          host_port2, kvstore_config)

    def testConnectNormalAlreadyUp(self):
        # check that connect can connect to an already started proxy
        kvstore_config = get_kvstore_config()
        store = Factory.open(host_port, kvstore_config)
        self.assertTrue(store is not None)

    def testConnectProxyAddress(self):
        # check that connect cannot start another proxy with a different address
        kvstore_config = get_kvstore_config()
        self.assertRaises(ConnectionException, Factory.open,
                          host_port2, kvstore_config)

    def testConnectHelperHostKVStoreConfig(self):
        # check connect with specific Helper Host
        # it should not actually work since it doesn't start a new proxy
        # using a KVStoreConfig object
        kvstore_config = get_kvstore_config()
        kvstore_config.set_helper_hosts((helper_host2,))
        self.assertRaises(ConnectionException, Factory.open,
                          host_port2, kvstore_config)


if __name__ == '__main__':
    add_runtime_params()
    unittest.main()
