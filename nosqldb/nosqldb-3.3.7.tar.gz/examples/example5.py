#!/usr/bin/python
# This example:
#     1. Creates a table
#     2. Writes data in it with ExecuteUpdates
#     3. Iterates over the data
#     4. Drops the table

from nosqldb import Factory
from nosqldb import Row
from nosqldb import FieldRange
from nosqldb import MultiRowOptions
from nosqldb import IllegalArgumentException
from nosqldb import ProxyConfig
from nosqldb import StoreConfig
from runtimeopts import add_runtime_params
from runtimeopts import store_host_port
from runtimeopts import proxy_host_port
from runtimeopts import store_name

## FieldRange constants
from nosqldb import ONDB_FIELD
from nosqldb import ONDB_START_VALUE
from nosqldb import ONDB_END_VALUE
from nosqldb import ONDB_START_INCLUSIVE
from nosqldb import ONDB_END_INCLUSIVE

## Needed to set a FieldRange for a table_iterator
from nosqldb import ONDB_FIELD_RANGE

import logging
import sys

# default store_name, store_host_port and proxy_host_port are
# defined in runtimeopts.py

op_array = []


# set logging level to debug and log to stdout
def setup_logging():
    # turn on logging in the python driver in DEBUG level
    StoreConfig.change_log("DEBUG")
    # add it the stdout handler
    nosqlLogger = logging.getLogger("nosqldb")

    logger = logging.StreamHandler(sys.stdout)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('\t%(levelname)s - %(message)s')
    logger.setFormatter(formatter)
    nosqlLogger.addHandler(logger)


# configure and open the store
def open_store():

    kvstoreconfig = StoreConfig(store_name, [store_host_port])
    StoreConfig.change_log("DEBUG", None)
    kvproxyconfig = ProxyConfig()

    return Factory.open(proxy_host_port, kvstoreconfig, kvproxyconfig)


# drop table statement
def do_drop_table(store):
    ### Drop the table if it exists it can be recreated
    try:
        ddl = """DROP TABLE IF EXISTS myTable"""
        store.execute_sync(ddl)
        store.refresh_tables()
        logging.debug("Table drop succeeded")
    except IllegalArgumentException, iae:
        logging.error("DDL failed.")
        logging.error(iae.message)
        return


def do_create_table(store):
    ### Drop table if exists
    do_drop_table(store)

    try:
        ### Create a table
        ddl = """CREATE TABLE myTable (
            surname STRING, \
            familiarName STRING, \
            userID STRING, \
            phonenumber STRING, \
            address STRING, \
            email STRING, \
            dateOfBirth STRING, \
            PRIMARY KEY (SHARD(surname, familiarName), userID)
        )"""
        store.execute_sync(ddl)
        logging.debug("Table creation succeeded")

        #### Define an index
        ddl = "CREATE INDEX DoB ON myTable (dateOfBirth)"
        store.execute_sync(ddl)
        logging.debug("Index creation succeeded")
    except IllegalArgumentException, iae:
        logging.error("DDL failed.")
        logging.error(iae.message)


def do_write_row(store, surname, famName, uid, phone, address,
                 email, DoB):
    store.refresh_tables()
    row_d = {'surname': surname,
             'familiarName': famName,
             'userID': uid,
             'phonenumber': phone,
             'address': address,
             'email': email,
             'dateOfBirth': DoB
               }
    row = Row(row_d)
    try:
        store.put("myTable", row)
        logging.debug("Store write succeeded.")
    except IllegalArgumentException, iae:
        logging.error("Could not write table.")
        logging.error(iae.message)
        sys.exit(-1)


def do_write_data(store):
    do_write_row(store, "Anderson", "Pete", "panderson",
                 "555-555-5555", "1122 Somewhere Court",
                 "panderson@example.com", "1994-05-01")
    do_write_row(store, "Andrews", "Veronica", "vandrews",
                 "666-666-6666", "5522 Nowhere Court",
                 "vandrews@example.com", "1973-08-21")
    do_write_row(store, "Bates", "Pat", "pbates",
                 "777-777-7777", "12 Overhere Lane",
                 "pbates@example.com", "1988-02-20")
    do_write_row(store, "Macar", "Tarik", "tmacar",
                 "888-888-8888", "100 Overthere Street",
                 "tmacar@example.com", "1990-05-17")


def display_row(row):
    try:
            print "Retrieved row:"
            print "\tSurname: %s" % row['surname']
            print "\tFamiliar Name: %s" % row['familiarName']
            print "\tUser ID: %s" % row['userID']
            print "\tPhone: %s" % row['phonenumber']
            print "\tAddress: %s" % row['address']
            print "\tEmail: %s" % row['email']
            print "\tDate of Birth: %s" % row['dateOfBirth']
            print "\n"
    except KeyError, ke:
        logging.error("Row display failed. Bad key: %s" % ke.message)


def do_iterate_data(store):
    store.refresh_tables()

    field_range = FieldRange({
                             ONDB_FIELD: "surname",
                             ONDB_START_VALUE: "Anderson",
                             ONDB_END_VALUE: "Bates",
                             ONDB_START_INCLUSIVE: True,
                             ONDB_END_INCLUSIVE: False
                             })

    mro = MultiRowOptions({ONDB_FIELD_RANGE: field_range})

    try:
        row_list = store.table_iterator("myTable", None, False, mro)
        if not row_list:
            logging.debug("Table retrieval failed")
        else:
            logging.debug("Table retrieval succeeded.")
            for r in row_list:
                display_row(r)
    except IllegalArgumentException, iae:
        logging.error("Table retrieval failed.")
        logging.error(iae.message)


if __name__ == '__main__':

    add_runtime_params()
    setup_logging()
    store = open_store()
    do_create_table(store)
    do_write_data(store)
    do_iterate_data(store)
    do_drop_table(store)
    store.close()

