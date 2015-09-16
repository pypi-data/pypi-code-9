from . import JobDAO, Connection, JobStatus, JobAction, JobCreator as JC
import threading

__author__ = 'rodak'

'''
How to use a connection to database:

try:
   db = database.getDB()
   dao = database.dao(db)
   ...
finally:
   database.releaseDB(db)

Always release db if you don't need it anymore.

'''

dbData = threading.local()

def getDB():
    if "nr" not in dbData.__dict__:
        dbData.nr = 0
    if dbData.nr == 0:
        dbData.db = Connection.createDB()
    dbData.nr += 1
    return dbData.db

def releaseDB(db):
    dbData.nr -= 1
    if dbData.nr == 0:
        dbData.db.connection.close()
    if dbData.nr < 0:
        raise Exception("Inconsistent use of getDB and releaseDB.")

def dao(db):
    return JobDAO.JobDAO(db)

def context(handler):
    db = getDB()
    try:
        handler(db)
    finally:
        releaseDB(db)

JobDependency = JobDAO.Dependency
JobOption = JobDAO.Option
JobCreator = JC.JobCreator


jobStatus = JobStatus
jobAction = JobAction