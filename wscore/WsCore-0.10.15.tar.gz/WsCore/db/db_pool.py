#!/usr/bin/python
# -*- coding:utf-8 -*-

version = "0.0.1"

import sys

reload(sys)
sys.setdefaultencoding('utf8')

from DBUtils.PooledDB import PooledDB
import MySQLdb
import time


class db_pool:
    pool = {}

    @staticmethod
    def get(db_config):
        db_name = db_config['db_database']
        try:
            if isinstance(db_name, unicode):
                db_name = db_name.encode("utf8")
            if db_pool.pool.get(db_name):
                return db_pool.pool.get(db_name)
            else:
                tmp_pool = PooledDB(MySQLdb,
                                    ["SET NAMES utf8", "SET CHARACTER SET utf8"],
                                    host=db_config['db_host'],
                                    user=db_config['db_user'],
                                    passwd=db_config['db_pwd'],
                                    db=db_name,
                                    charset="utf8")
                tmp_pool.charset = "utf8"
                db_pool.pool[db_name] = tmp_pool
                return db_pool.pool[db_name]
        except Exception, e:
            time.sleep(5)
            return db_pool.get(db_name)