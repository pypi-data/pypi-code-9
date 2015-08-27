'''
Created on Mar 24, 2010

@author: rodak

'''

import os
import sys
import MySQLdb
import sqlite3
from . import Settings

def createMysqlConnection():
        return MySQLdb.connect(
            host = Settings.db_host,
            user = Settings.db_user,
            passwd = Settings.db_password,
            db = Settings.db_name)

def run_sql_file(filename, connection):
    file = open(filename, 'r')
    sql = " ".join(file.readlines())
    lines = sql.split(";")
    for line in lines:
        line = line.strip()
        if line != "":
            cursor = connection.cursor()
            cursor.execute(line)
            connection.commit()
            cursor.close()

def createSqliteConnection():
    return sqlite3.connect(Settings.sqlite_path, isolation_level=None, check_same_thread=False)

def createInMemorySqliteConnection():
    return sqlite3.connect(":memory:", isolation_level=None)

def dict_factory(cursor, row):
    d = {}
    for idx,col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def initSqliteDB(db):
    f = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "database/JobDatabaseSQLite.sql"))
    str = f.read()
    db.connection.executescript(str)
    f.close()

def initMysqlDB(db):
    run_sql_file(os.path.join(os.path.dirname(os.path.realpath(__file__)), "database/JobDatabase.sql"), db.connection)


class MysqlDB():

    def __init__(self, connection):
        self.connection = connection
        self.cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)

    def execute(self, query, params=[]):
        try:
            self.cursor.execute(query, params)
        except (AttributeError, MySQLdb.OperationalError):
            self.connection = createMysqlConnection()
            self.cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
            self.cursor.execute(query, params)
        return self.cursor

    def insert_id(self):
        return self.connection.insert_id()

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def close(self):
        self.connection.close()

    def init(self):
        initMysqlDB(self)

class SqliteDB():

    def __init__(self, connection):
        self.connection = connection
        self.connection.row_factory = dict_factory
        self.cursor = self.connection.cursor()

    def execute(self, query, params=[]):
        query = query.replace("%s", "?")
        try:
            self.cursor.execute(query, params)
        except (AttributeError, MySQLdb.OperationalError):
            self.connection = createSqliteConnection()
            self.connection.row_factory = dict_factory
            self.cursor = self.connection.cursor()
            self.cursor.execute(query, params)
        return self.cursor

    def insert_id(self):
        return self.cursor.lastrowid

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def close(self):
        self.connection.close()

    def init(self):
        initSqliteDB(self)


def createDB():
    try:
        return SqliteDB(createSqliteConnection())
    except AttributeError:
        return MysqlDB(createMysqlConnection())
