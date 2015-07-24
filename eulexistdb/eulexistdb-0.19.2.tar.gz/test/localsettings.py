# file testsettings.py
#
#   Copyright 2011 Emory University Libraries
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

#from localsettings import *

import os
import logging

# must be set before importing anything from django
os.environ['DJANGO_SETTINGS_MODULE'] = 'localsettings'

# secret key required as of django 1.5
SECRET_KEY = 'notsomuchofasecretafterall'

#EXISTDB_SERVER_HOST = "localhost:8080/exist"
# EXISTDB_SERVER_HOST = "localhost:7018/exist"
# EXISTDB_SERVER_HOST = "localhost:8080/exist"
EXISTDB_SERVER_URL     = "http://kamina.library.emory.edu:8080/exist"
# NOTE: test account used for tests that require non-guest access; user should be in eXist DBA group
# EXISTDB_SERVER_USER = "eulcore_tester"
# EXISTDB_SERVER_PASSWORD = "eVlc0re_t3st"

EXISTDB_SERVER_USER = "findingaids"
EXISTDB_SERVER_PASSWORD = "findingaids"

# testing against exist 2.2
EXISTDB_SERVER_URL = 'http://wlibqas002.library.emory.edu:8081/exist/'
EXISTDB_SERVER_ADMIN_USER = "eulexistdbtest"
EXISTDB_SERVER_ADMIN_PASSWORD = "ergoiam"

# limited-access test account to be created by the admin user for
# testing purposes only
EXISTDB_SERVER_USER = "eulexistdbtester-rsk"
EXISTDB_SERVER_PASSWORD = "pass12349876"

# #EXISTDB_SERVER_USER = "admin"
# #EXISTDB_SERVER_PASSWORD = ""
# # main access - no user/password, guest account
# EXISTDB_SERVER_URL = EXISTDB_SERVER_PROTOCOL + EXISTDB_SERVER_HOST
# # access with the specified user account
# # FIXME: don't use
# EXISTDB_SERVER_URL_DBA = EXISTDB_SERVER_PROTOCOL + EXISTDB_SERVER_USER + ":" + \
    # EXISTDB_SERVER_PASSWORD + "@" + EXISTDB_SERVER_HOST
EXISTDB_ROOT_COLLECTION = '/eulexistdb-rsk'
EXISTDB_TEST_BASECOLLECTION = '/test-eulexistdb'
EXISTDB_TEST_COLLECTION = EXISTDB_TEST_BASECOLLECTION + EXISTDB_ROOT_COLLECTION
EXISTDB_TEST_GROUP = 'eulexistdb-test'

DATABASES = {}

logging.basicConfig(level=logging.DEBUG)