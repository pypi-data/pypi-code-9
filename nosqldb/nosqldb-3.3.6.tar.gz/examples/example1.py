#!/usr/bin/python
# This example creates and drops a table

from nosqldb import Factory
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
        ddl = """DROP TABLE IF EXISTS Users2"""
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
        ddl = """CREATE TABLE Users2 (
            id INTEGER CHECK(id > 300),
            firstName STRING,
            lastName STRING,
            runner ENUM(slow,fast) DEFAULT slow,
            myEmbeddedRecord RECORD(firstField STRING, secondField INTEGER),
            myRec RECORD(a STRING),
            myMap MAP(INTEGER CHECK(ELEMENTOF(myMap) > 500)),
            myArray ARRAY(INTEGER),
            myBool BOOLEAN DEFAULT FALSE,
            PRIMARY KEY (SHARD(id, firstName), lastName)
        )"""
        store.execute_sync(ddl)
        logging.debug("Table creation succeeded")
        store.refresh_tables()
    except IllegalArgumentException, iae:
        logging.error("DDL failed.")
        logging.error(iae.message)


if __name__ == '__main__':

    add_runtime_params()
    setup_logging()
    store = open_store()
    do_create_table(store)
    do_drop_table(store)
    store.shutdown()
