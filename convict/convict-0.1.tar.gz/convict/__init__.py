# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json

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


class Convict(dict):
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
                # enforce json typing and close values
                json_str = json.dumps(value['default'])
                parent[key] = json.loads(json_str)
                default[key] = json.loads(json_str)
            else:
                parent[key] = {}
                default[key] = {}
                self.__load_schema(value, parent[key], default[key])

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
        orig = self
        if not isinstance(keys, dict):
            raise TypeError(
                'convict config must be of type dict, not %s'
                % type(obj)
            )
        self.__load(orig, obj)

    def loadFile(self, *files):
        for path in files:
            with open(path) as pointer:
                json_str = pointer.read()
            self.load(json.loads(json_str))

    def getProperties(self):
        return dict(self)

    def __str__(self):
        return json.dumps(self)

    def toString(self):
        return str(self)

    def getSchema(self):
        return dict(self.__schema)

    def getSchemaString(self):
        return json.dumps(_json_copy(self.__schema))
