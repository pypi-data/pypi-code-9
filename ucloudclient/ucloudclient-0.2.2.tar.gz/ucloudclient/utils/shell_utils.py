import json
import os
import textwrap
import time

import six
import prettytable


def add_arg(func, *args, **kwargs):
    """Bind CLI arguments to a shell.py `do_foo` function."""

    if not hasattr(func, 'arguments'):
        func.arguments = []

    if (args, kwargs) not in func.arguments:
        func.arguments.insert(0, (args, kwargs))


def arg(*args, **kwargs):
    """Decorator for CLI args.

    Example:

    >>> @arg("name", help="Name of the new entity")
    ... def entity_create(args):
    ...     pass
    """

    def _decorator(func):
        add_arg(func, *args, **kwargs)
        return func

    return _decorator


def multi_arg(*args, **kwargs):
    """Decorator for multiple CLI args.

    Example:

    >>> @arg("name", help="Name of the new entity")
    ... def entity_create(args):
    ...     pass
    """

    def _decorator(func):
        add_arg(func, *args, **kwargs)
        return func

    return _decorator


def print_original_dict(d):
    d = json.dumps(d, encoding='UTF-8', ensure_ascii=False, indent=2)
    print(d)


def print_dict(d, dict_property="Property", dict_value="Value", wrap=0):
    pt = prettytable.PrettyTable([dict_property, dict_value], caching=False)
    pt.align = 'l'
    for k, v in sorted(d.items()):
        # convert dict to str to check length
        if isinstance(v, (dict, list)):
            # v = jsonutils.dumps(v)
            v = json.dumps(v)
        if wrap > 0:
            v = textwrap.fill(str(v), wrap)
        # if value has a newline, add in multiple rows
        # e.g. fault with stacktrace
        if v and isinstance(v, six.string_types) and r'\n' in v:
            lines = v.strip().split(r'\n')
            col1 = k
            for line in lines:
                pt.add_row([col1, line])
                col1 = ''
        else:
            if v is None:
                v = '-'
            pt.add_row([k, v])

    # result = encodeutils.safe_encode(pt.get_string())
    result = pt.get_string()

    if six.PY3:
        result = result.decode()

    print(result)


def print_list(objs, fields, formatters={}, sortby_index=None):
    '''
    give the fields of objs to be printed.
    :param objs:
    :param fields: the fields to be printed
    :param formatters:
    :param sortby_index:
    :return:
    '''
    if sortby_index is None:
        sortby = None
    else:
        sortby = fields[sortby_index]
    mixed_case_fields = ['serverId']
    pt = prettytable.PrettyTable([f for f in fields], caching=False)
    pt.align = 'l'

    for o in objs:
        row = []
        for field in fields:
            if field in formatters:
                row.append(formatters[field](o))
            else:
                if field in mixed_case_fields:
                    field_name = field.replace(' ', '_')
                # else:
                # field_name = field.lower().replace(' ', '_')
                field_name = field
                data = o.get(field_name, '')
                if data is None:
                    data = '-'
                row.append(data)
        pt.add_row(row)

    if sortby is not None:
        result = pt.get_string(sortby=sortby)
    else:
        result = pt.get_string()

    if six.PY3:
        result = result.decode()

    print(result)


def env(*args, **kwargs):
    """Returns environment variable set."""

    for arg in args:
        value = os.environ.get(arg)
        if value:
            return value
    return kwargs.get('default', '')


def parse_time(d):
    for (k, v) in d.items():
        if 'Time' in k and isinstance(v, int) and v > 1000000000:
            d[k] = time.strftime('%F %T', time.localtime(v))
