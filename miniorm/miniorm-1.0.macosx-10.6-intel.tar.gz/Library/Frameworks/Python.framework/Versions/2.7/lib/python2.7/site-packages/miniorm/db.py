# coding=utf-8
# __author__ = 'ininwn@gmail.com'

import logging

logger = logging.getLogger("simpledb")

from mysql.connector import connection

class Model(object):
    initialized = False

    @staticmethod
    def make(name, dbargkws, tablename=None):
        return type(name, (Model,), dict(tablename=tablename or name.lower(), dbargkws=dbargkws))

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
                    logger.debug( sql)
                    c.execute(sql)
            else:
                conds, vals = Model.combine_fields(params)
                cond = (" " + and_or + " ").join(conds)

                if select_cols:
                    sql = "select %s from  %s where %s %s limit %s,%s" % (
                        "`" + "`,`".join(select_cols) + "`", clz.tablename, cond, order_by, start, limit)
                    logger.debug( sql , "%s"%vals)
                    c.execute(sql, vals)
                else:
                    sql = "select * from %s where %s %s limit %s,%s" % (clz.tablename, cond, order_by, start, limit)
                    logger.debug( sql+", %s"% vals)
                    c.execute(sql, vals)
            return c.fetchall()
        finally:
            c.close()

    @staticmethod
    def combine_fields(params):
        fields = []
        vals = []
        for field, val in params.items():
            if field.endswith("$like"):
                fields.append("`%s` like %%s " % field[:-5])
            elif field.endswith("$gt"):
                fields.append("`%s` > %%s " % field[:-3])
            elif field.endswith("$gte"):
                fields.append("`%s` >= %%s " % field[:-4])
            elif field.endswith("$gl"):
                fields.append("`%s` < %%s " % field[:-3])
            elif field.endswith("$gle"):
                fields.append("`%s` <= %%s " % field[:-4])
            else:
                fields.append("`%s` =%%s " % field)

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
                logger.debug( sql)
                c.execute(sql)
            else:
                conds, vals = Model.combine_fields(params)
                cond = (" " + and_or + " ").join(conds)
                sql = "select count(" + (
                    distinct and "distinct(" + distinct + ")" or "*") + ") as count from %s where %s" % (
                clz.tablename, cond)
                logger.debug( sql+"%s"%vals)
                c.execute(sql, vals)
            return c.fetchone()["count"]
        finally:
            c.close()

    @classmethod
    def delete_by_id(clz, id):
        c = clz.cursor()
        try:
            c.execute("delete from %s where id =%s" % (clz.tablename, "%s"), (id,))
        finally:
            clz.commit()
            c.close()
        return c.rowcount

    @classmethod
    def delete_by_map(clz, params={}, and_or="and"):
        if not params: raise Exception("params can not be empty or None! params:%s" % params)
        cond = and_or.join(["%s=%%(%s)s" % (k, k) for k in params.keys()])
        c = clz.cursor()
        try:
            c.execute("delete from %s where %s" % (clz.tablename, cond), params)
        finally:
            clz.commit()
            c.close()
        return c.rowcount

    @classmethod
    def commit(clz):
        clz.conn.commit()

    @classmethod
    def save(clz, data, pk="id", update_data_with_insert_id=True):
        data = type(data) in (tuple, list) and data or [data, ]
        params = [type(d) is not dict and d._asdict() or d for d in data]
        c = clz.cursor()
        updated, inserted, noteffected = [], [], []
        try:
            for i, p in enumerate(params):
                cols = []
                pkey, pval = None, None
                for k, v in p.items():
                    if k.lower() != pk:
                        cols.append(k)
                    else:
                        pkey = k
                        pval = v
                if not cols:
                    continue
                is_insert = pkey is None or pval is None
                if is_insert:  # insert
                    sql = "insert into %s (%s) values(%s) " % (
                        clz.tablename, "`" + "`,`".join(cols) + "`", ",".join(["%%(%s)s" % k for k in cols]))
                else:  # update
                    sql = "update %s set " % clz.tablename + ",".join(
                        ["`%s`=%%(%s)s" % (k, k) for k in cols]) + " where %s=%s" % (pkey, pval)
                logger.debug(sql)
                c.execute(sql, p)
                if c.rowcount < 1:
                    noteffected.append(data[i])  # raise Exception("no data updated: sql:%s,data:%s"%(sql, str(p)))
                else:
                    if is_insert:
                        d = data[i]
                        if update_data_with_insert_id:
                            if type(d) is not dict:
                                d = d._replace(id=c.lastrowid)
                            else:
                                d["id"] = c.lastrowid
                        inserted.append(d)
                    else:
                        updated.append(data[i])
            return inserted, updated, noteffected
        finally:
            c.close()
            clz.commit()
