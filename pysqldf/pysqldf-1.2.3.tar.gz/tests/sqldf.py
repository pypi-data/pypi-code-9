#!/usr/bin/env python
# -*- coding: utf-8 -*-


import pandas as pd
from pandas import DataFrame
from pysqldf import SQLDF, load_meat, load_births
from pandas.util.testing import assert_frame_equal
import string
import unittest
import os
import sqlite3


class SQLDFTest(unittest.TestCase):

    def setUp(self):
        self.default_df = DataFrame(
            [["l1", 1, 2], ["l2", 3, 4], ["l3", 4, 5]], columns=["label", "c1", "c2"])
        self.default_env = {"a": 1, "df": self.default_df}
        self.default_udfs = {"udf1": lambda x: x}

        class udaf1(object):

            def __init__(self):
                self.count = 0

            def step(self, x):
                self.count += 1

            def finalize(self):
                return self.count
        self.default_udafs = {"udaf1": udaf1}

    def tearDown(self):
        pass

    def test_constructor_with_default(self):
        sqldf = SQLDF(self.default_env)
        self.assertEqual(isinstance(sqldf, SQLDF), True)
        self.assertEqual(sqldf.env, self.default_env)
        self.assertEqual(sqldf.inmemory, True)
        self.assertEqual(sqldf._dbname, ":memory:")
        self.assertEqual(sqldf.udfs, {})
        self.assertEqual(sqldf.udafs, {})
        self.assertEqual(isinstance(sqldf.conn, sqlite3.Connection), True)

    def test_constructor_with_assign(self):
        sqldf = SQLDF(
            self.default_env,
            inmemory=False,
            udfs=self.default_udfs,
            udafs=self.default_udafs)
        self.assertEqual(isinstance(sqldf, SQLDF), True)
        self.assertEqual(sqldf.env, self.default_env)
        self.assertEqual(sqldf.inmemory, False)
        self.assertEqual(sqldf._dbname, ".pysqldf.db")
        self.assertEqual(sqldf.udfs, self.default_udfs)
        self.assertEqual(sqldf.udafs, self.default_udafs)
        self.assertEqual(isinstance(sqldf.conn, sqlite3.Connection), True)

    def test_destructor_with_inmemory_db(self):
        sqldf = SQLDF(self.default_env)
        conn = sqldf.conn
        self.assertRaises(
            sqlite3.OperationalError,
            lambda: conn.execute("select * from tbl;"))
        sqldf = None  # destruct
        self.assertRaises(
            sqlite3.ProgrammingError,
            lambda: conn.execute("select * from tbl;"))

    def test_destructor_with_fs_db(self):
        sqldf = SQLDF(self.default_env, inmemory=False)
        conn = sqldf.conn
        self.assertRaises(
            sqlite3.OperationalError,
            lambda: conn.execute("select * from tbl;"))
        self.assertEqual(os.path.exists(".pysqldf.db"), True)
        sqldf = None  # destruct
        self.assertRaises(
            sqlite3.ProgrammingError,
            lambda: conn.execute("select * from tbl;"))
        self.assertEqual(os.path.exists(".pysqldf.db"), False)

    def test_execute_method(self):
        sqldf = SQLDF(self.default_env)
        query = "select * from df;"
        result = sqldf.execute(query)
        assert_frame_equal(result, self.default_df)
        # table deleted
        self.assertRaises(
            sqlite3.OperationalError,
            lambda: sqldf.conn.execute(query))

    def test_execute_method_returning_none(self):
        births = load_births()
        result = SQLDF(locals()).execute(
            "select a from births limit 10;")  # col a not exists
        self.assertEqual(result, None)

    def test_execute_method_with_table_not_found(self):
        sqldf = SQLDF(self.default_env)
        self.assertRaises(
            Exception,
            lambda: sqldf.execute("select * from notable"))
        # table deleted
        self.assertRaises(sqlite3.OperationalError,
                          lambda: sqldf.conn.execute("select * from df;"))

    def test_execute_method_with_query_error(self):
        sqldf = SQLDF(self.default_env)
        self.assertEqual(sqldf.execute("select a from df uuuuuu;"), None)
        # table deleted
        self.assertRaises(sqlite3.OperationalError,
                          lambda: sqldf.conn.execute("select * from df;"))

    def test_extract_table_names_method(self):
        sqldf = SQLDF(self.default_env)
        tablenames = {
            "select * from df;": ["df"],
            "select * from df": ["df"],
            "select * from _": ["_"],
            "select * from 11;": [],
            "select * from 1ab;": [],
            "select * from a-b;": [],
            "select * from a.b;": [],
            "select a;": [],
            "select * from (select * from subq_df) f;": ["subq_df"],
            "select * from df d1 inner join df2 d2 on d1.id = d2.id;": ["df", "df2"],
            "select a, b c from df where c in (select foo from df2 inner join df3 on df2.id = df3.id);": ["df", "df2", "df3"],
            "select * from df where a in (select a from (select c from df2 where c in (select a from df3 inner join df4 on df3.id = df4.id)));": ["df", "df2", "df3", "df4"]
        }
        for query, tablename in tablenames.items():
            self.assertEqual(
                set(sqldf._extract_table_names(query)), set(tablename))

    def test_ensure_data_frame_method_nested_list(self):
        data = [[1, 2, 3], [4, 5, 6]]
        result = SQLDF(locals())._ensure_data_frame(data, "df")
        self.assertEqual(len(result), 2)
        self.assertEqual(list(result.columns), ["c0", "c1", "c2"])
        self.assertEqual(list(result.index), [0, 1])

    def test_ensure_data_frame_method_list_of_tuple(self):
        data = [(1, 2, 3), (4, 5, 6)]
        result = SQLDF(locals())._ensure_data_frame(data, "df")
        self.assertEqual(len(result), 2)
        self.assertEqual(list(result.columns), ["c0", "c1", "c2"])
        self.assertEqual(list(result.index), [0, 1])

    def test_ensure_data_frame_method_nested_tuple(self):
        data = ((1, 2, 3), (4, 5, 6))
        sqldf = SQLDF(locals())
        self.assertRaises(
            Exception,
            lambda: sqldf._ensure_data_frame(
                data,
                "df"))

    def test_ensure_data_frame_method_tuple_of_list(self):
        data = ([1, 2, 3], [4, 5, 6])
        sqldf = SQLDF(locals())
        self.assertRaises(
            Exception,
            lambda: sqldf._ensure_data_frame(
                data,
                "df"))

    def test_ensure_data_frame_method_list_of_dict(self):
        data = [{"a": 1, "b": 2, "c": 3}, {"a": 4, "b": 5, "c": 6}]
        result = SQLDF(locals())._ensure_data_frame(data, "df")
        self.assertEqual(len(result), 2)
        self.assertEqual(list(result.columns), ["a", "b", "c"])
        self.assertEqual(list(result.index), [0, 1])

    def test_write_table_method(self):
        df = DataFrame([[1, 2], [3, 4]], columns=["col1", "col2"])
        sqldf = SQLDF(locals())
        sqldf._write_table("tbl", df)
        # table created
        cursor = sqldf.conn.cursor()
        sq_type, name, tbl_name, rootpage, sql = list(
            cursor.execute("select * from sqlite_master where type='table';"))[0]
        self.assertEqual(name, "tbl")

    def test_write_table_method_col_with_left_bracket(self):
        df = DataFrame([[1]], columns=["col("])
        sqldf = SQLDF(locals())
        self.assertRaises(Exception, lambda: sqldf._write_table("tbl", df))

    def test_write_table_method_col_with_right_bracket(self):
        df = DataFrame([[1]], columns=["co)l"])
        sqldf = SQLDF(locals())
        self.assertRaises(Exception, lambda: sqldf._write_table("tbl", df))

    def test_write_table_method_garbage_table(self):
        df = [[1, 2], [3, [4]]]
        sqldf = SQLDF(locals())
        self.assertRaises(Exception, lambda: sqldf._write_table("tbl", df))
        # table destroyed
        cursor = sqldf.conn.cursor()
        tablemaster = list(cursor.execute("select * from sqlite_master where type='table';"))
        self.assertEqual(tablemaster, [])

    def test_del_table_method(self):
        sqldf = SQLDF(locals())
        cursor = sqldf.conn.cursor()
        # create table
        cursor.execute("create table deltbl(col);")
        sqldf._del_table(["deltbl"])
        self.assertEqual(
            list(
                cursor.execute("select * from sqlite_master where type='table';")),
            [])

    def test_del_table_method_not_exist_table(self):
        sqldf = SQLDF(locals())
        self.assertRaises(
            sqlite3.OperationalError,
            lambda: sqldf._del_table(
                ["deltblaaaaaaa"]))

    def test_set_udf_method(self):
        sqldf = SQLDF(locals())
        conn = sqldf.conn
        self.default_df.to_sql("df", conn)
        sqldf._set_udf(self.default_udfs)
        self.assertEqual(
            list(
                conn.execute("select udf1(label) from df;")), [
                ("l1",), ("l2",), ("l3",)])

    def test_set_udaf_method_with_agg_class(self):
        sqldf = SQLDF(locals())
        conn = sqldf.conn
        self.default_df.to_sql("df", conn)
        sqldf._set_udaf(self.default_udafs)
        self.assertEqual(
            list(
                conn.execute("select udaf1(label) from df;")), [
                (3,)])

    def test_set_udaf_method_with_agg_function(self):
        sqldf = SQLDF(locals())
        conn = sqldf.conn
        self.default_df.to_sql("df", conn)

        def agg_func(values):
            return len(values)
        sqldf._set_udaf({"mycount": agg_func})
        self.assertEqual(
            list(
                conn.execute("select mycount(label) from df;")), [
                (3,)])

    def test_udf(self):
        data = [{"a": 1, "b": 2, "c": 3}, {"a": 4, "b": 5, "c": 6}]

        def ten(x):
            return 10
        result = SQLDF(locals(), udfs={"ten": ten}).execute(
            "SELECT ten(a) AS ten FROM data;")
        self.assertEqual(len(result), 2)
        self.assertEqual(list(result.columns), ["ten"])
        self.assertEqual(list(result.index), [0, 1])
        self.assertEqual(list(result["ten"]), [10, 10])

    def test_udaf(self):
        data = [{"a": 1, "b": 2, "c": 3}, {"a": 4, "b": 5, "c": 6}]

        class mycount(object):

            def __init__(self):
                super(mycount, self).__init__()
                self.count = 0

            def step(self, x):
                self.count += x

            def finalize(self):
                return self.count
        result = SQLDF(locals(), udafs={"mycount": mycount}).execute(
            "select mycount(a) as mycount from data;")
        self.assertEqual(len(result), 1)
        self.assertEqual(list(result.columns), ["mycount"])
        self.assertEqual(list(result.index), [0])
        self.assertEqual(list(result["mycount"]), [1 + 4])

    def test_no_table(self):
        self.assertRaises(
            Exception, lambda: SQLDF(
                locals()).execute("select * from notable;"))

    def test_invalid_colname(self):
        data = [{"a": "valid", "(b)": "invalid"}]
        sqldf = SQLDF(locals())
        self.assertRaises(
            Exception,
            lambda: sqldf.execute("select * from data;"))

    def test_db_in_fs(self):
        data = [{"a": 1, "b": 2, "c": 3}, {"a": 4, "b": 5, "c": 6}]
        sqldf = SQLDF(locals(), inmemory=False)
        self.assertEqual(os.path.exists(".pysqldf.db"), True)
        sqldf = None  # run GC
        self.assertEqual(os.path.exists(".pysqldf.db"), False)


class QueryTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_select(self):
        df = pd.DataFrame({
            "letter_pos": [i for i in range(len(string.ascii_letters))],
            "l2": list(string.ascii_letters)
        })
        result = SQLDF(locals()).execute("select * from df limit 10;")
        self.assertEqual(len(result), 10)

    def test_join(self):

        df = pd.DataFrame({
            "letter_pos": [i for i in range(len(string.ascii_letters))],
            "l2": list(string.ascii_letters)
        })

        df2 = pd.DataFrame({
            "letter_pos": [i for i in range(len(string.ascii_letters))],
            "letter": list(string.ascii_letters)
        })

        result = SQLDF(locals()).execute(
            "select a.*, b.letter from df a inner join df2 b on a.l2 = b.letter limit 20;")
        self.assertEqual(len(result), 20)

    def test_query_with_spacing(self):

        df = pd.DataFrame({
            "letter_pos": [i for i in range(len(string.ascii_letters))],
            "l2": list(string.ascii_letters)
        })

        df2 = pd.DataFrame({
            "letter_pos": [i for i in range(len(string.ascii_letters))],
            "letter": list(string.ascii_letters)
        })

        result = SQLDF(locals()).execute(
            "select a.*, b.letter from df a inner join df2 b on a.l2 = b.letter limit 20;")
        self.assertEqual(len(result), 20)

        q = """
            select
            a.*
        from
            df a
        inner join
            df2 b
        on a.l2 = b.letter
        limit 20
        ;"""
        result = SQLDF(locals()).execute(q)
        self.assertEqual(len(result), 20)

    def test_query_single_list(self):

        mylist = [i for i in range(10)]

        result = SQLDF(locals()).execute("select * from mylist")
        self.assertEqual(len(result), 10)

    def test_query_list_of_lists(self):

        mylist = [[i for i in range(10)], [i for i in range(10)]]

        result = SQLDF(locals()).execute("select * from mylist")
        self.assertEqual(len(result), 2)

    def test_query_list_of_tuples(self):

        mylist = [tuple([i for i in range(10)]), tuple([i for i in range(10)])]

        result = SQLDF(locals()).execute("select * from mylist")
        self.assertEqual(len(result), 2)

    def test_subquery(self):
        kermit = pd.DataFrame({"x": range(10)})
        q = "select * from (select * from kermit) tbl limit 2;"
        result = SQLDF(locals()).execute(q)
        self.assertEqual(len(result), 2)

    def test_in(self):
        courseData = {
            "courseCode": ["TM351", "TU100", "M269"],
            "points": [30, 60, 30],
            "level": ["3", "1", "2"]
        }
        course_df = pd.DataFrame(courseData)
        q = "select * from course_df where courseCode in ( 'TM351', 'TU100' );"
        result = SQLDF(locals()).execute(q)
        self.assertEqual(len(result), 2)

    def test_in_with_subquery(self):
        programData = {
            "courseCode": [
                "TM351",
                "TM351",
                "TM351",
                "TU100",
                "TU100",
                "TU100",
                "M269",
                "M269",
                "M269"],
            "programCode": [
                "AB1",
                "AB2",
                "AB3",
                "AB1",
                "AB3",
                "AB4",
                "AB3",
                "AB4",
                "AB5"]}
        program_df = pd.DataFrame(programData)

        courseData = {
            "courseCode": ["TM351", "TU100", "M269"],
            "points": [30, 60, 30],
            "level": ["3", "1", "2"]
        }
        course_df = pd.DataFrame(courseData)

        q = """
            select * from course_df where courseCode in ( select distinct courseCode from program_df ) ;
          """
        result = SQLDF(locals()).execute(q)
        self.assertEqual(len(result), 3)

    def test_datetime_query(self):
        meat = load_meat()
        result = SQLDF(locals()).execute("select * from meat limit 10;")
        self.assertEqual(len(result), 10)
