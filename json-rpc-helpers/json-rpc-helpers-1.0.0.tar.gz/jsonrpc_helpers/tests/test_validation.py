import pytest
from jsonschema import SchemaError, ValidationError
from jsonrpc_helpers.validation import validated, CallError

SCHEMA = {
    'properties': {
        'arg1': {'type': 'string'},
        'arg2': {'type': 'integer'}
    },
    'required': ['arg1']
}


@pytest.fixture()
def without_args():
    return lambda: True


@pytest.fixture()
def with_args():
    return lambda arg1, arg2: (arg1, arg2)


@pytest.fixture()
def with_kwargs():
    return lambda arg1='val1', arg2=10: (arg1, arg2)


def test_should_fail_if_schema_invalid(with_args):
    with pytest.raises(SchemaError):
        validated({'properties': {'arg1': {'type': 'int'}}})(with_args)


def test_should_fail_if_no_schema(with_args):
    with pytest.raises(AttributeError):
        validated(None)(with_args)


def test_should_validate_if_args_ok(with_args):
    function = validated(SCHEMA)(with_args)
    assert function('a', 1)


def test_should_fail_if_args_not_ok(with_args):
    function = validated(SCHEMA)(with_args)
    with pytest.raises(ValidationError):
        function(1, 'a')


def test_should_skip_args(with_args):
    function = validated(SCHEMA, args_to_skip=['arg2'])(with_args)
    assert function('foo', 'bar') == ('foo', 'bar')


def test_should_validate_if_kwargs_ok(with_kwargs):
    function = validated(SCHEMA)(with_kwargs)
    assert function(arg2=10, arg1='a')


def test_should_fail_if_kwargs_not_ok(with_kwargs):
    function = validated(SCHEMA)(with_kwargs)
    with pytest.raises(ValidationError):
        function(arg2='10', arg1=10)


def test_should_skip_kwargs(with_kwargs):
    function = validated(SCHEMA, args_to_skip=['arg2'])(with_kwargs)
    assert function(arg1='foo', arg2='bar') == ('foo', 'bar')


def test_should_add_defaults_to_args_before_validation(with_kwargs):
    function = validated(SCHEMA)(with_kwargs)
    assert function('a')


def test_should_add_defaults_to_kwargs_before_validation(with_kwargs):
    function = validated(SCHEMA)(with_kwargs)
    assert function()


def test_should_fail_if_both_args_and_kwargs_provided(with_kwargs):
    function = validated(SCHEMA)(with_kwargs)
    with pytest.raises(CallError):
        function('foo', arg2=10)


def test_should_add_schema_if_decorated(with_args):
    function = validated(SCHEMA)(with_args)
    assert getattr(function, 'schema') is not None


def test_should_not_mutate_arguments(with_kwargs):
    function = validated(SCHEMA)(with_kwargs)
    assert function('foo', 42) == ('foo', 42)
