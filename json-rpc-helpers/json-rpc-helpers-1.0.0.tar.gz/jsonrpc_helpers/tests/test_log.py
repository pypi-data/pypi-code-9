from logging import Logger
from collections import namedtuple

import pytest

from jsonrpc_helpers.log import (
    LoggedDecorator, EnchantedLoggerAdapter, response_to_len_mapper,
    build_instance_method_decorator)

LogRecord = namedtuple(
    'LogRecord', ['level', 'msg', 'args', 'exc_info', 'extra'])


class Context(object):
    def __init__(self):
        self.logger = None
        self.context = {}

    def setup_logger(self, f, logger, context, args, kwargs):
        context.update(self.context)
        self.logger = logger


class TestLogger(Logger):
    def __init__(self):
        self.logs = []
        self.level = 20  # INFO

    def _log(self, level, msg, args, exc_info=None, extra=None):
        self.logs.append(LogRecord(level, msg, args, exc_info, extra))


@pytest.fixture
def func():
    def func(arg1, arg2=None):
        return arg1, arg2
    return func


@pytest.fixture
def error_func():
    def error_func(arg1, arg2=None):
        raise Exception('WAAAGH!!')
    return error_func


@pytest.fixture
def method():
    class A(object):
        def method(self, arg1, arg2=None):
            return arg1, arg2
    return A().method


@pytest.fixture
def class_method():
    class A(object):
        @classmethod
        def method(cls, arg1, arg2=None):
            return arg1, arg2
    return A().method


@pytest.fixture
def decorator():
    logger = TestLogger()
    context = Context()
    decorator = LoggedDecorator(
        setup_logger=context.setup_logger, logger=logger)
    decorator.context = context
    return decorator


def _decorate_and_call(fn, dec):
    decorated = dec()(fn)
    return decorated('1', '2')


def _assert_call(decorator, result, func_name):
    assert len(decorator.logger.logs) == 3
    assert decorator.logger.logs[0].msg == 'Method {} called'.format(func_name)
    assert decorator.logger.logs[0].extra == {
        'tag': None, 'params': ['1', '2'],
        'method': func_name}
    assert decorator.logger.logs[1].msg == 'OK'
    assert decorator.logger.logs[1].extra == {
        'response': ('1', '2'), 'method': func_name, 'tag': None}
    assert decorator.logger.logs[2].msg == 'Execution time'
    assert result == ('1', '2')


def test_should_work_with_functions(func, decorator):
    result = _decorate_and_call(func, decorator)
    _assert_call(decorator, result, 'func')


def test_should_work_with_methods(method, decorator):
    result = _decorate_and_call(method, decorator)
    _assert_call(decorator, result, 'method')


def test_should_work_with_class_methods(class_method, decorator):
    result = _decorate_and_call(class_method, decorator)
    _assert_call(decorator, result, 'method')


def test_should_log_time(func, decorator):
    _decorate_and_call(func, decorator)
    assert 'time' in decorator.logger.logs[2].extra


def test_should_add_context_to_logs(func, decorator):
    decorated = decorator()(func)
    decorator.context.context['some_value'] = 42
    decorated('1', '2')
    assert decorator.logger.logs[0].extra['some_value'] == 42


def test_should_make_logger_available(func, decorator):
    _decorate_and_call(func, decorator)
    assert decorator.context.logger is not None
    assert isinstance(decorator.context.logger, EnchantedLoggerAdapter)


def test_should_log_exception(error_func, decorator):
    decorated = decorator()(error_func)
    with pytest.raises(Exception):
        decorated('1', '2')
    assert decorator.logger.logs[1].msg == 'Internal error!'
    assert decorator.logger.logs[2].msg == 'Execution time'


def test_should_log_kwargs(func, decorator):
    decorated = decorator()(func)
    result = decorated(arg1='a', arg2='b')
    assert result == ('a', 'b')


def test_should_add_tag_if_provided(func, decorator):
    decorated = decorator(tag='quirky')(func)
    decorated('1', '2')
    assert decorator.logger.logs[0].extra['tag'] == 'quirky'


def test_should_skip_args(func, decorator):
    decorated = decorator(args_to_skip=['arg1'])(func)
    decorated('1', '2')
    assert decorator.logger.logs[0].extra == {
        'tag': None, 'params': ['skipped', '2'],
        'method': 'func'}


def test_should_skip_kwargs(func, decorator):
    decorated = decorator(args_to_skip=['arg1'])(func)
    decorated(arg1='1', arg2='2')
    assert decorator.logger.logs[0].extra == {
        'tag': None, 'params': {'arg2': '2'},
        'method': 'func'}


def test_should_map_response(func, decorator):
    decorated = decorator(response_mapper=response_to_len_mapper)(func)
    result = decorated('1', '2')
    assert result == ('1', '2')
    assert decorator.logger.logs[1].extra == {
        'response': 'response length is 2', 'method': 'func', 'tag': None}


def test_should_use_func_name_if_specified(func, decorator):
    decorated = decorator(func_name='marvelous_handler')(func)
    result = decorated('1', '2')
    _assert_call(decorator, result, 'marvelous_handler')


def test_should_not_fail_if_no_args(decorator):
    def func(): pass
    decorated = decorator()(func)
    result = decorated()
    assert result is None
    assert decorator.logger.logs[0].extra == {
        'tag': None, 'params': {},
        'method': 'func'}
    assert decorator.logger.logs[1].extra == {
        'response': None, 'method': 'func', 'tag': None}


def test_should_work_for_instance_method_with_args():
    decorator = build_instance_method_decorator(logger=TestLogger())

    class Foo(object):
        @decorator()
        def handle(self, arg1):
            self.logger.info('Bar')
            return arg1

    foo = Foo()
    foo.handle('1')
    assert decorator.logger.logs[0].extra == {
        'tag': None, 'params': ['1'],
        'method': 'handle'}
    assert decorator.logger.logs[1].msg == 'Bar'


def test_should_work_for_instance_method_with_kwargs():
    decorator = build_instance_method_decorator(logger=TestLogger())

    class Foo(object):
        @decorator()
        def handle(self, arg1):
            self.logger.info('Bar')
            return arg1

    foo = Foo()
    foo.handle(arg1='1')
    assert decorator.logger.logs[0].extra == {
        'tag': None, 'params': {'arg1': '1'},
        'method': 'handle'}
    assert decorator.logger.logs[1].msg == 'Bar'
