#!/usr/bin/python
# This example:
#     1. Creates a table
#     2. Writes data in it
#     3. Reads that data
#     4. Deletes the data
#     5. Drops the table

from nosqldb import Factory
from nosqldb import Row
from nosqldb import IllegalArgumentException
from nosqldb import ProxyConfig
from nosqldb import StoreConfig
from runtimeopts import add_runtime_params
from runtimeopts import store_host_port
from runtimeopts import proxy_host_port
from runtimeopts import store_name

import logging
import sys

# default store_name, store_host_port and proxy_host_port are
# defined in runtimeopts.py


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
    kvproxyconfig = ProxyConfig()
    return Factory.open(proxy_host_port, kvstoreconfig, kvproxyconfig)


# drop table statement
def do_drop_table(store):
    ### Drop the table if it exists it can be recreated
    try:
        ddl = """DROP TABLE IF EXISTS myTable"""
        store.execute_sync(ddl)
        logging.debug("Table drop succeeded")
        store.refresh_tables()
    except IllegalArgumentException, iae:
        logging.error("DDL failed.")
        logging.error(iae.message)
        return


def do_create_table(store):
    ### Drop table if exists
    do_drop_table(store)

    ### Create a table
    try:
        ddl = """CREATE TABLE myTable (
            item STRING,
            description STRING,
            count INTEGER,
            percentage FLOAT,
            PRIMARY KEY (item)
        )"""
        store.execute_sync(ddl)
        logging.debug("Table creation succeeded")
        store.refresh_tables()
    except IllegalArgumentException, iae:
        logging.error("DDL failed.")
        logging.error(iae.message)


def do_write_data(store):
    store.refresh_tables()
    row_d = {'item': 'bolts',
             'description': "Hex head, stainless",
             'count': 5,
             'percentage': 0.2173913}
    row = Row(row_d)
    try:
        store.put("myTable", row)
        logging.debug("Store write succeeded.")
    except IllegalArgumentException, iae:
        logging.error("Could not write table.")
        logging.error(iae.message)


def display_row(row):
    try:
            print "Retrieved row:"
            print "\tItem: %s" % row['item']
            print "\tDescription: %s" % row['description']
            print "\tCount: %s" % row['count']
            print "\tPercentage: %s" % row['percentage']
            print "\n"
    except KeyError, ke:
        logging.error("Row display failed. Bad key: %s" % ke.message)


def do_read_data(store):
    try:
        primary_key_d = {"item": "bolts"}
        row = store.get("myTable", primary_key_d)
        if not row:
            logging.debug("Row retrieval failed")
        else:
            logging.debug("Row retrieval succeeded.")
            display_row(row)
    except IllegalArgumentException, iae:
        logging.error("Row retrieval failed.")
        logging.error(iae.message)
        return
    except KeyError, ke:
        logging.error("Row display failed. Bad key: %s" % ke.message)


def do_delete_data(store):
    try:
        # To delete a table row, just include a dictionary
        # that contains all the fields needed to create
        # the primary key.
        primary_key_d = {"item": "bolts"}
        ret = store.delete("myTable", primary_key_d)
        if ret[0]:
            logging.debug("Row deletion succeeded")
        else:
            logging.debug("Row deletion failed.")
    except IllegalArgumentException, iae:
        logging.error("Row deletion failed.")
        logging.error(iae.message)
        return


if __name__ == '__main__':

    add_runtime_params()
    setup_logging()
    store = open_store()
    do_create_table(store)
    do_write_data(store)
    do_read_data(store)
    do_delete_data(store)
    do_drop_table(store)
    store.close()
