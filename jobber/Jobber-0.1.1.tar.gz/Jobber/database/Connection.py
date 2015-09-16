'''
Created on Mar 24, 2010

@author: rodak

'''
from Jobber import Settings

from . import Mysql
from . import Sqlite3


def createMysqlDB():
    return Mysql.DB()

def createSqliteDB():
    return Sqlite3.DB()

try:
    sqlitePath = Settings.sqlite_path
    createDB = createSqliteDB
except AttributeError:
    createDB = createMysqlDB