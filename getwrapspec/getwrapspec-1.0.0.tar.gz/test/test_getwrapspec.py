# -*- coding: utf-8 -*-

import getwrapspec


class G:
    _side_effects = []
    _log_entries = []
    _third = []


def side_effect_decorator(func):
    @getwrapspec.wraps(func)
    def wrapper(*args, **kwargs):
        argspec = getwrapspec.getargspec(func)
        G._side_effects.append({'args': args, 'kwargs': kwargs})
        return func(*args, **kwargs)
    return wrapper


def logging_decorator(func):
    @getwrapspec.wraps(func)
    def wrapper(*args, **kwargs):
        argspec = getwrapspec.getargspec(func)
        G._log_entries.append({'args': args, 'kwargs': kwargs})
        return func(*args, **kwargs)
    return wrapper


def third_decorator(func):
    @getwrapspec.wraps(func)
    def wrapper(*args, **kwargs):
        argspec = getwrapspec.getargspec(func)
        G._third.append({'args': args, 'kwargs': kwargs})
        return func(*args, **kwargs)
    return wrapper

@logging_decorator
@side_effect_decorator
def foo(a, b, c=None):
    return {'a': a, 'b': b, 'c': c}


def test_ordering_a():
    G._side_effects = []
    G._log_entries = []
    assert foo(1, 2) == {'a': 1, 'b': 2, 'c': None}
    assert len(G._side_effects) == 1
    assert len(G._log_entries) == 1
    assert foo(1, 2, 3) == {'a': 1, 'b': 2, 'c': 3}
    assert len(G._side_effects) == 2
    assert len(G._log_entries) == 2


@side_effect_decorator
@logging_decorator
def bar(a, b, c=None):
    return {'a': a, 'b': b, 'c': c}


def test_ordering_b():
    G._side_effects = []
    G._log_entries = []
    assert bar(1, 2) == {'a': 1, 'b': 2, 'c': None}
    assert len(G._side_effects) == 1
    assert len(G._log_entries) == 1
    assert bar(1, 2, 3) == {'a': 1, 'b': 2, 'c': 3}
    assert len(G._side_effects) == 2
    assert len(G._log_entries) == 2


@third_decorator
@side_effect_decorator
@logging_decorator
def baz(a, b, c=None):
    return {'a': a, 'b': b, 'c': c}


def test_three_decorators():
    G._side_effects = []
    G._log_entries = []
    G._third = []
    assert baz(1, 2) == {'a': 1, 'b': 2, 'c': None}
    assert len(G._side_effects) == 1
    assert len(G._log_entries) == 1
    assert len(G._third) == 1
    assert baz(1, 2, 3) == {'a': 1, 'b': 2, 'c': 3}
    assert len(G._side_effects) == 2
    assert len(G._log_entries) == 2
    assert len(G._third) == 2
