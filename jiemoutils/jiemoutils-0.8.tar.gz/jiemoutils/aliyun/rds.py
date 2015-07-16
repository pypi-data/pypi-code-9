from jiemoutils.aliyun.base import RestApi
from jiemoutils.funcs import pymysql
import time


class _SyncDb(RestApi):
    def __init__(self, domain='rds.aliyuncs.com',port=80):
        RestApi.__init__(self,domain, port)
        self.DBInfo = None
        self.DBInstanceId = None
        self.SourceDBInstanceId = None

    def getapiname(self):
        return 'rds.aliyuncs.com.ImportDatabaseBetweenInstances.2014-08-15'


class _DescDb(RestApi):
    def __init__(self, domain='rds.aliyuncs.com',port=80):
        RestApi.__init__(self,domain, port)
        self.Action = 'DescribeDBInstanceAttribute'
        self.DBInstanceId = None

    def getapiname(self):
        return 'rds.aliyuncs.com.ImportDatabaseBetweenInstances.2014-08-15'


def syncdb(dbid_src, dbid_dst, dbname, wait=True):
    sdb = _SyncDb()
    sdb.DBInstanceId = dbid_dst
    sdb.SourceDBInstanceId = dbid_src
    sdb.DBInfo = '{"DBNames":["%s"]}' % dbname
    resp = sdb.getResponse()
    if 'Code' in resp:
        print('error occure ' + str(resp))
    if wait:
        waitdb_synced(dbid_dst)
    return resp

def waitdb_synced(dbid):
    while True:
        time.sleep(10)
        r = descdb(dbid)
        status = r['Items']['DBInstanceAttribute'][0]['DBInstanceStatus']
        print('dbstatus is: ' + status)
        if status != 'ImportingFromOthers':
            break

def descdb(dbid):
    ddb = _DescDb()
    ddb.DBInstanceId = dbid
    return ddb.getResponse()


def cleardb(**dbconf):
    con = pymysql.connect(**
                          dbconf)
    cursor = con.cursor()
    cursor.execute('show tables')
    rs = cursor.fetchall()
    for r in rs:
        cursor.execute('drop table %s' % r[0])
