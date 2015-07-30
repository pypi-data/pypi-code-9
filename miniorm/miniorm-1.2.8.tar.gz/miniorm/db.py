# coding=utf-8
# __author__ = 'ininwn@gmail.com'

import logging

logger = logging.getLogger("simpledb")

from mysql.connector import connection
from collections import OrderedDict


class Model(object):
    initialized = False

    @staticmethod
    def make(name, dbargkws, tablename=None):
        return type(tablename or name.lower(), (Model,), dict(tablename=tablename or name.lower(), dbargkws=dbargkws))

    @classmethod
    def connect(clz):
        if not clz.initialized:
            clz.conn = connection.MySQLConnection(**clz.dbargkws)
            clz.conn.set_autocommit(False)
            clz.initialized = True

    @classmethod
    def cursor(clz, buffered=True, dictionary=True):
        clz.connect()
        return clz.conn.cursor(buffered=buffered, dictionary=dictionary)

    @classmethod
    def get_by_id(clz, id, select_cols=None):
        c = clz.cursor()
        try:
            if select_cols:
                c.execute("select %s from %s where id =%s" % ("`" + "`,`".join(select_cols) + "`", clz.tablename, "%s"),
                          (id,))
            else:
                c.execute("select * from %s  where id =%s " % (clz.tablename, "%s"), (id,))
            return c.fetchone()
        finally:
            c.close()

    @classmethod
    def get_by_map(clz, params={}, start=0, limit=50, and_or="and", select_cols=None, order_by=None):
        c = clz.cursor()
        order_by = order_by and " order by " + ",".join(order_by) or ""
        try:
            if not params:
                if select_cols:
                    sql = "select %s from %s %s limit %s,%s" % (
                        "`" + "`,`".join(select_cols) + "`", clz.tablename, order_by, start, limit)
                    logger.debug(sql)
                    c.execute(sql)
                else:
                    sql = "select * from %s %s limit %s,%s" % (clz.tablename, order_by, start, limit)
                    logger.debug(sql)
                    c.execute(sql)
            else:
                conds, vals = Model.combine_fields(params)
                cond = (" " + and_or + " ").join(conds)

                if select_cols:
                    sql = "select %s from  %s where %s %s limit %s,%s" % (
                        "`" + "`,`".join(select_cols) + "`", clz.tablename, cond, order_by, start, limit)
                    logger.debug(sql + ", %s" % vals)
                    c.execute(sql, vals)
                else:
                    sql = "select * from %s where %s %s limit %s,%s" % (clz.tablename, cond, order_by, start, limit)
                    logger.debug(sql + ", %s" % vals)
                    c.execute(sql, vals)
            return c.fetchall()
        finally:
            c.close()

    @staticmethod
    def combine_fields(params):
        fields = []
        vals = []
        for field, val in params.items():
            if field.endswith("$match"):
                fields.append("match(`%s`) against (%%s) " % field[:-5])
            if field.endswith("$like"):
                fields.append("`%s` like %%s " % field[:-5])
            elif field.endswith("$gt"):
                fields.append("`%s` > %%s " % field[:-3])
            elif field.endswith("$gte"):
                fields.append("`%s` >= %%s " % field[:-4])
            elif field.endswith("$lt"):
                fields.append("`%s` < %%s " % field[:-3])
            elif field.endswith("$lte"):
                fields.append("`%s` <= %%s " % field[:-4])
            else:
                fields.append("`%s` %s %%s " % (field, val is None and "is" or "="))

            if field.endswith("$like"):
                vals.append("%%%s%%" % val)
            else:
                vals.append(val)
        return fields, vals

    @classmethod
    def count_by_map(clz, params={}, and_or="and", distinct=None):
        c = clz.cursor()

        try:
            if not params:
                sql = "select count(" + (
                    distinct and "distinct(" + distinct + ")" or "*") + ") as count from %s " % clz.tablename
                logger.debug(sql)
                c.execute(sql)
            else:
                conds, vals = Model.combine_fields(params)
                cond = (" " + and_or + " ").join(conds)
                sql = "select count(" + (
                    distinct and "distinct(" + distinct + ")" or "*") + ") as count from %s where %s" % (
                    clz.tablename, cond)
                logger.debug(sql + ", %s" % vals)
                c.execute(sql, vals)
            return c.fetchone()["count"]
        finally:
            c.close()

    @classmethod
    def delete_by_id(clz, id):
        c = clz.cursor()
        try:
            c.execute("delete from %s where id =%s" % (clz.tablename, "%s"), (id,))
            return c.rowcount
        finally:
            clz.commit()
            c.close()

    @classmethod
    def delete_by_map(clz, params={}, and_or="and"):
        if not params: raise Exception("params can not be empty or None! params:%s" % params)
        cond = and_or.join(["%s=%%(%s)s" % (k, k) for k in params.keys()])
        c = clz.cursor()
        try:
            c.execute("delete from %s where %s" % (clz.tablename, cond), params)
            return c.rowcount
        finally:
            clz.commit()
            c.close()

    @classmethod
    def commit(clz):
        clz.conn.commit()

    @classmethod
    def insert(clz, data, with_insert_id=True):
        if not data: return []
        data = type(data) in (tuple, list) and data or [data, ]
        inserts = []
        c = clz.cursor()
        try:
            for d in data:
                d = hasattr(d, "_asdict") and d._asdict() or d
                fields, vals = [], []
                for field, val in d.items():
                    if field.lower() == "id" and val is None:
                        continue
                    fields.append("`%s`" % field)
                    vals.append(val)
                sql = "insert into %s (%s) values(%s) " % (
                    clz.tablename, ",".join(fields), ",".join(["%s"] * len(fields)))

                logger.debug(sql + ", %s" % vals)
                c.execute(sql, vals)

                if with_insert_id:
                    if hasattr(d, "_replace"):
                        d = d._replace(id=c.lastrowid)
                        # print "attach id rep", c.lastrowid
                    elif type(d) in (dict, OrderedDict):
                        d["id"] = c.lastrowid
                        # print "attach id d[id]", c.lastrowid
                    else:
                        d.id = c.lastrowid
                        # print "attach id d.id", c.lastrowid
                inserts.append(d)
            return inserts
        finally:
            clz.commit()
            c.close()

    @classmethod
    def update(clz, data, where=None, and_or="and"):
        if not data: return [], []

        data = type(data) in (tuple, list) and data or [data, ]
        c = clz.cursor()
        updates, noeffects = [], []

        try:
            for d in data:
                if where:
                    w_conds, w_vals = Model.combine_fields(where)
                    w_cond = (" " + and_or + " ").join(w_conds)
                else:
                    w_cond = "`id`=%s"
                    if type(d) in (dict, OrderedDict) and "id" in d and d["id"] is not None:
                        w_vals = [d["id"], ]
                    elif hasattr(d, "id") and d.id is not None:
                        w_vals = [d.id, ]
                    else:
                        noeffects.append(d)
                        continue

                for p in data:
                    d = hasattr(p, "_asdict") and p._asdict() or p
                    fields, vals = [], []
                    for field, val in d.items():
                        if field.lower() == "id" and val is None:
                            continue
                        fields.append("`%s`=%%s" % field)
                        vals.append(val)
                    sql = "update %s set %s where %s" % (clz.tablename, ",".join(fields), w_cond)
                    vss = vals + w_vals
                    logger.debug(sql + ", %s" % vss)
                    c.execute(sql, vss)
                    if c.rowcount < 1:
                        noeffects.append(p)  # raise Exception("no data updated: sql:%s,data:%s"%(sql, str(p)))
                    else:
                        updates.append(p)
            return updates, noeffects
        finally:
            c.close()
            clz.commit()
