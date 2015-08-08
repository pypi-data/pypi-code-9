# -*- encoding: utf-8 -*-
from datetime import datetime, date, time
from decimal import Decimal
import types
import six

from .config import KVStore

if six.PY3:
    def long(value):
        return value

MONGO_TEST_DATABASE = 'waterboy-test'

def clearstore(method):
    """Method decorator that clears the backend before returning."""
    def inner(self, *args, **kwargs):
        ret = method(self, *args, **kwargs)
        self.config.clear()
        return ret
    return inner

class ConfigTestType(type):
    """Per-method tearDown for test classes.

    Applies the clearstore decorator to any method starting with 'test_'.

    Use this rather than a tearDown method so that the base test class,
    ConfigTestCase, can stay compatible with both unittest and pytest.
    """

    def __new__(cls, name, bases, attrs):
        newattrs = {}
        for k, v in attrs.items():
            if k.startswith('test_') and isinstance(v, types.FunctionType):
                newattrs[k] = clearstore(v)
            else:
                newattrs[k] = v
        t = type.__new__(cls, name, bases, newattrs)
        return t

@six.add_metaclass(ConfigTestType)
class ConfigTestCase(object):

    BACKEND = None
    BACKEND_PARAMS = None
    DEFAULTS = {
        'INT_VALUE': 1,
        'LONG_VALUE': long(123456),
        'FLOAT_VALUE': 3.1415926536,
        'DECIMAL_VALUE': Decimal('0.1'),
        'BOOL_VALUE': True,
        'STRING_VALUE': 'Hello world',
        'UNICODE_VALUE': six.u('Rivière-Bonjour'),
        'DATETIME_VALUE': datetime(2010, 8, 23, 11, 29, 24),
        'DATE_VALUE': date(2010, 12, 24),
        'TIME_VALUE': time(23, 59, 59),
    }

    @property
    def config(self):
        """Create the config object with backend given by BACKEND"""
        try:
            cfg = self._cfg
        except AttributeError:
            if not self.BACKEND:
                raise Exception('BACKEND class attribute is not set.')
            cfg = self._cfg = KVStore(self.BACKEND, backend_params=self.BACKEND_PARAMS, initial=self.DEFAULTS)
        return cfg

    def test_get_invalid_key_fails(self):
        try:
            self.config.INVALID
        except Exception as e:
            assert type(e) == AttributeError

    def test_set_invalid_key_fails(self):
        try:
            self.config.INVALID = 'XYZ'
        except Exception as e:
            assert type(e) == AttributeError

    def test_get_valid_key_succeeds_and_returns_default_if_not_stored(self):
        assert self.config.backend.get('INT_VALUE') is None
        assert self.config.INT_VALUE == 1

    def test_set_valid_key_succeeds_and_updates_store(self):
        assert self.config.backend.get('INT_VALUE') is None
        self.config.INT_VALUE = 2
        assert self.config.backend.get('INT_VALUE') == 2

    def test_get_set_by_attribute(self):
        # get defaults
        assert self.config.INT_VALUE == 1
        assert self.config.LONG_VALUE == long(123456)
        assert self.config.BOOL_VALUE == True
        assert self.config.STRING_VALUE == 'Hello world'
        assert self.config.UNICODE_VALUE == six.u('Rivière-Bonjour')
        assert self.config.DECIMAL_VALUE == Decimal('0.1')
        assert self.config.DATETIME_VALUE == datetime(2010, 8, 23, 11, 29, 24)
        assert self.config.FLOAT_VALUE == 3.1415926536
        assert self.config.DATE_VALUE == date(2010, 12, 24)
        assert self.config.TIME_VALUE == time(23, 59, 59)

        # set new values
        self.config.INT_VALUE = 100
        self.config.LONG_VALUE = long(654321)
        self.config.BOOL_VALUE = False
        self.config.STRING_VALUE = 'Beware the weeping angel'
        self.config.UNICODE_VALUE = six.u('Québec')
        self.config.DECIMAL_VALUE = Decimal('1.2')
        self.config.DATETIME_VALUE = datetime(1977, 10, 2)
        self.config.FLOAT_VALUE = 2.718281845905
        self.config.DATE_VALUE = date(2001, 12, 20)
        self.config.TIME_VALUE = time(1, 59, 0)

        # get new values
        assert self.config.INT_VALUE == 100
        assert self.config.LONG_VALUE == long(654321)
        assert self.config.BOOL_VALUE == False
        assert self.config.STRING_VALUE == 'Beware the weeping angel'
        assert self.config.UNICODE_VALUE == six.u('Québec')
        assert self.config.DECIMAL_VALUE == Decimal('1.2')
        assert self.config.DATETIME_VALUE == datetime(1977, 10, 2)
        assert self.config.FLOAT_VALUE == 2.718281845905
        assert self.config.DATE_VALUE == date(2001, 12, 20)
        assert self.config.TIME_VALUE == time(1, 59, 0)

    def test_missing_values(self):
        # set some values and leave out others
        self.config.LONG_VALUE = long(654321)
        self.config.BOOL_VALUE = False
        self.config.UNICODE_VALUE = six.u('Québec')
        self.config.DECIMAL_VALUE = Decimal('1.2')
        self.config.DATETIME_VALUE = datetime(1977, 10, 2)
        self.config.DATE_VALUE = date(2001, 12, 20)
        self.config.TIME_VALUE = time(1, 59, 0)

        assert self.config.INT_VALUE == 1  # this should be the default value
        assert self.config.LONG_VALUE == long(654321)
        assert self.config.BOOL_VALUE == False
        assert self.config.STRING_VALUE == 'Hello world'  # this should be the default value
        assert self.config.UNICODE_VALUE == six.u('Québec')
        assert self.config.DECIMAL_VALUE == Decimal('1.2')
        assert self.config.DATETIME_VALUE == datetime(1977, 10, 2)
        assert self.config.FLOAT_VALUE == 3.1415926536  # this should be the default value
        assert self.config.DATE_VALUE == date(2001, 12, 20)
        assert self.config.TIME_VALUE == time(1, 59, 0)

