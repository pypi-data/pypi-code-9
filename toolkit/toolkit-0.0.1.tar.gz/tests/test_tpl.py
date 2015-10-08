# coding=utf8

import os
from toolkit import tpl


def _test_register(mapped, register):
    register('test1', lambda function: None)

    @register
    def test2():
        pass

    @register('test3')
    def test3_function():
        pass

    assert len(mapped) == 3
    for k, v in mapped.iteritems():
        assert k == v.__name__
    mapped = {}


def test_register():
    test_map = {}

    def test_register(key, function):
        test_map[key] = function

    @tpl.proxy_register(test_register)
    def register():
        pass

    _test_register(test_map, register)


def test_register_filter():
    _test_register(tpl._default_filters, tpl.register_filter)


def test_register_test():
    _test_register(tpl._default_tests, tpl.register_test)


def test_render():
    path = os.path.join(os.getcwd(), 'tests/testfiles/template.tpl')
    assert 'Toolkit' in tpl.render(path, title='Toolkit')


def test_render_recursive():
    pass