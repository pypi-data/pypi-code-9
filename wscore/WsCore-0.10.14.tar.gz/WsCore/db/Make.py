#!/usr/bin/python
# -*- encoding:utf8 -*-

"""封装的mysql基类
@version:0.0.1
@author:waner(ShouCai Zhang)
@time:2015/06/03
"""
version = "0.0.1"

import sys

reload(sys)
sys.setdefaultencoding('utf8')

import datetime
from MySQLHelper import MySQLHelper
from jinja2 import Template
from WsCore.kenel.IO import IO


class Make():
    def __init__(self, kwargs):
        self.version = kwargs["version"]
        self.db_conn = kwargs["db_conn"]
        pass

    def execute(self, conn, tableName):
        sql_str = "show columns from %s" % tableName
        with MySQLHelper(conn) as sql:
            return sql.query(sql_str, None)

    def run(self, conn, tableName, model):
        ls = self.execute(conn, tableName)
        template = IO.read("model.html")
        info = {"model": model, "table": tableName, "time": datetime.date.today(), "version": self.version,
                "db_conn": self.db_conn}
        template = Template(template)
        content = template.render(rows=ls, info=info)
        print content


if __name__ == "__main__":
    DB_CONN = {'db_host': 'localhost', 'db_user': 'root', 'db_pwd': 'wanersoft', 'db_database': 'ws_2015'}
    # DB_SYSTEM_CONN  , DB_BOOK_CONN , DB_MEMBER_CONN , DB_ARTICLE_CONN, DB_REPORT_CONN
    make = Make({"version": "0.0.1", "db_conn": "DB_ARTICLE_CONN"})

    make.run(conn=DB_CONN, tableName="Ws_payrecords", model="PayRecords")

    pass