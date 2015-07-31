
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


class TestOpenClose(unittest.TestCase):

    def setUp(self):
        self.kvstore_config = get_kvstore_config()
        self.kvproxy_config = get_kvproxy_config()
        self.store = None
        self.store2 = None

    def tearDown(self):
        if (self.store is not None):
            self.store.close()
        if (self.store2 is not None):
            self.store2.shutdown()
            self.store2.close()

    def testOpenNormalStartup(self):
        # check that open can start the proxy
        try:
            self.store = Factory.open(host_port,
                self.kvstore_config)
            if (self.store is not None):
            # if the proxy is up shut it down and wait for it to stop
                self.store.shutdown()
                time.sleep(10)
        except ConnectionException, ce:
            self.store = Factory.open(host_port,
                self.kvstore_config, self.kvproxy_config)
            self.assertTrue(self.store is not None)

    def testOpenNormalAlreadyUp(self):
        # check that open can connect to an already started proxy
        self.store = Factory.open(host_port,
            self.kvstore_config, self.kvproxy_config)
        self.assertTrue(self.store is not None)

    def testOpenProxyAddress(self):
        # check that open can start another proxy with a different address
        self.store2 = Factory.open(host_port2,
            self.kvstore_config, self.kvproxy_config)
        self.assertTrue(self.store2 is not None)

    def testOpenhelper_hostParam(self):
        # check open with specific Helper Host
        # note that there should be a store at localhost:5000
        self.kvstore_config.set_helper_hosts((helper_host,))
        self.store = Factory.open(host_port2,
            self.kvstore_config, self.kvproxy_config)
        self.assertTrue(self.store is not None)


if __name__ == '__main__':
    add_runtime_params()
    unittest.main()
