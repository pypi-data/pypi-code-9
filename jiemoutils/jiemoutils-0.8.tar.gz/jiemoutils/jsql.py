from django.db import connection


def raw_query(sql, *arg):
    cur = connection.cursor()
    cur.execute(sql, arg)
    return cur.fetchall()


def query(sql, *arg):
    cur = connection.cursor()
    cur.execute(sql, arg)
    r = cur.fetchall()
    desc = cur.description
    return [dict(zip([col[0] for col in desc], row)) for row in r]


def query_one_row(sql, *arg):
    return query(sql, *arg)[0]


def query_one_col(sql, *arg):
    return [r[0] for r in raw_query(sql, arg)]

def query_value(sql, *arg):
    return raw_query(sql, *arg)[0]
