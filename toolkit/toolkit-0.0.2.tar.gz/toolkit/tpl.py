# coding=utf8

"""
The :mod:`tpl` module has some helper function implements
base on :mod:`jinja2` for human.
"""

import os
import jinja2
import inspect
import functools

from toolkit import ToolkitException


class TplException(ToolkitException):
    pass


class RegisterError(TplException):
    pass


class RenderError(TplException):
    pass


class AbsLoader(jinja2.loaders.BaseLoader):
    def __init__(self):
        pass

    def get_source(self, environment, template):
        path = template
        if not os.path.exists(path):
            raise jinja2.exceptions.TemplateNotFound(template)
        mtime = os.path.getmtime(path)
        with file(path) as f:
            source = f.read().decode('utf-8')
        return source, path, lambda: mtime == os.path.getmtime(path)

env = jinja2.Environment(loader=AbsLoader())


def proxy_register(register_function):
    """
    Proxy a function to a register function.

    :param register_funtion: a function need to proxy.
    :return: a proxy wrapper
    """
    def wrapper(function):
        @functools.wraps(function)
        def register(excepted, filter_function=None):
            if inspect.isfunction(excepted):
                register_function(excepted.__name__, excepted)
            elif isinstance(excepted, str) and filter_function:
                if not inspect.isfunction(filter_function):
                    raise RegisterError('Registered must be a function.')
                filter_function.__name__ = excepted
                register_function(excepted, filter_function)
            elif isinstance(excepted, str):
                def register_wrapper(func):
                    if not inspect.isfunction(func):
                        raise RegisterError('Registered must be a function.')
                    func.__name__ = excepted
                    register_function(excepted, func)
                return register_wrapper
        return register
    return wrapper


def _register_filter(name, filter_function):
    global env
    env.filters[name] = filter_function


@proxy_register(_register_filter)
def register_filter():
    """
    Add default filter function to template rendered environment.
    Register provide 3-way to add a function to environment
    and use on template.

    .. code-block:: python

        register_filter('lower', str.lower)

        @register_filter
        def lower(s):
            return s.lower()

        @register_filter('lower')
        def xxx_lower():
            return s.lower()
    """
    pass


def _register_test(name, test_function):
    global env
    env.tests[name] = test_function


@proxy_register(_register_test)
def register_test():
    """
    Add default test function to template rendered environment.
    Register provide 3-way to add a function to environment
    and use on template.

    .. code-block:: python

        register_test('digital', lambda v: type(v) in (int, float))

        @register_test
        def digital(v):
            return type(v) in (int, float)

        @register_test('digital')
        def test_if_it_is_digital():
            return type(v) in (int, float)
    """
    pass


def _register_func(name, global_function):
    global env
    env.globals[name] = global_function


@proxy_register(_register_func)
def register_func():
    """
    Add default global function to template rendered environment.
    Register provide 3-way to add a function to environment
    and use on template.

    .. code-block:: python

        register_func('add', lambda a, b: a + b)

        @register_func
        def add(a, b):
            return a + b

        @register_func('add')
        def add(a, b):
            return a + b
    """
    pass


def create_env_by_folder(folder):
    """
    Create :mod:`jinja2` environment with :meth:`jinja2.FileSystemLoader`

    :param folder: folder path.
    :return: jinja2 environment object.
    """
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(folder))

    return env


def get_template(template_path):
    """
    Get template object from absolute path.

    For example, the template has:

    .. code-block:: html

        {% macro add(a, b) -%}
            {{a + b}}
        {%- endmacro %}

    And call the macro as template object method.

    .. code-block:: python

        tpl = get_template('template.tpl')
        print(tpl.add(1, 2))

        >>> 3

    :param template_path: template absolute path.
    :return: template object
    """
    global env
    return env.get_template(template_path)


def render(template_path, output_file=None, **kwargs):
    """
    Render jinja2 template file use absolute path.

    **Usage**

    A simple template as follow:

    .. code-block:: jinja

        This is a test template

        {{ title }}

    Then write render code by single line.

    .. code-block:: python

        render('template.tpl', name='toolkit')

    :param template_path: absolute file path of template file.
    :param output_file: the path of output file.
    :param kwargs: keyword arguments for template.
    """
    template = get_template(template_path)
    rendered = template.render(**kwargs)
    if not output_file:
        return rendered
    with open(output_file) as f:
        f.write(rendered)


def render_recursive(folder, **kwargs):
    if not os.path.isdir(folder):
        err_msg = 'render_recursive() excepted a folder, ' \
                  'but {} is not a folder.'
        raise RenderError(err_msg.format(folder))
