#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sqlite3 as sqlite
import pandas as pd
import numpy as np
from pandas.io.sql import to_sql, read_sql
import re
import os
import inspect


class SQLDF(object):
    def __init__(self, env, inmemory=True, udfs={}, udafs={}):
        super(SQLDF, self).__init__()
        self.env = env
        self.inmemory = inmemory
        self.udfs = udfs
        self.udafs = udafs
        if self.inmemory:
            self._dbname = ":memory:"
        else:
            self._dbname = ".pandasql.db"
        self.conn = sqlite.connect(self._dbname, detect_types=sqlite.PARSE_DECLTYPES|sqlite.PARSE_COLNAMES)
        self._set_udf(udfs)
        self._set_udaf(udafs)

    def __del__(self):
        self.conn.close()
        if not self.inmemory:
            os.remove(self._dbname)

    def execute(self, query):
        tables = self._extract_table_names(query)
        for table in tables:
            if table not in self.env:
                raise Exception("%s not found" % table)
            df = self.env[table]
            df = self._ensure_data_frame(df, table)
            self._write_table(table, df)

        try:
            result = read_sql(query, self.conn, index_col=None)
            if 'index' in result:
                del result['index']
        except Exception:
            result = None
        finally:
            self._del_table(tables)
        return result

    def _extract_table_names(self, query):
        "extracts table names from a sql query"
        # a good old fashioned regex. turns out this worked better than actually parsing the code
        rgx = '(?:FROM|JOIN)\s+([A-Za-z0-9_]+)'
        tables = re.findall(rgx, query, re.IGNORECASE)
        return list(set(tables))

    def _ensure_data_frame(self, obj, name):
        """
        obj a python object to be converted to a DataFrame

        take an object and make sure that it's a pandas data frame
        """
        try:
            df = pd.DataFrame(obj)
            columns = [col if isinstance(col, str) else "c%d" % i
                       for i, col in enumerate(df.columns)]
            df.columns = columns
        except Exception:
            raise Exception("%s is not a convertable data to Dataframe" % name)

        for col in df:
            if df[col].dtype==np.int64:
                df[col] = df[col].astype(np.float)
            elif isinstance(df[col].get(0), pd.tslib.Timestamp):
                df[col] = df[col].apply(lambda x: str(x))

        return df

    def _write_table(self, tablename, df):
        "writes a dataframe to the sqlite database"

        for col in df.columns:
            if re.search("[()]", col):
                msg = "please follow SQLite column naming conventions: "
                msg += "http://www.sqlite.org/lang_keywords.html"
                raise Exception(msg)

        to_sql(df, name=tablename, con=self.conn, flavor='sqlite')

    def _del_table(self, tablenames):
        for tablename in tablenames:
            self.conn.execute("drop table " + tablename)
        self.conn.commit()

    def _set_udf(self, udfs):
        for name, func in udfs.items():
            num_params = len(inspect.getargspec(func).args)
            self.conn.create_function(name, num_params, func)

    def _set_udaf(self, udafs):
        for name, agg_class in udafs.items():
            num_params = len(inspect.getargspec(agg_class.step).args) - 1 # subtract self
            self.conn.create_aggregate(name, num_params, agg_class)


if __name__ == '__main__':
    from pandas import DataFrame

    data = [
        ["hoge", 0,  1,  2,  3,  4],
        ["fuga", 5,  6,  7,  8,  9],
        ["hoge", 10, 11, 12, 13, 14],
        ["fuga", 15, 16, 17, 18, 19],
        ["hoge", 20, 21, 22, 23, 24]
    ]
    df = DataFrame(data, columns=["label", "a", "b", "c", "d", "e"])
    class mysum(object):
        def __init__(self):
            self.count = 0
        def step(self, val):
            self.count += val
        def finalize(self):
            return self.count

    sqldf = SQLDF(locals(), udfs={"half": lambda x: x / 2}, udafs={"mysum": mysum})
    print(sqldf.execute("select * from data;"))
    print(sqldf.execute("select sum(c1) from data;"))
    print(sqldf.execute("select half(c1) from data;"))
    print(sqldf.execute("select mysum(c2) from data;"))
    print(sqldf.execute("select MySum(c2) from data;"))
    print(sqldf.execute("select * from df;"))
    print(sqldf.execute("select sum(a) from df;"))
    print(sqldf.execute("select half(a) from df;"))
    print(sqldf.execute("select mysum(b) from df;"))
    print(sqldf.execute("select MySum(b) from df;"))
