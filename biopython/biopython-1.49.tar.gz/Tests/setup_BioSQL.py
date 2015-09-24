#!/usr/bin/env python
"""Preparation for BioSQL tests, setting passwords etc
"""
import os
from Bio import MissingExternalDependencyError
from BioSQL import BioSeqDatabase

##################################
# Start of user-editable section #
##################################

# You are expected to edit the following lines to match your system.
# The BioSQL unit tests will call this code, and will only run if it works.

# -- MySQL
DBDRIVER = 'MySQLdb'
DBTYPE = 'mysql'
# -- PostgreSQL
#DBDRIVER = 'psycopg'
#DBTYPE = 'pg'

# Constants for the database driver
DBHOST = 'localhost'
#DBUSER = 'root'
#DBPASSWD = ''
TESTDB = 'biosql_test'

DBUSER = 'pjcock'
DBPASSWD = 'pjcockmysql'

################################
# End of user-editable section #
################################

# Works for mysql and postgresql, not oracle
try:
    DBSCHEMA = "biosqldb-" + DBTYPE + ".sql"
except NameError:
    #This happens if the lines above are commented out
    message = "Enter your settings in Tests/setup_BioSQL.py " \
              "(not important if you do not plan to use BioSQL)."
    raise MissingExternalDependencyError(message)

# Uses the SQL file in the Tests/BioSQL directory -- try to keep this current
# with what is going on with BioSQL
SQL_FILE = os.path.join(os.getcwd(), "BioSQL", DBSCHEMA)
assert os.path.isfile(SQL_FILE), "Missing %s" % SQL_FILE

#Check the database driver is installed:
try :
    __import__(DBDRIVER)
except ImportError :
    message = "Install %s or correct Tests/setup_BioSQL.py "\
              "(not important if you do not plan to use BioSQL)." % DBDRIVER
    raise MissingExternalDependencyError(message)

#Could check the username, password and host work here,
#but this only seems to work for the first unit test
#that tries to import this file.


def create_database():
    """Create an empty BioSQL database."""
    # first open a connection to create the database
    server = BioSeqDatabase.open_database(driver = DBDRIVER,
                                          user = DBUSER, passwd = DBPASSWD,
                                          host = DBHOST)

    # Auto-commit: postgresql cannot drop database in a transaction
    try:
        server.adaptor.autocommit()
    except AttributeError:
        pass

    # drop anything in the database
    try:
        # with Postgres, can get errors about database still being used and
        # not able to be dropped. Wait briefly to be sure previous tests are
        # done with it.
        import time
        time.sleep(1)

        sql = r"DROP DATABASE " + TESTDB
        server.adaptor.cursor.execute(sql, ())
    except server.module.OperationalError: # the database doesn't exist
        pass
    except (server.module.IntegrityError,
            server.module.ProgrammingError), e: # ditto--perhaps
        if str(e).find('database "%s" does not exist' % TESTDB) > 0:
            pass
        else:
            raise
    # create a new database
    sql = r"CREATE DATABASE " + TESTDB
    server.adaptor.execute(sql, ())

    server.adaptor.conn.close()

    # now open a connection to load the database
    server = BioSeqDatabase.open_database(driver = DBDRIVER,
                                          user = DBUSER, passwd = DBPASSWD,
                                          host = DBHOST, db = TESTDB)
    server.load_database_sql(SQL_FILE)
    server.adaptor.conn.commit()
    server.adaptor.conn.close()
