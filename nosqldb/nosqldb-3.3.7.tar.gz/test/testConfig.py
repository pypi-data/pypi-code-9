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
from nosqldb import Consistency
from nosqldb import Durability
from nosqldb import IllegalArgumentException
from nosqldb import StoreConfig
from nosqldb import ProxyConfig
from nosqldb import ONDB_TIME_CONSISTENCY
from nosqldb import ONDB_PERMISSIBLE_LAG
from nosqldb import ONDB_TIMEOUT
from nosqldb import ONDB_MASTER_SYNC
from nosqldb import ONDB_REPLICA_SYNC
from nosqldb import ONDB_REPLICA_ACK
from testSetup import add_runtime_params

import unittest


class TestConfig(unittest.TestCase):

    def testStoreConfConsistency(self):
        s_conf = StoreConfig('kvstore', ('localhost:5000',))
        con = Consistency({
            ONDB_TIME_CONSISTENCY: {
                ONDB_PERMISSIBLE_LAG: 100,
                ONDB_TIMEOUT: 1000
            }})
        con.validate()
        s_conf.set_consistency(con)
        r_con = s_conf.get_consistency()
        self.assertEqual(r_con['time']['lag'], 100)
        self.assertEqual(r_con['time']['timeout'], 1000)

    def testStoreConfBadConsistency(self):
        s_conf = StoreConfig('kvstore', ('localhost:5000',))
        self.assertRaises(IllegalArgumentException,
            s_conf.set_consistency,
            '321')

    def testStoreConfDurability(self):
        s_conf = StoreConfig('kvstore', ('localhost:5000',))
        dur = Durability({
            ONDB_MASTER_SYNC: 'NO_SYNC',
            ONDB_REPLICA_SYNC: 'NO_SYNC',
            ONDB_REPLICA_ACK: 'ALL'
            })
        dur.validate()
        s_conf.set_durability(dur)
        r_dur = s_conf.get_durability()
        self.assertEqual(r_dur[ONDB_MASTER_SYNC], 'NO_SYNC')
        self.assertEqual(r_dur[ONDB_REPLICA_SYNC], 'NO_SYNC')
        self.assertEqual(r_dur[ONDB_REPLICA_ACK], 'ALL')

    def testStoreConfBadDurability(self):
        s_conf = StoreConfig('kvstore', ('localhost:5000',))
        self.assertRaises(IllegalArgumentException,
            s_conf.set_durability,
            'hi')

    def testStoreConfMaxResults(self):
        s_conf = StoreConfig('kvstore', ('localhost:5000',))
        s_conf.set_max_results(123)
        r_max_res = s_conf.get_max_results()
        self.assertEqual(r_max_res, 123)

    def testStoreConfBadMaxResults(self):
        s_conf = StoreConfig('kvstore', ('localhost:5000',))
        self.assertRaises(IllegalArgumentException,
            s_conf.set_max_results,
            '123')

    def testStoreConfReadZones(self):
        s_conf = StoreConfig('kvstore', ('localhost:5000',))
        read_zones = ('rz1', 'rz2', 'rz3')
        s_conf.set_read_zones(read_zones)
        r_read_zones = s_conf.get_read_zones()
        all_ok = True
        for i in range(len(read_zones)):
            if (read_zones[i] != r_read_zones[i]):
                all_ok = False
                break
        self.assertTrue(all_ok)

    def testStoreConfBadReadZones(self):
        s_conf = StoreConfig('kvstore', ('localhost:5000',))
        self.assertRaises(IllegalArgumentException,
            s_conf.set_read_zones,
            1)

    def testStoreConfRequestTimeout(self):
        s_conf = StoreConfig('kvstore', ('localhost:5000',))
        s_conf.set_request_timeout(150)
        r_request_timeout = s_conf.get_request_timeout()
        self.assertEqual(r_request_timeout, 150)

    def testStoreConfBadRequestTimeout(self):
        s_conf = StoreConfig('kvstore', ('localhost:5000',))
        self.assertRaises(IllegalArgumentException,
            s_conf.set_request_timeout,
            'True')

    def testStoreConfGetUser(self):
        s_conf = StoreConfig('kvstore', ('localhost:5000',))
        s_conf.set_user('user1')
        r_user = s_conf.get_user()
        self.assertEqual(r_user, 'user1')

    def testStoreConfBadGetUser(self):
        s_conf = StoreConfig('kvstore', ('localhost:5000',))
        self.assertRaises(IllegalArgumentException,
            s_conf.set_user,
            {})

    def testProxyConfRequestLimit(self):
        s_conf = ProxyConfig('kvstore', ('localhost:5000',))
        s_conf.set_request_limit(100)
        r_request_limit = s_conf.get_request_limit()
        self.assertEqual(r_request_limit, 100)

    def testProxyConfBadRequestLimit(self):
        s_conf = ProxyConfig('kvstore', ('localhost:5000',))
        self.assertRaises(IllegalArgumentException,
            s_conf.set_request_limit,
            {})

    def testProxyConfMaxIteratorResults(self):
        p_conf = ProxyConfig('../../kvstore/dist/lib/kvstore.jar',
            '../kvproxy/lib/kvproxy.jar')
        p_conf.set_max_iterator_results(543)
        r_max_iter_results = p_conf.get_max_iterator_results()
        self.assertEqual(r_max_iter_results, 543)

    def testProxyConfBadMaxIteratorResults(self):
        p_conf = ProxyConfig('../../kvstore/dist/lib/kvstore.jar',
            '../kvproxy/lib/kvproxy.jar')
        self.assertRaises(IllegalArgumentException,
            p_conf.set_max_iterator_results,
            'hi')

    def testProxyConfIteratorExpirationMs(self):
        p_conf = ProxyConfig('../../kvstore/dist/lib/kvstore.jar',
            '../kvproxy/lib/kvproxy.jar')
        p_conf.set_iterator_expiration_ms(111)
        r_iterator_expiration_ms = p_conf.get_iterator_expiration_ms()
        self.assertEqual(r_iterator_expiration_ms, 111)

    def testProxyConfBadIteratorExpirationMs(self):
        p_conf = ProxyConfig('../../kvstore/dist/lib/kvstore.jar',
            '../kvproxy/lib/kvproxy.jar')
        self.assertRaises(IllegalArgumentException,
            p_conf.set_iterator_expiration_ms,
            'False')

    def testProxyConfMaxOpenIterators(self):
        p_conf = ProxyConfig('../../kvstore/dist/lib/kvstore.jar',
            '../kvproxy/lib/kvproxy.jar')
        p_conf.set_max_open_iterators(700)
        r_max_open_iterators = p_conf.get_max_open_iterators()
        self.assertEqual(r_max_open_iterators, 700)

    def testProxyConfBadMaxOpenIterators(self):
        p_conf = ProxyConfig('../../kvstore/dist/lib/kvstore.jar',
            '../kvproxy/lib/kvproxy.jar')
        self.assertRaises(IllegalArgumentException,
            p_conf.set_max_open_iterators,
            '')

    def testProxyConfNumPoolThreads(self):
        p_conf = ProxyConfig('../../kvstore/dist/lib/kvstore.jar',
            '../kvproxy/lib/kvproxy.jar')
        p_conf.set_num_pool_threads(200)
        r_num_pool_threads = p_conf.get_num_pool_threads()
        self.assertEqual(r_num_pool_threads, 200)

    def testProxyConfBadNumPoolThreads(self):
        p_conf = ProxyConfig('../../kvstore/dist/lib/kvstore.jar',
            '../kvproxy/lib/kvproxy.jar')
        self.assertRaises(IllegalArgumentException,
            p_conf.set_num_pool_threads,
            'hi')

    def testProxyConfSocketReadTimeout(self):
        p_conf = ProxyConfig('../../kvstore/dist/lib/kvstore.jar',
            '../kvproxy/lib/kvproxy.jar')
        p_conf.set_socket_read_timeout(500)
        r_socket_read_timeout = p_conf.get_socket_read_timeout()
        self.assertEqual(r_socket_read_timeout, 500)

    def testProxyConfBadSocketReadTimeout(self):
        p_conf = ProxyConfig('../../kvstore/dist/lib/kvstore.jar',
            '../kvproxy/lib/kvproxy.jar')
        self.assertRaises(IllegalArgumentException,
            p_conf.set_socket_read_timeout,
            {})

    def testProxyConfRequestTimeout(self):
        p_conf = ProxyConfig('../../kvstore/dist/lib/kvstore.jar',
            '../kvproxy/lib/kvproxy.jar')
        p_conf.set_request_timeout(333)
        r_request_timeout = p_conf.get_request_timeout()
        self.assertEqual(r_request_timeout, 333)

    def testProxyConfBadRequestTimeout(self):
        p_conf = ProxyConfig('../../kvstore/dist/lib/kvstore.jar',
            '../kvproxy/lib/kvproxy.jar')
        self.assertRaises(IllegalArgumentException,
            p_conf.set_request_timeout,
            {})

    def testProxyConfSocketOpenTimeout(self):
        p_conf = ProxyConfig('../../kvstore/dist/lib/kvstore.jar',
            '../kvproxy/lib/kvproxy.jar')
        p_conf.set_socket_open_timeout(100)
        r_socket_open_timeout = p_conf.get_socket_open_timeout()
        self.assertEqual(r_socket_open_timeout, 100)

    def testProxyConfBadSocketOpenTimeout(self):
        p_conf = ProxyConfig('../../kvstore/dist/lib/kvstore.jar',
            '../kvproxy/lib/kvproxy.jar')
        self.assertRaises(IllegalArgumentException,
            p_conf.set_socket_open_timeout,
            'True')

    def testProxyConfMaxActiveRequest(self):
        p_conf = ProxyConfig('../../kvstore/dist/lib/kvstore.jar',
            '../kvproxy/lib/kvproxy.jar')
        p_conf.set_max_active_requests(350)
        r_max_active_requests = p_conf.get_max_active_requests()
        self.assertEqual(r_max_active_requests, 350)

    def testProxyConfBadMaxActiveRequest(self):
        p_conf = ProxyConfig('../../kvstore/dist/lib/kvstore.jar',
            '../kvproxy/lib/kvproxy.jar')
        self.assertRaises(IllegalArgumentException,
            p_conf.set_max_active_requests,
            'hi')

    def testProxyConfRequestThresholdPercent(self):
        p_conf = ProxyConfig('../../kvstore/dist/lib/kvstore.jar',
            '../kvproxy/lib/kvproxy.jar')
        p_conf.set_request_threshold_percent(90)
        r_request_threshold_percent = p_conf.get_request_threshold_percent()
        self.assertEqual(r_request_threshold_percent, 90)

    def testProxyConfBadRequestThresholdPercent(self):
        p_conf = ProxyConfig('../../kvstore/dist/lib/kvstore.jar',
            '../kvproxy/lib/kvproxy.jar')
        self.assertRaises(IllegalArgumentException,
            p_conf.set_request_threshold_percent,
            'hi')

    def testProxyConfNodeLimitPercent(self):
        p_conf = ProxyConfig('../../kvstore/dist/lib/kvstore.jar',
            '../kvproxy/lib/kvproxy.jar')
        p_conf.set_node_limit_percent(75)
        r_node_limit_percent = p_conf.get_node_limit_percent()
        self.assertEqual(r_node_limit_percent, 75)

    def testProxyConfBadNodeLimitPercent(self):
        p_conf = ProxyConfig('../../kvstore/dist/lib/kvstore.jar',
            '../kvproxy/lib/kvproxy.jar')
        self.assertRaises(IllegalArgumentException,
            p_conf.set_node_limit_percent,
            'hi')

    def testProxyConfVerbose(self):
        p_conf = ProxyConfig('../../kvstore/dist/lib/kvstore.jar',
            '../kvproxy/lib/kvproxy.jar')
        p_conf.set_verbose(False)
        r_verbose = p_conf.get_verbose()
        self.assertTrue(not r_verbose)

    def testProxyConfBadVerbose(self):
        p_conf = ProxyConfig('../../kvstore/dist/lib/kvstore.jar',
            '../kvproxy/lib/kvproxy.jar')
        self.assertRaises(IllegalArgumentException, p_conf.set_verbose,
            1)

    def testProxyConfSecurityPropsFile(self):
        p_conf = ProxyConfig('../../kvstore/dist/lib/kvstore.jar',
            '../kvproxy/lib/kvproxy.jar')
        p_conf.set_security_props_file('local/security.props')
        r_security_props_file = p_conf.get_security_props_file()
        self.assertEqual(r_security_props_file, 'local/security.props')

    def testProxyConfBadSecurityPropsFile(self):
        p_conf = ProxyConfig('../../kvstore/dist/lib/kvstore.jar',
            '../kvproxy/lib/kvproxy.jar')
        self.assertRaises(IllegalArgumentException,
            p_conf.set_security_props_file, bytearray('local/security.props'))


if __name__ == '__main__':
    add_runtime_params()
    unittest.main()
