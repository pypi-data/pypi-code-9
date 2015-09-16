import os

__author__ = 'rodak'

import sqlite3

from Jobber import Settings

def connect():
    return sqlite3.connect(Settings.sqlite_path, isolation_level=None, check_same_thread=False)

def init(db):
    f = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "JobDatabaseSQLite.sql"))
    str = f.read()
    db.connection.executescript(str)
    f.close()

def dict_factory(cursor, row):
    d = {}
    for idx,col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class DB():

    def __init__(self):
        self.connection = connect()
        self.connection.row_factory = dict_factory
        self.cursor = self.connection.cursor()

    def execute(self, query, params=[]):
        query = query.replace("%s", "?")
        try:
            self.cursor.execute(query, params)
        except (AttributeError, sqlite3.OperationalError):
            self.connection = connect()
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
        init(self)