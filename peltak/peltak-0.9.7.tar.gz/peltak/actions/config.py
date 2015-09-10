# -*- coding: utf-8 -*-
from peltak.actions import actions
from peltak.core import cstr


def str2bool(s):
    return s.lower() in ['true', 't', 'yes', '1', 'on']


@actions.register(
    'config',
    desc=cstr('\n'.join([
        "Manage configuration for the current project.",
        "",
        "EXAMPLES",
        "",
        "Disable SSL verification:",
        "  ^1$ %(prog)s config set-bool verify_ssl false^0",
        "",
        "Set the project id:",
        "  ^1$ %(prog)s config set-int project_id 10^0",
        "",
        "Set gitlab url:",
        "  ^1$ %(prog)s config set gitlab_url https://my.gitlab.url^0",
    ])),
    cmdline=[{
        'args':     ('action',),
        'nargs':    '?',
        'default':  'list',
        'help': ("Action to take: list/get/set/set-int/set-bool")
    }, {
        'args':     ('name',),
        'nargs':    '?',
        'help': ("If action is get or set, this should be the config "
                 "variable name.")
    }, {
        'args':     ('value',),
        'nargs':    '?',
        'help': ("If action is 'set', this should be the config value")
    }]
)
def manage_config(app):
    #action = app.cl.action.lower()
    action = {
        'list':     config_list,
        'get':      config_get,
        'set':      config_set,
        'set-int':  lambda a: config_set(a, vtype=int),
        'set-bool': lambda a: config_set(a, vtype=str2bool),
    }.get(
        app.cl.action.lower(),
        lambda a: None
    )
    action(app)


def config_set(app, vtype=str):
    name  = app.cl.name
    value = vtype(app.cl.value)
    setattr(app.conf, name, value)
    config_get(app)


def config_get(app):
    print(cstr("  ^32{name}^0 = {value}").format(
        name  = app.cl.name,
        value = app.conf[app.cl.name],
    ))


def config_list(app):
    maxlen = max(len(name) for name in app.conf.keys())
    fmt    = "  ^32{{name:{}}}^0 = {{value}}".format(maxlen)
    for name, value in app.conf.items():
        print(cstr(fmt).format(name=name, value=value))

