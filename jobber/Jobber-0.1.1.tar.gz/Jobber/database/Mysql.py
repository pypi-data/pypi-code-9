import MySQLdb
import os

from Jobber import Settings

__author__ = 'rodak'

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

def connect():
    return MySQLdb.connect(
        host = Settings.db_host,
        user = Settings.db_user,
        passwd = Settings.db_password,
        db = Settings.db_name)

def init(db):
    run_sql_file(os.path.join(os.path.dirname(os.path.realpath(__file__)), "JobDatabase.sql"), db.connection)


class DB():

    def __init__(self):
        self.connection = connect()
        self.cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)

    def execute(self, query, params=[]):
        try:
            self.cursor.execute(query, params)
        except (AttributeError, MySQLdb.OperationalError):
            self.connection = connect()
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
        init(self)