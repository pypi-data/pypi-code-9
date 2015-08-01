#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from pandas.io.sql import read_sql
import os
import yaml
import pymysql
import pandas as pd
import netifaces as ni

ni.ifaddresses('eth0')
LOCALIP = ni.ifaddresses('eth0')[2][0]['addr']

pd.set_option("display.precision",4)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

YMD=datetime.now().strftime("%Y-%m-%d")

CONFDIR='/singapore/config/' if os.name=='posix' else "c:\\singapore\\config\\"

yml_sentosa=yaml.load(open(CONFDIR+'sentosa.yml'))
yml_holiday=yaml.load(open(CONFDIR+'holiday.yml'))

#https://razvantudorica.com/08/example-for-singleton-decorator-pattern-in-python/
class Singleton:
  def __init__(self, klass):
    self.klass = klass
    self.instance = None
  def __call__(self, *args, **kwds):
    if self.instance == None:
      self.instance = self.klass(*args, **kwds)
    return self.instance

@Singleton
class CConfig:
  connection = None
  def get_connection(self):
    if self.connection is None:
      self.connection = pymysql.connect(host=yml_sentosa['DB']['DBHOST'],
                              port=3306,
                              user=yml_sentosa['DB']['DBUSER'],
                              passwd=yml_sentosa['DB']['DBPASS'],
                              db=yml_sentosa['DB']['DBNAME'])
    return self.connection

class CQuery(object):
    sqlcache = {}

    def __init__(self):
        self.dbconn = CConfig().get_connection()
        self.cur=self.dbconn.cursor()

    def cachedQuery(self, sql):
        if CQuery.sqlcache.has_key(sql):
            return CQuery.sqlcache[sql]
        tmp = read_sql(sql, self.dbconn, index_col='dt')
        CQuery.sqlcache[sql] = tmp
        return tmp

    def Query(self, sql):
        return read_sql(sql, self.dbconn, index_col='dt')

    def execute(self,sql):
        self.cur.execute(sql)

_node = yml_sentosa['strategies']
if _node.has_key("singleta"):
    SYMBOLS=_node['singleta']
if _node.has_key("pairs"):
    [SYMBOLS.extend(s.split('|')[1:3]) for s in _node['pairs']]
SYMBOLS=list(set(SYMBOLS))

ACCOUNT = yml_sentosa['global']['account']
TRADEINFODIR = yml_sentosa['linux']['TRADEINFODIR'] + os.sep + ACCOUNT

if __name__ == "__main__":
    print CConfig().get_connection()
    result=CQuery().Query("select * from transaction")
    print result
