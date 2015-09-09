"""Contains the DataAccess class, and functions for working with database transactions."""
import logging
from contextlib import contextmanager

from bidon.util import get_value


class DataAccess(object):
  """A thin wrapper over a DB API2 database connection.

  Provides a context manager, direct access to the execute method, and wrappers over some common
  methods to reduce the amount of boilerplate SQL required.
  """
  def __init__(self, core, *, logger=None):
    """Initialize a DataAccess object with a DataAccessCore"""
    self.core = core
    self.connection = None
    self.last_query = None
    self.row_count = -1
    self._logger = logger

  def __enter__(self):
    """Opens DataAccess and returns self as context manager."""
    return self.open()

  def __exit__(self, ex_type, ex_value, ex_traceback):
    """Closes DataAccess, requesting commit if no execption was thrown."""
    self.close(ex_type == None)

  def _log(self, message, loglevel=logging.INFO):
    """Logs message if logger is present."""
    if self._logger:
      self._logger.log(loglevel, message)

  @property
  def sql_writer(self):
    """The SQL writer object associated with the core."""
    return self.core.sql_writer

  def commit(self):
    """Commit the pending statements."""
    self._log("Commit", logging.DEBUG)
    self.connection.commit()

  def rollback(self):
    """Rollback the pending statements."""
    self._log("Rollback", logging.DEBUG)
    self.connection.rollback()

  @property
  def autocommit(self):
    """Get the autocommit value."""
    return self.core.get_autocommit(self.connection)

  @autocommit.setter
  def autocommit(self, value):
    """Set the autocommit value."""
    self._log("Setting autocommit from {} to {}".format(self.autocommit, value), logging.DEBUG)
    self.core.set_autocommit(self.connection, value)

  def open(self, autocommit=False):
    """Sets the connection via the core's open method."""
    if self.connection is not None:
      raise Exception("Connection already set")
    self.connection = self.core.open()
    self.autocommit = autocommit
    return self

  def close(self, commit=True):
    """Closes the connection via the core's close method."""
    self.core.close(self.connection, commit)
    self.connection = None
    return self

  def execute(self, query_string, params=None):
    """Execute a given query."""
    cr = self.connection.cursor()
    self._log("SQL: {0} ({1})".format(query_string, params))
    self.last_query = (query_string, params)
    cr.execute(query_string, params or self.core.empty_params)
    self._update_cursor_stats(cr)
    return cr

  def callproc(self, proc_name, params):
    """Call a stored procedure."""
    cr = self.connection.cursor()
    self._log(
      "SQL: {0}({1})".format(proc_name, ",".join([str(p) for p in params]) if params else ""))
    self.last_query = (proc_name, params)
    result_params = cr.callproc(proc_name, params)
    self._update_cursor_stats(cr)
    return (cr, result_params)

  def get_callproc_signature(self, proc_name, param_types):
    """Gets a procedure's signature from the name and list of types."""
    if isinstance(param_types[0], (list, tuple)):
      params = [self.core.sql_writer.to_placeholder(*pt) for pt in param_types]
    else:
      params = [self.core.sql_writer.to_placeholder(None, pt) for pt in param_types]

    return proc_name + self.core.sql_writer.to_tuple(params)

  def find(self, table_name, constraints=None, *, columns=None, order_by=None):
    """Find the first record that matches the given criteria.

    Constraints is any construct that canb e parsed by SQLWriter.parse_constraints.
    """
    query_string, params = self.core.sql_writer.get_find_all_query(
      table_name, constraints, columns=columns, order_by=order_by)
    query_string += " limit 1;"
    return self.execute(query_string, params).fetchone()

  def find_all(self, table_name, constraints=None, *, columns=None, order_by=None, limiting=None):
    """Find all records that match a given criteria.

    Constraints is any construct that canb e parsed by SQLWriter.parse_constraints.
    """
    query_string, params = self.core.sql_writer.get_find_all_query(
      table_name, constraints, columns=columns, order_by=order_by, limiting=limiting)
    query_string += ";"
    return self.execute(query_string, params)

  def page(self, table_name, paging, constraints=None, *, columns=None, order_by=None,
           get_count=True):
    """Performs a find_all method with paging. Returns results and the total number of records.

    Paging is a tuple containing (page, page_size). Page is 0-baesd."""
    if get_count:
      count = self.count(table_name, constraints)
    else:
      count = None

    page, page_size = paging

    limiting = None
    if page_size > 0:
      limiting = (page_size, page * page_size)

    records = list(self.find_all(
      table_name, constraints, columns=columns, order_by=order_by, limiting=limiting))
    return (records, count)

  def update(self, table_name, values, constraints=None, *, returning=None):
    """Builds and executes and update statement.

    Values can be either a dict or an enuerable of 2-tuples in the form (column, value). Constraints
    can be any construct that can be parsed by SQLWriter.parse_constraints. However, you cannot mix
    tuples and dicts between values and constraints.
    """
    if constraints is None:
      constraints = "1=1"
    assignments, assignment_params = self.core.sql_writer.parse_constraints(
      values, ", ", is_assignment=True)
    where, where_params = self.core.sql_writer.parse_constraints(constraints, " and ")
    returns = ""
    if returning and self.core.supports_returning_syntax:
      returns = " returning {0}".format(returning)
    sql = "update {0} set {1} where {2}{3};".format(table_name, assignments, where, returns)
    params = assignment_params

    if constraints is None or isinstance(constraints, str):
      pass
    elif isinstance(constraints, dict):
      if isinstance(params, list):
        raise ValueError("you cannot mix enumerable and dict values and constraints")
      params = params or {}
      params.update(where_params)
    else:
      if isinstance(params, dict):
        raise ValueError("you cannot mix enumerable and dict values and constraints")
      params = params or []
      params.extend(where_params)

    cr = self.execute(sql, params)
    return cr

  def insert(self, table_name, values, *, returning=None):
    """Builds and executes an insert statement.

    Values can be either a dict or an enumerable of 2-tuples in the form (column, value).
    """
    if isinstance(values, dict):
      names = values.keys()
      placeholders = [self.core.sql_writer.to_placeholder(i) for i in names]
      params = values
    else:
      names = [i[0] for i in values]
      placeholders = [self.core.sql_writer.to_placeholder() for i in values]
      params = [i[1] for i in values]
    placeholders = self.core.sql_writer.to_tuple(placeholders)
    names = self.core.sql_writer.to_tuple(names)
    returns = ""
    if returning and self.core.supports_returning_syntax:
      returns = " returning {0}".format(returning)
    sql = "insert into {0} {1} values {2}{3};".format(table_name, names, placeholders, returns)
    cr = self.execute(sql, params)
    return cr

  def delete(self, table_name, constraints=None):
    """Builds and executes an delete statement.

    Constraints can be any construct that can be parsed by SQLWriter.parse_constraints.
    """
    if constraints is None:
      constraints = "1=1"
    where, params = self.core.sql_writer.parse_constraints(constraints)
    sql = "delete from {0} where {1};".format(table_name, where)
    self.execute(sql, params)

  def count(self, table_name, constraints=None, *, extract="index"):
    """Get the count of records in a table.

    If the default cursor is a tuple or named tuple, this method will work without specifying an
    extract parameter. If it is a dict cursor, it is necessary to specify any value other than
    'index' for extract. This method will not work with cursors that aren't like tuple, namedtuple
    or dict cursors.
    """
    where, params = self.core.sql_writer.parse_constraints(constraints)
    sql = "select count(*) as count from {0} where {1};".format(table_name, where or "1 = 1")
    # NOTE: Won't work right with dict cursor
    return self.get_scalar(self.execute(sql, params), 0 if extract == "index" else "count")

  def get_scalar(self, cursor, index=0):
    """Get a single value from the first returned record from a cursor.

    By default it will get cursor.fecthone()[0] which works with tuples and namedtuples. For dict
    cursor it is necessary to specify index. This method will not work with cursors that aren't
    indexable.
    """
    if isinstance(index, int):
      return cursor.fetchone()[index]
    else:
      return get_value(cursor.fetchone(), index)

  def _update_cursor_stats(self, cursor):
    """Sets DataAccess members according to the given cursor."""
    self.row_count = cursor.rowcount


@contextmanager
def transaction(dax):
  """Wrap statements in a transaction. If the statements succeed, commit, otherwise rollback."""
  old_autocommit = dax.autocommit
  dax.autocommit = False
  try:
    yield dax
  except Exception as ex:
    dax.rollback()
    raise ex
  else:
    dax.commit()
  finally:
    dax.autocommit = old_autocommit


@contextmanager
def autocommit(dax):
  """Make statements autocommit."""
  if not dax.autocommit:
    dax.commit()
  old_autocommit = dax.autocommit
  dax.autocommit = True
  try:
    yield dax
  finally:
    dax.autocommit = old_autocommit
