#!/usr/bin/python
# This example:
#     1. Creates a table
#     2. Writes data in it with ExecuteUpdates
#     3. Reads that data with multi_get
#     4. Deletes data with multi_delete
#     5. Drops the table

from nosqldb import Factory
from nosqldb import Row
from nosqldb import Operation
from nosqldb import OperationType
from nosqldb import IllegalArgumentException
from nosqldb import ProxyConfig
from nosqldb import StoreConfig
from runtimeopts import add_runtime_params
from runtimeopts import store_host_port
from runtimeopts import proxy_host_port
from runtimeopts import store_name

### Constants needed for operations
from nosqldb import ONDB_OPERATION
from nosqldb import ONDB_OPERATION_TYPE
from nosqldb import ONDB_TABLE_NAME
from nosqldb import ONDB_ROW
from nosqldb import ONDB_ABORT_IF_UNSUCCESSFUL
from nosqldb import ONDB_PUT

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

    ### Create a table
    try:
        ddl = "CREATE TABLE myTable ("\
            "itemType STRING,"\
            "itemCategory STRING,"\
            "itemClass STRING,"\
            "itemColor STRING,"\
            "itemSize STRING,"\
            "price FLOAT,"\
            "inventoryCount INTEGER,"\
            "PRIMARY KEY (SHARD(itemType, itemCategory, itemClass),"\
            "            itemColor, itemSize)"\
        ")"
        store.execute_sync(ddl)
        store.refresh_tables()
        logging.debug("Table creation succeeded")
    except IllegalArgumentException, iae:
        logging.error("DDL failed.")
        logging.error(iae.message)


def add_op(op_t, table_name, if_unsuccess,
           item_type, item_cat, item_class,
           item_color, item_size, price, inv_count):

    global op_array

    row_d = {'itemType': item_type,
             'itemCategory': item_cat,
             'itemClass': item_class,
             'itemColor': item_color,
             'itemSize': item_size,
             'price': price,
             'inventoryCount': inv_count
             }
    op_row = Row(row_d)

    op_type = OperationType({ONDB_OPERATION_TYPE: op_t})
    op = Operation({
                    ONDB_OPERATION: op_type,
                    ONDB_TABLE_NAME: table_name,
                    ONDB_ROW: op_row,
                    ONDB_ABORT_IF_UNSUCCESSFUL: if_unsuccess
                   })
    op_array.append(op)


def do_write_data(store):
    try:
        res = store.execute_updates(op_array)
        if (len(res) == 3):
            logging.debug("Store write succeeded.")
        else:
            logging.debug("Store write failed.")
    except IllegalArgumentException, iae:
        logging.error("Could not write table.")
        logging.error(iae.message)
        sys.exit(-1)


def display_row(row):
    try:
            print "Retrieved row:"
            print "\tItem Type: %s" % row['itemType']
            print "\tCategory: %s" % row['itemCategory']
            print "\tClass: %s" % row['itemClass']
            print "\tSize: %s" % row['itemSize']
            print "\tColor: %s" % row['itemColor']
            print "\tPrice: %s" % row['price']
            print "\tInventory Count: %s" % row['inventoryCount']
    except KeyError, ke:
        logging.error("Row display failed. Bad key: %s" % ke.message)


def do_read_data(store):
    store.refresh_tables()
    try:
        shard_key_d = {"itemType": "Hats",
                       "itemCategory": "baseball",
                       "itemClass": "longbill"}

        rows = store.multi_get("myTable", shard_key_d, False)
        if not rows:
            logging.debug("Table retrieval failed")
        else:
            logging.debug("Table retrieval succeeded.")
            for r in rows:
                display_row(r)
    except IllegalArgumentException, iae:
        logging.error("Table retrieval failed.")
        logging.error(iae.message)


def do_multi_delete_data(store):
    try:
        # To delete a table row, just include a dictionary
        # that contains all the fields needed to create
        # the primary key.
        primary_key_d = {
            "itemType": "Hats",
            "itemCategory": "baseball",
            "itemClass": "longbill"
            }
        ret = store.multi_delete("myTable", primary_key_d)
        if ret == 3:
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
    add_op(ONDB_PUT, 'myTable', True,
            "Hats", "baseball", "longbill",
            "red", "small", 13.07, 107)
    add_op(ONDB_PUT, 'myTable', True,
            "Hats", "baseball", "longbill",
            "red", "medium", 14.07, 198)
    add_op(ONDB_PUT, 'myTable', True,
            "Hats", "baseball", "longbill",
            "red", "large", 15.07, 140)
    do_write_data(store)
    do_read_data(store)
    do_multi_delete_data(store)
    do_drop_table(store)
    store.close()
