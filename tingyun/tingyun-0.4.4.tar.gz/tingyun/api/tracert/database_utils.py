import re
import weakref

"""this module implement the database trace tools
"""

_sql_statements = weakref.WeakValueDictionary()


_parse_operation_p = r'(\w+)'
_parse_operation_re = re.compile(_parse_operation_p)
_identifier_re = re.compile('[\',"`\[\]\(\)]*')

_uncomment_sql_p = r'/\*.*?\*/'
_uncomment_sql_re = re.compile(_uncomment_sql_p, re.DOTALL)

_normalize_params_1_p = r'%\([^)]*\)s'
_normalize_params_1_re = re.compile(_normalize_params_1_p)
_normalize_params_2_p = r'%s'
_normalize_params_2_re = re.compile(_normalize_params_2_p)
_normalize_params_3_p = r':\w+'
_normalize_params_3_re = re.compile(_normalize_params_3_p)

_normalize_values_p = r'\([^)]+\)'
_normalize_values_re = re.compile(_normalize_values_p)

_normalize_whitespace_1_p = r'\s+'
_normalize_whitespace_1_re = re.compile(_normalize_whitespace_1_p)
_normalize_whitespace_2_p = r'\s+(?!\w)'
_normalize_whitespace_2_re = re.compile(_normalize_whitespace_2_p)
_normalize_whitespace_3_p = r'(?<!\w)\s+'
_normalize_whitespace_3_re = re.compile(_normalize_whitespace_3_p)

_parse_identifier_1_p = r'"((?:[^"]|"")+)"'
_parse_identifier_2_p = r"'((?:[^']|'')+)'"
_parse_identifier_3_p = r'`((?:[^`]|``)+)`'
_parse_identifier_4_p = r'\[\s*(\S+)\s*\]'
_parse_identifier_5_p = r'\(\s*(\S+)\s*\)'
_parse_identifier_6_p = r'([^\s\(\)\[\],]+)'

_parse_identifier_p = ''.join(('(', _parse_identifier_1_p, '|', _parse_identifier_2_p, '|', _parse_identifier_3_p, '|',
                               _parse_identifier_4_p, '|', _parse_identifier_5_p, '|', _parse_identifier_6_p, ')'))

_parse_from_p = '\s+FROM\s+' + _parse_identifier_p
_parse_from_re = re.compile(_parse_from_p, re.IGNORECASE)
_parse_into_p = '\s+INTO\s+' + _parse_identifier_p
_parse_into_re = re.compile(_parse_into_p, re.IGNORECASE)
_parse_update_p = '\s*UPDATE\s+' + _parse_identifier_p
_parse_update_re = re.compile(_parse_update_p, re.IGNORECASE)
_parse_table_p = '\s+TABLE\s+' + _parse_identifier_p
_parse_table_re = re.compile(_parse_table_p, re.IGNORECASE)

_parse_call_p = r'\s*CALL\s+(?!\()(\w+)'
_parse_call_re = re.compile(_parse_call_p, re.IGNORECASE)
_parse_show_p = r'\s*SHOW\s+(.*)'
_parse_show_re = re.compile(_parse_show_p, re.IGNORECASE | re.DOTALL)
_parse_set_p = r'\s*SET\s+(.*?)\W+.*'
_parse_set_re = re.compile(_parse_set_p, re.IGNORECASE | re.DOTALL)
_parse_exec_p = r'\s*EXEC\s+(?!\()(\w+)'
_parse_exec_re = re.compile(_parse_exec_p, re.IGNORECASE)
_parse_execute_p = r'\s*EXECUTE\s+(?!\()(\w+)'
_parse_execute_re = re.compile(_parse_execute_p, re.IGNORECASE)
_parse_alter_p = r'\s*ALTER\s+(?!\()(\w+)'
_parse_alter_re = re.compile(_parse_alter_p, re.IGNORECASE)


_int_re = re.compile(r'(?<!:)\b\d+\b')
_single_quotes_p = "'(?:[^']|'')*'"
_double_quotes_p = '"(?:[^"]|"")*"'
_any_quotes_p = _single_quotes_p + '|' + _double_quotes_p

_single_quotes_re = re.compile(_single_quotes_p)
_double_quotes_re = re.compile(_double_quotes_p)
_any_quotes_re = re.compile(_any_quotes_p)
_quotes_default = _single_quotes_re

_quotes_table = {
    'MySQLdb': _any_quotes_re,
    'pymysql': _any_quotes_re,
    'oursql': _any_quotes_re,
}

plugin_db_mapping = {
    "MySQLdb": "MySQL",
    "cx_Oracle": "Oracle",
}


_explain_plan_table = {
    'MySQLdb': ('EXPLAIN', ('select',)),
    'ibm_db_dbi': ('EXPLAIN', ('select', 'insert', 'update', 'delete')),
    'oursql': ('EXPLAIN', ('select',)),
    'pymysql': ('EXPLAIN', ('select',)),
    'postgresql.interface.proboscis.dbapi2': ('EXPLAIN', ('select', 'insert', 'update', 'delete')),
    'psycopg2': ('EXPLAIN', ('select', 'insert', 'update', 'delete')),
    'psycopg2ct': ('EXPLAIN', ('select', 'insert', 'update', 'delete')),
    'sqlite3.dbapi2': ('EXPLAIN QUERY PLAN', ('select', 'insert', 'update', 'delete')),
}


def _extract_identifier(token):
    return _identifier_re.sub('', token).strip().lower()


def _parse_default(sql, regex):
    match = regex.search(sql)
    return match and _extract_identifier(match.group(1)) or ''


def _parse_select(sql, dbapi):
    m = _parse_from_re.search(sql)
    return m and next(s for s in m.groups()[1:] if s).lower() or ''


def _parse_delete(sql, dbapi):
    m = _parse_from_re.search(sql)
    return m and next(s for s in m.groups()[1:] if s).lower() or ''


def _parse_insert(sql, dbapi):
    m = _parse_into_re.search(sql)
    return m and next(s for s in m.groups()[1:] if s).lower() or ''


def _parse_update(sql, dbapi):
    m = _parse_update_re.search(sql)
    return m and next(s for s in m.groups()[1:] if s).lower() or ''


def _parse_create(sql, dbapi):
    m = _parse_table_re.search(sql)
    return m and next(s for s in m.groups()[1:] if s).lower() or ''


def _parse_drop(sql, dbapi):
    m = _parse_table_re.search(sql)
    return m and next(s for s in m.groups()[1:] if s).lower() or ''


def _parse_call(sql, dbapi):
    return _parse_default(sql, _parse_call_re)


def _parse_show(sql, dbapi):
    return _parse_default(sql, _parse_show_re)


def _parse_set(sql, dbapi):
    return _parse_default(sql, _parse_set_re)


def _parse_exec(sql, dbapi):
    return _parse_default(sql, _parse_exec_re)


def _parse_execute(sql, dbapi):
    return _parse_default(sql, _parse_execute_re)


def _parse_alter(sql, dbapi):
    return _parse_default(sql, _parse_alter_re)


_operation_table = {
    'select': _parse_select,
    'delete': _parse_delete,
    'insert': _parse_insert,
    'update': _parse_update,
    'create': _parse_create,
    'drop': _parse_drop,
    'call': _parse_call,
    'show': _parse_show,
    'set': _parse_set,
    'exec': _parse_exec,
    'execute': _parse_execute,
    'alter': _parse_alter,
}


def _parse_operation(sql, dbapi):
    match = _parse_operation_re.search(sql)
    operation = match and match.group(1).lower() or ''
    return operation if operation in _operation_table else ''


def _parse_target(sql, dbapi, operation):
    parse = _operation_table.get(operation, None)
    return parse and parse(sql, dbapi) or ''


def _uncomment_sql(sql, dbapi):
    return _uncomment_sql_re.sub('', sql)


def _dbapi_name(dbapi):
    return dbapi and hasattr(dbapi, '__name__') and dbapi.__name__ or dbapi


def _obfuscate_sql(sql, dbapi=None):
    """
    :param sql:
    :param dbapi:
    :return:
    """
    name = _dbapi_name(dbapi)
    quotes_re = _quotes_table.get(name, _quotes_default)

    # Substitute quoted strings first.
    sql = quotes_re.sub('?', sql)

    # Replace straight integer values. This will pick up
    # integers by themselves but also as part of floating point
    # numbers. Because of word boundary checks in pattern will
    # not match numbers within identifier names.
    sql = _int_re.sub('?', sql)

    return sql


def _normalize_sql(sql, dbapi):
    """
    :param sql:
    :param dbapi:
    :return:
    """
    sql = _normalize_params_1_re.sub('?', sql)

    # Collapse any parenthesised set of values to a single value.
    sql = _normalize_values_re.sub('(?)', sql)

    # Convert '%s', ':1' and ':name' param styles to '?'.
    sql = _normalize_params_2_re.sub('?', sql)
    sql = _normalize_params_3_re.sub('?', sql)

    # Strip leading and trailing white space.
    sql = sql.strip()

    # Collapse multiple white space to single white space.
    sql = _normalize_whitespace_1_re.sub(' ', sql)

    # Drop spaces adjacent to identifier except for case where
    # identifiers follow each other.
    sql = _normalize_whitespace_2_re.sub('', sql)
    sql = _normalize_whitespace_3_re.sub('', sql)

    return sql


def _explain_plan(sql, dbapi, connect_params, cursor_params, execute_params):
    """
    :param sql:
    :param dbapi:
    :param connect_params:
    :param cursor_params:
    :param execute_params:
    :return:
    """
    if dbapi is None:
        return None

    if type(dbapi) == type(''):
        return None

    name = _dbapi_name(dbapi)

    if name is None:
        return None

    if connect_params is None or cursor_params is None or execute_params is None:
        return None
    if cursor_params is None:
        return None
    if execute_params is None:
        return None

    command, operations = _explain_plan_table.get(name, (None, None))
    if not command:
        return None

    operation = _parse_operation(sql, dbapi)
    if operation not in operations:
        return None

    query = '%s %s' % (command, sql)
    args, kwargs = connect_params
    try:
        connection = dbapi.connect(*args, **kwargs)
        try:
            args, kwargs = cursor_params
            cursor = connection.cursor(*args, **kwargs)
            try:
                args, kwargs = execute_params
                cursor.execute(query, *args, **kwargs)
                columns = []
                if cursor.description:
                    for column in cursor.description:
                        columns.append(column[0])
                rows = cursor.fetchall()
                if not columns and not rows:
                    return None

                db_name = plugin_db_mapping.get(name, "Unknown")
                return {"dialect": db_name, "keys": columns, "values": [[str(t) for t in r] for r in rows]}
            except Exception:
                pass
            finally:
                cursor.close()
        finally:
            try:
                connection.rollback()
            except (AttributeError, dbapi.NotSupportedError):
                pass
            connection.close()
    except Exception:
        pass

    return None


class SQLStatement(object):
    def __init__(self, sql, dbapi=None):
        self.sql = sql
        self.dbapi = dbapi

        self._operation = None
        self._target = None
        self._uncommented = None
        self._obfuscated = None
        self._normalized = None
        self._identifier = None

    @property
    def operation(self):
        if self._operation is None:
            self._operation = _parse_operation(self.uncommented, self.dbapi)

        return self._operation

    @property
    def target(self):
        if self._target is None:
            self._target = _parse_target(self.uncommented, self.dbapi, self.operation)
        return self._target

    @property
    def uncommented(self):
        if self._uncommented is None:
            self._uncommented = _uncomment_sql(self.sql, self.dbapi)
        return self._uncommented

    @property
    def obfuscated(self):
        if self._obfuscated is None:
            self._obfuscated = _obfuscate_sql(self.uncommented, self.dbapi)
        return self._obfuscated

    @property
    def normalized(self):
        if self._normalized is None:
            self._normalized = _normalize_sql(self.obfuscated, self.dbapi)
        return self._normalized

    @property
    def identifier(self):
        if self._identifier is None:
            self._identifier = hash(self.normalized)
        return self._identifier

    def formatted(self, sql_format):
        if sql_format == 'off':
            return ''

        elif sql_format == 'raw':
            return self.sql

        else:
            return self.obfuscated

    def explain_plan(self, connect_params, cursor_params, execute_params):
        return _explain_plan(self.sql, self.dbapi, connect_params, cursor_params, execute_params)


def sql_statement(sql, dbapi):
    key = (sql, dbapi)
    result = _sql_statements.get(key, None)

    if result is not None:
        return result

    result = SQLStatement(sql, dbapi)
    _sql_statements[key] = result

    return result