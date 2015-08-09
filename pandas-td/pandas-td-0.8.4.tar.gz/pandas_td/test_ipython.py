import pandas_td.ipython
import pandas_td.td
from pandas_td.ipython import DatabasesMagics
from pandas_td.ipython import TablesMagics
from pandas_td.ipython import JobsMagics
from pandas_td.ipython import UseMagics
from pandas_td.ipython import QueryMagics
from pandas_td.ipython import load_ipython_extension

from unittest import TestCase
try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock
from nose.tools import ok_, eq_, raises

class MockIPython(object):
    push = MagicMock()
    ev = MagicMock()
    user_ns = {}
    register_magics = MagicMock()

class MockContext(object):
    def connect(self):
        return MagicMock()

# test cases

class MagicDatabasesTestCase(TestCase):
    def setUp(self):
        pandas_td.ipython.get_ipython = MockIPython

    def TearDown(self):
        del pandas_td.ipython.get_ipython

    def test_ok(self):
        ipython = MockIPython()
        DatabasesMagics(ipython).td_databases('')

class MagicTablesTestCase(TestCase):
    def setUp(self):
        pandas_td.ipython.get_ipython = MockIPython

    def TearDown(self):
        del pandas_td.ipython.get_ipython

    def test_ok(self):
        ipython = MockIPython()
        TablesMagics(ipython).td_tables('sample_datasets')

class MagicJobsTestCase(TestCase):
    def setUp(self):
        pandas_td.ipython.get_ipython = MockIPython

    def TearDown(self):
        del pandas_td.ipython.get_ipython

    def test_ok(self):
        ipython = MockIPython()
        JobsMagics(ipython).td_jobs('')

class MagicUseTestCase(TestCase):
    def setUp(self):
        pandas_td.ipython.get_ipython = MockIPython

    def TearDown(self):
        del pandas_td.ipython.get_ipython

    def test_ok(self):
        ipython = MockIPython()
        UseMagics(ipython).td_use('sample_datasets')

class MagicQueryTestCase(TestCase):
    def setUp(self):
        pandas_td.ipython.get_ipython = MockIPython

    def TearDown(self):
        del pandas_td.ipython.get_ipython

    def test_ok(self):
        ipython = MockIPython()
        pandas_td.ipython.td.read_td_query = MagicMock()
        QueryMagics(ipython).td_presto('', 'select 1')

class LoadIPythonExtensionTestCase(TestCase):
    def test_load_ext(self):
        ipython = MockIPython()
        load_ipython_extension(ipython)
        ipython.push.assert_called_with('get_td_magic_context')
