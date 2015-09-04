from __future__ import print_function

import os
import sys
import yaml

# We are running in production if MORPH_URL is set in the environment.
in_production = bool(os.getenv('MORPH_URL'))
is_admin = "admin" in os.getenv('USER_ROLES', '').split(",")

def data_dir():
    return _path_to("data")

def sources_dir():
    if (in_production and not is_admin):
        raise RuntimeError("Only admins are permitted to write to `sources_dir`")
    else:
        return _path_to("sources")

def _vars_path():
    return data_dir() + '/_vars.yml'

def log(message):
    print(message, file=sys.stderr)


def save_var(key, val):
    vars = _get_vars()
    vars[key] = val
    _save_vars(vars)


def get_var(key):
    try:
        return _get_vars()[key]
    except KeyError:
        raise KeyError('No such var: ' + key)

def _path_to(directory):
    if in_production:
        directory = '/%s' % directory
    else:
        _set_up_dir(directory)
    return directory


def _save_vars(vars):
    with open(_vars_path(), 'w') as f:
        f.write(yaml.dump(vars))


def _get_vars():
    try:
        with open(_vars_path()) as f:
            return yaml.load(f)
    except IOError:
        return {}

def _set_up_dir(d):
    try:
        os.mkdir(d)
    except OSError:
        pass

os.environ["SCRAPERWIKI_DATABASE_NAME"] = "sqlite:///%s/data.sqlite" % data_dir()
