import os
from collections import namedtuple

from bidon.data import DataAccess, ModelAccess


DA_CORE = None
TEST_ROWCOUNT = False
TEST_CALLPROC = False
TEST_ROOT = os.path.dirname(os.path.abspath(__file__))


def configure(database="postgres"):
  if database == "postgres":
    configure_postgres(None)
  elif database == "mysql":
    configure_mysql(None)
  elif database == "sqlite":
    configure_sqlite(None)


def configure_postgres(args):
  from psycopg2.extras import Json
  from psycopg2.extensions import register_adapter

  from bidon.data.data_access_core import get_pg_core

  global DA_CORE, TEST_ROWCOUNT, TEST_CALLPROC

  DA_CORE = get_pg_core("dbname=bidon_test user=postgres host=localhost")
  TEST_ROWCOUNT = True
  TEST_CALLPROC = True

  register_adapter(dict, lambda d: Json(d))


def configure_mysql(args):
  from pymysql.cursors import Cursor

  from bidon.data.data_access_core import get_mysql_core

  global DA_CORE, TEST_ROWCOUNT, TEST_CALLPROC

  class NamedTupleCursorMixin(object):
    def _do_get_result(self):
      super(NamedTupleCursorMixin, self)._do_get_result()
      if self.description:
        fields = [f.name for f in self._result.fields]
        Row = namedtuple("Row", fields)
        self._rows = [Row(*row) for row in self._rows]

  class NamedTupleCursor(NamedTupleCursorMixin, Cursor):
    pass

  defaults_file = os.path.join(os.path.expanduser("~"), ".mysql-defaults/localhost")
  DA_CORE = get_mysql_core(
    dict(read_default_file=defaults_file, database="bidon_test"),
    cursor_factory=NamedTupleCursor)
  TEST_ROWCOUNT = True
  TEST_CALLPROC = False


def configure_sqlite(args):
  from bidon.data.data_access_core import get_sqlite_core

  global DA_CORE, TEST_ROWCOUNT, TEST_CALLPROC

  def get_namedtuple_factory():
    fields = []
    Row = None
    def namedtuple_factory(cursor, row):
      nonlocal fields, Row
      _fields = [col[0] for col in cursor.description]
      if _fields != fields:
        fields = _fields
        Row = namedtuple("Row", fields)
      return Row(*row)
    return namedtuple_factory

  DA_CORE = get_sqlite_core("tests/fixtures/test.sqlite3", cursor_factory=get_namedtuple_factory())
  TEST_ROWCOUNT = False
  TEST_CALLPROC = False


def get_data_access():
  return DataAccess(DA_CORE)


def get_model_access():
  return ModelAccess(DA_CORE)


from .data import *
from .util import *
from .spreadsheet import *
from .test_configuration import ConfigurationTestCase
from .test_data_table import DataTableTestCase
from .test_field_mapping import FieldMappingTestCase
from .test_json_patch import JsonPatchTestCase
from .test_xml import ElementPullerTestCase
