# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json
import os


def _json_copy(obj):
    if isinstance(obj, dict):
        copy = obj.copy()
        for key, value in copy.iteritems():
            copy[key] = _json_copy(value)
        return copy
    elif isinstance(obj, list):
        copy = obj[:]
        for index in range(len(copy)):
            copy[index] = _json_copy(copy[index])
        return copy
    elif isinstance(
        obj,
        (bool, int, float, long, str, unicode, type(None))
    ):
        return obj
    elif isinstance(obj, type):
        # this is so schema json exports to the right thing
        return obj.__name__
    else:
        return str(obj)


# validation
def _validate_noop(obj): return True
## python types
def _validate_bool(obj): return isinstance(obj, bool)
def _validate_dict(obj): return isinstance(obj, dict)
def _validate_float(obj): return isinstance(obj, float)
def _validate_int(obj): return isinstance(obj, int)
def _validate_list(obj): return isinstance(obj, list)
def _validate_long(obj): return isinstance(obj, long)
def _validate_none(obj): return isinstance(obj, type(None))
def _validate_str(obj): return isinstance(obj, str)
def _validate_unicode(obj): return isinstance(obj, unicode)


## json types
def _validate_number(obj): return isinstance(obj, (int, long, float))
def _validate_string(obj): return isinstance(obj, (str, unicode))


## convict types
def _validate_ipaddress(obj):
    octets = obj.split('.')
    if len(octets) != 4:
        return False
    for o in octets:
        if not 0 <= int(o) <= 255:
            return False
    return True


def _validate_port(obj):
    _validate_number(obj)
    return 0 <= obj <= 65535


# coercion
def _coerce_noop(obj): return obj
## python types
def _coerce_float(obj): return float(obj)
def _coerce_int(obj): return int(obj)
def _coerce_long(obj): return long(obj)
def _coerce_str(obj): return str(obj)
def _coerce_unicode(obj): return unicode(obj)


## manually coerced python types
def _coerce_bool(obj):
    if obj in ['True', 'true']:
        return True
    elif obj in ['False', 'false']:
        return False
    else:
        raise ValueError('could not coerce to bool: %s' % obj)


def _coerce_none(obj):
    if obj in ['None', 'none', 'null', '']:
        return None
    else:
        raise ValueError('could not coerce to None: %s' % obj)


## json types (includes list and dict for coercion)
def _coerce_json(obj): return json.loads(obj)


class Convict(dict):
    types = {
        # python types
        (bool, 'bool'): {
            'validate': _validate_bool,
            'coerce': _coerce_bool,
        },
        (dict, 'dict'): {
            'validate': _validate_dict,
            'coerce': _coerce_json,
        },
        (float, 'float'): {
            'validate': _validate_float,
            'coerce': _coerce_float,
        },
        (int, 'int'): {
            'validate': _validate_int,
            'coerce': _coerce_int,
        },
        (list, 'list'): {
            'validate': _validate_list,
            'coerce': _coerce_json,
        },
        (long, 'long'): {
            'validate': _validate_long,
            'coerce': _coerce_long,
        },
        (None, 'None', 'none', 'null'): {
            'validate': _validate_none,
            'coerce': _coerce_none,
        },
        (str, 'str'): {
            'validate': _validate_str,
            'coerce': _coerce_str,
        },
        (unicode, 'unicode'): {
            'validate': _validate_unicode,
            'coerce': _coerce_unicode,
        },
        # json types
        ('String', 'string'): {
            'validate': _validate_string,
            'coerce': _coerce_noop,
        },
        ('Number', 'number'): {
            'validate': _validate_number,
            'coerce': _coerce_json,
        },
        # convict types
        ('*',): {
            'validate': _validate_noop,
            'coerce': _coerce_noop,
        },
        ('port',): {
            'validate': _validate_port,
            'coerce': _coerce_json,
        },
        ('ipaddress',): {
            'validate': _validate_ipaddress,
            'coerce': _coerce_noop,
        },
    }

    def __init__(self, schema, *args, **kwargs):
        if not isinstance(schema, dict):
            raise TypeError(
                'convict schema must be of type dict, not %s'
                % type(schema)
            )

        self.__schema = schema
        self.__default = {}

        self.__load_schema(schema, self, self.__default)

        super(Convict, self).__init__(*args, **kwargs)

    def __load_schema(self, schema, parent, default):
        for key, value in schema.iteritems():
            if not isinstance(key, (str,unicode)):
                raise TypeError(
                    'convict properties must have keys of type str, not %s'
                    % type(key)
                )

            if not isinstance(value, dict):
                raise TypeError(
                    'convict properties must be described by a dict, not %s'
                    % type(value)
                )

            if 'default' in value:
                if 'format' not in value:
                    raise ValueError('setting missing format: %s' % key)
                # enforce json typing and close values
                json_str = json.dumps(value['default'])
                # load env var
                if 'env' in value:
                    parent[key] = self.__coerce_env(
                        value['env'],
                        value['format'],
                        json.loads(json_str)
                    )
                else:
                    parent[key] = json.loads(json_str)
                default[key] = json.loads(json_str)
            else:
                parent[key] = {}
                default[key] = {}
                self.__load_schema(value, parent[key], default[key])

    def __coerce_env(self, env, form, default):
        if env not in os.environ:
            return default
        elif isinstance(form, (type(lambda x:x), list)):
            return os.environ[env]
        else:
            for key in self.types.keys():
                if form in key:
                    return self.types[key]['coerce'](os.environ[env])
        raise TypeError('could not coerce env var with format: %s' % form)

    def set(self, keys, value):
        if not isinstance(keys, (str,unicode)):
            raise KeyError(keys)

        keys = keys.split('.')
        last = keys.pop()
        prop = self

        for key in keys:
            if isinstance(prop, list):
                prop = prop[int(key)]
            elif isinstance(prop, dict):
                if key not in prop:
                    prop[key] = {}

                prop = prop[key]
            else:
                raise KeyError(keys)

        prop[last] = value

    def get(self, keys):
        if not isinstance(keys, (str,unicode)):
            raise KeyError(keys)

        value = self
        for key in keys.split('.'):
            if isinstance(value, list):
                value = value[int(key)]
            elif isinstance(value, dict):
                value = value[key]
            else:
                raise KeyError(keys)

        return value

    def default(self, keys):
        if not isinstance(keys, (str,unicode)):
            raise KeyError(keys)

        value = self.__default
        for key in keys.split('.'):
            if isinstance(value, list):
                value = value[int(key)]
            elif isinstance(value, dict):
                value = value[key]
            else:
                raise KeyError(keys)

        return value

    def has(self, keys):
        try:
            self.get(keys)
            return true
        except Exception:
            return false


    def __load(self, orig, obj):
        for key, value in obj.iteritems():
            if not isinstance(key, (str,unicode)):
                raise TypeError(
                    'convict properties must have keys of type str, not %s'
                    % type(key)
                )

            if isinstance(value, dict) and isinstance(orig[key], dict):
                self.__load(orig[key], value)
            else:
                # enforce json typing and close value
                orig[key] = json.loads(json.dumps(value))


    def load(self, obj):
        if not isinstance(obj, dict):
            raise TypeError(
                'convict config must be of type dict, not %s'
                % type(obj)
            )
        self.__load(self, obj)

    def loadFile(self, *files):
        for paths in files:
            if isinstance(paths, list):
                for path in paths:
                    with open(path) as pointer:
                        json_str = pointer.read()
                    self.load(json.loads(json_str))
            else:
                path = paths
                with open(path) as pointer:
                    json_str = pointer.read()
                self.load(json.loads(json_str))

    def getProperties(self):
        return dict(self)

    def __str__(self):
        return json.dumps(_json_copy(self))

    def toString(self):
        return str(self)

    def getSchema(self):
        return dict(self.__schema)

    def getSchemaString(self):
        return json.dumps(_json_copy(self.__schema))

    def __validate_value(self, value, form):
        if isinstance(form, list):
            return value in form
        elif isinstance(form, type(lambda x:x)):
            return form(value)
        else:
            for key in self.types.keys():
                if form in key:
                    return self.types[key]['validate'](value)
        raise TypeError('could not validate with format: %s' % form)

    def __validate(self, schema, parent):
        exceptions = []
        for key, value in schema.iteritems():
            try:
                if 'default' in value:
                    if not self.__validate_value(parent[key], value['format']):
                        raise ValueError('invalid setting value: %s' % parent[key])
                else:
                    exceptions += self.__validate(value, parent[key])
            except Exception as e:
                exceptions.append(e)
        return exceptions

    def validate(self):
        exceptions = self.__validate(self.__schema, self)
        if not exceptions:
            return True

        message = 'convict validation failed:\n'
        for e in exceptions:
            message += ('\n%s' % e)

        raise Exception(message)
