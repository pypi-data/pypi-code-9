# 主要提供api方式操作数据库同步的功能
# aliyun提供的python SDK不支持python3，因此稍稍改动了默认sdk，详情请diff 本项目的base.py和aliyun的base.py
from jiemoutils.aliyun.base import RestApi
from jiemoutils.funcs import pymysql
import time


# 模拟aliyun SDK中的ImportDatabaseBetweenInstances
class _SyncDb(RestApi):
    def __init__(self, domain='rds.aliyuncs.com',port=80):
        RestApi.__init__(self,domain, port)
        self.DBInfo = None
        self.DBInstanceId = None
        self.SourceDBInstanceId = None

    def getapiname(self):
        return 'rds.aliyuncs.com.ImportDatabaseBetweenInstances.2014-08-15'


# 模拟aliyun ImportDatabaseBetweenInstances
class _DescDb(RestApi):
    def __init__(self, domain='rds.aliyuncs.com',port=80):
        RestApi.__init__(self,domain, port)
        self.Action = 'DescribeDBInstanceAttribute'
        self.DBInstanceId = None

    def getapiname(self):
        return 'rds.aliyuncs.com.ImportDatabaseBetweenInstances.2014-08-15'


# 同步mysql
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


# 等待同步完成
def waitdb_synced(dbid):
    while True:
        time.sleep(10)
        r = descdb(dbid)
        status = r['Items']['DBInstanceAttribute'][0]['DBInstanceStatus']
        print('dbstatus is: ' + status)
        if status != 'ImportingFromOthers':
            break


# 获取db状态
def descdb(dbid):
    ddb = _DescDb()
    ddb.DBInstanceId = dbid
    return ddb.getResponse()


# 清空db的所有表，方便接下来的同步操作
def cleardb(**dbconf):
    con = pymysql.connect(**dbconf)
    cursor = con.cursor()
    cursor.execute('show tables')
    rs = cursor.fetchall()
    for r in rs:
        cursor.execute('drop table %s' % r[0])
