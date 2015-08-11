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

# This file contains support routines for testcases.
# It needs parameters.py file updated with user defaults
# in order to be able to run correctly.

from nosqldb import Factory
from nosqldb import StoreConfig
from nosqldb import ProxyConfig
from parameters import store_name
from parameters import host_port
from parameters import host_port2
from parameters import helper_host
from parameters import helper_host2
from parameters import table_name
from parameters import table_name2
from parameters import kvstore_path
from parameters import kvproxy_path
from parameters import user

import argparse
import sys


def get_kvstore_config():
    # Creates the default StoreConfig with the default store_name
    # and the default helper_host
    s_config = StoreConfig(store_name, (helper_host,))
    return s_config


def get_kvproxy_config():
    # Creates the default ProxyConfig with the default paths for
    # kvstore and kvproxy
    p_config = ProxyConfig(kvstore_path, kvproxy_path)
    return p_config


def get_store2():
    # Returns a connection to the secondary proxy
    # denoted by host_port2
    kvstore_config = get_kvstore_config()
    kvproxy_config = get_kvproxy_config()
    return Factory.open(host_port2, kvstore_config, kvproxy_config)


def get_store():
    # Returns a connection to the primary proxy
    # denoted by host_port
    kvstore_config = get_kvstore_config()
    kvproxy_config = get_kvproxy_config()
    return Factory.open(host_port, kvstore_config, kvproxy_config)


def add_runtime_params():
    # Add a mechanism to change the default parameters from command line.
    # This is only for manual excecution, if you want to change a default
    # parameter you can edit parameters.py in order to do so.
    global host_port
    global helper_host
    global helper_host2
    global table_name
    global table_name2
    global store_name
    global user
    global kvstore_config
    global kvproxy_config
    parser = argparse.ArgumentParser()
    parser.add_argument('--hostport',
                        help='specify the host and port to connect to')
    parser.add_argument('--helperhost',
                        help='specify the helperhost to be used')
    parser.add_argument('--helperhost2',
                        help='specify the second helperhost to be used')
    parser.add_argument('--tablename',
                        help='specify the table name to be used')
    parser.add_argument('--tablename2',
                        help='specify the table name to be used')
    parser.add_argument('--storename',
                        help='specify the store name to be used')
    parser.add_argument('--user',
                        help='specify the user to be used')
    parser.add_argument('--storejar',
                        help='specify the location of kvstore jar')
    parser.add_argument('--proxyjar',
                        help='specify the location of kvproxy jar')
    args = parser.parse_args()
    if (args.hostport is not None):
        host_port = args.hostport
    if (args.helperhost is not None):
        helper_host = args.helperhost
    if (args.helperhost2 is not None):
        helper_host2 = args.helperhost2
    if (args.tablename is not None):
        table_name = args.tablename
    if (args.tablename2 is not None):
        table_name2 = args.tablename2
    if (args.storename is not None):
        store_name = args.storename
    if (args.user is not None):
        user = args.user
    if (args.storejar is not None):
        kvstore_path = args.storejar
    if (args.proxyjar is not None):
        kvproxy_path = args.proxyjar
    del sys.argv[1:]
