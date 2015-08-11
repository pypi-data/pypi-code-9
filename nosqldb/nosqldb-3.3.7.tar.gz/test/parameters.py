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

# This file is intended to be modified for the user in order to set the
# default parameters for testing

# the store name
store_name = 'kvstore'
# the address for the proxy
host_port = 'localhost:5010'
# the address for the secondary proxy
host_port2 = 'localhost:9999'
# the address for the primary helper host
helper_host = 'localhost:5000'
# the address for the seconary helper host
helper_host2 = 'localhost:6000'
# the primary table name to use
table_name = 't2'
# the secondary table name to use
table_name2 = 't3'
# the location for kvclient jar
kvstore_path = '../nosqldb/kvproxy/lib/kvclient.jar'
# the location for the proxy jar is known to us but it
# is better if you can point to other if needed
kvproxy_path = '../nosqldb/kvproxy/lib/kvproxy.jar'
# the default user
user = 'user'
