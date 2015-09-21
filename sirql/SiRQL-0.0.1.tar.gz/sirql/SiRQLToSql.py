def __lt(c, param_id=0):
    return '%s < %s' % (c.field, c.parameter[param_id])


def __gt(c, param_id=0):
    return '%s > %s' % (c.field, c.parameter[param_id])


def __between(c):
    return '%s AND %s' % (__gt(c, param_id=0), __lt(c, param_id=1))


def __like(c, param_id=0):
    return "%s LIKE %s" % (c.field, c.parameter[param_id])


def __eq(c):
    return '(%s)' % ' OR '.join(map(lambda p: "%s = %s" % (c.field, p), c.parameter))


def __is(c, param_id=0):
    return '%s IS %s' % (c.field, c.parameter[param_id])


def __generate_condition(c):
    sql_condition = __KEYWORDS[c.operator.lower()](c)
    if c.negated:
        sql_condition = 'NOT (%s)' % sql_condition
    return sql_condition


def convert(conditions):
    sql_conditions = map(lambda c: __generate_condition(c), conditions)
    return " AND ".join(sql_conditions)


__KEYWORDS = {'lt': __lt,
              'gt': __gt,
              'between': __between,
              'like': __like,
              'eq': __eq,
              'is': __is}
