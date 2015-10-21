# -*- coding: utf-8 -*-

# TODO: datetime support

###
### DO NOT CHANGE THIS FILE
### 
### The code is auto generated, your change will be overwritten by 
### code generating.
###


DefinitionsUpstream = {'properties': {'name': {'type': 'string'}, 'servers': {'items': {'type': 'string'}, 'type': 'array'}}}
DefinitionsCertificate = {'required': ['private_key', 'certificate_chain'], 'properties': {'private_key': {'type': 'string'}, 'cipher': {'type': 'string'}, 'certificate_chain': {'type': 'string'}}}
DefinitionsFrontend = {'required': ['protocol'], 'properties': {'protocol': {'default': 'http', 'enum': ['http', 'https', 'tcp', 'ssl'], 'type': 'string', 'description': 'not support udp'}, 'port': {'type': 'integer', 'description': 'intranet port. readonly. decided by GLB'}}}
DefinitionsSlave = {'required': ['address'], 'properties': {'haproxy_version': {'type': 'string'}, 'nginx_version': {'type': 'string'}, 'address': {'type': 'string'}}}
DefinitionsBackend = {'properties': {'tag': {'type': 'string'}, 'port': {'type': 'integer'}, 'address': {'type': 'string', 'format': 'ipv4'}}}
DefinitionsEntrypoint = {'required': ['domain', 'port'], 'properties': {'domain': {'type': 'string', 'format': 'hostname'}, 'protocol': {'default': 'http', 'enum': ['http', 'https', 'tcp', 'ssl'], 'type': 'string', 'description': 'not support udp'}, 'port': {'type': 'integer'}, 'certificate': DefinitionsCertificate}}
DefinitionsServer = {'required': ['port', 'server_names', 'protocol'], 'properties': {'server_names': {'items': {'type': 'string'}, 'type': 'array'}, 'protocol': {'default': 'http', 'enum': ['http', 'ssl'], 'type': 'string'}, 'port': {'default': 80, 'type': 'integer'}, 'certificate': DefinitionsCertificate}}
DefinitionsBalancer = {'required': ['name'], 'properties': {'entrypoints': {'items': DefinitionsEntrypoint, 'type': 'array'}, 'backends': {'items': DefinitionsBackend, 'type': 'array'}, 'frontend': DefinitionsFrontend, 'name': {'type': 'string'}}}
DefinitionsNginx = {'required': ['name'], 'properties': {'upstream': DefinitionsUpstream, 'name': {'type': 'string'}, 'server': DefinitionsServer}}

validators = {
    ('balancer_balancer_name_frontend', 'PUT'): {'json': DefinitionsFrontend},
    ('balancer_balancer_name_backends', 'PUT'): {'json': {'items': DefinitionsBackend, 'type': 'array'}},
    ('balancer_balancer_name_backends', 'POST'): {'json': {'items': DefinitionsBackend, 'type': 'array'}},
    ('balancer_balancer_name_backends', 'GET'): {'args': {'required': [], 'properties': {'tag': {'type': 'string'}}}},
    ('balancer_balancer_name_backends', 'DELETE'): {'args': {'required': [], 'properties': {'tag': {'type': 'string', 'description': 'delete number'}, 'port': {'type': 'integer'}, 'address': {'type': 'string'}}}},
    ('balancer_balancer_name_entrypoints', 'PUT'): {'json': {'items': DefinitionsEntrypoint, 'type': 'array'}},
    ('balancer_balancer_name_entrypoints', 'POST'): {'json': {'items': DefinitionsEntrypoint, 'type': 'array'}},
    ('balancer_balancer_name_entrypoints', 'DELETE'): {'args': {'required': [], 'properties': {'domain': {'type': 'string'}, 'del_type': {'enum': ['default', 'all'], 'type': 'string'}, 'port': {'type': 'integer'}}}},
    ('nginx', 'POST'): {'json': DefinitionsNginx},
    ('nginx', 'GET'): {'args': {'required': [], 'properties': {'limit': {'description': 'max records to return', 'format': 'int32', 'default': 20, 'maximum': 1000, 'minimum': 1, 'type': 'integer'}, 'offset': {'description': 'number of items to skip', 'format': 'int32', 'default': 0, 'maximum': 10000, 'minimum': 0, 'type': 'integer'}}}},
    ('nginx_name_upstream', 'PUT'): {'json': DefinitionsUpstream},
    ('balancer', 'POST'): {'json': DefinitionsBalancer},
    ('balancer', 'GET'): {'args': {'required': [], 'properties': {'limit': {'description': 'max records to return', 'format': 'int32', 'default': 20, 'maximum': 1000, 'minimum': 1, 'type': 'integer'}, 'offset': {'description': 'number of items to skip', 'format': 'int32', 'default': 0, 'maximum': 10000, 'minimum': 0, 'type': 'integer'}}}},
    ('nginx_name_server', 'PUT'): {'json': DefinitionsServer},
}

filters = {
    ('balancer_balancer_name_frontend', 'PUT'): {200: {'headers': None, 'schema': {'type': 'boolean'}}},
    ('balancer_balancer_name_frontend', 'GET'): {200: {'headers': None, 'schema': DefinitionsFrontend}},
    ('balancer_balancer_name_backends', 'PUT'): {200: {'headers': None, 'schema': {'type': 'boolean'}}},
    ('balancer_balancer_name_backends', 'POST'): {201: {'headers': None, 'schema': {'type': 'boolean'}}},
    ('balancer_balancer_name_backends', 'GET'): {200: {'headers': None, 'schema': {'items': DefinitionsBackend, 'type': 'array'}}},
    ('balancer_balancer_name_backends', 'DELETE'): {200: {'headers': None, 'schema': {'type': 'boolean'}}},
    ('balancer_balancer_name_entrypoints', 'PUT'): {200: {'headers': None, 'schema': {'type': 'boolean'}}},
    ('balancer_balancer_name_entrypoints', 'POST'): {201: {'headers': None, 'schema': {'type': 'boolean'}}},
    ('balancer_balancer_name_entrypoints', 'GET'): {200: {'headers': None, 'schema': {'items': DefinitionsEntrypoint, 'type': 'array'}}},
    ('balancer_balancer_name_entrypoints', 'DELETE'): {200: {'headers': None, 'schema': {'type': 'boolean'}}},
    ('nginx', 'POST'): {201: {'headers': None, 'schema': DefinitionsNginx}},
    ('nginx', 'GET'): {200: {'headers': None, 'schema': {'items': DefinitionsNginx, 'type': 'array'}}},
    ('balancer_names_prefix', 'GET'): {200: {'headers': None, 'schema': {'items': {'type': 'string'}, 'type': 'array'}}},
    ('nginx_name', 'DELETE'): {200: {'headers': None, 'schema': {'type': 'boolean'}}},
    ('nginx_name', 'GET'): {200: {'headers': None, 'schema': DefinitionsNginx}},
    ('nginx_name_upstream', 'PUT'): {200: {'headers': None, 'schema': {'type': 'boolean'}}},
    ('nginx_name_upstream', 'GET'): {200: {'headers': None, 'schema': DefinitionsUpstream}},
    ('balancer', 'POST'): {201: {'headers': None, 'schema': DefinitionsBalancer}},
    ('balancer', 'GET'): {200: {'headers': None, 'schema': {'items': DefinitionsBalancer, 'type': 'array'}}},
    ('balancer_balancer_name', 'DELETE'): {200: {'headers': None, 'schema': {'type': 'boolean'}}},
    ('balancer_balancer_name', 'GET'): {200: {'headers': None, 'schema': DefinitionsBalancer}},
    ('slaves', 'GET'): {200: {'headers': None, 'schema': {'items': DefinitionsSlave, 'type': 'array'}}},
    ('nginx_name_server', 'PUT'): {200: {'headers': None, 'schema': {'type': 'boolean'}}},
    ('nginx_name_server', 'GET'): {200: {'headers': None, 'schema': DefinitionsServer}},
}

scopes = {
}


class Security(object):

    def __init__(self):
        super(Security, self).__init__()
        self._loader = lambda: []

    @property
    def scopes(self):
        return self._loader()

    def scopes_loader(self, func):
        self._loader = func
        return func

security = Security()


def merge_default(schema, value):
    # TODO: more types support
    type_defaults = {
        'integer': 9573,
        'string': 'something',
        'object': {},
        'array': [],
        'boolean': False
    }

    return normalize(schema, value, type_defaults)[0]


def normalize(schema, data, required_defaults=None):

    if required_defaults is None:
        required_defaults = {}
    errors = []

    class DataWrapper(object):

        def __init__(self, data):
            super(DataWrapper, self).__init__()
            self.data = data

        def get(self, key, default=None):
            if isinstance(self.data, dict):
                return self.data.get(key, default)
            if hasattr(self.data, key):
                return getattr(self.data, key)
            else:
                return default

        def has(self, key):
            if isinstance(self.data, dict):
                return key in self.data
            return hasattr(self.data, key)

    def _normalize_dict(schema, data):
        result = {}
        data = DataWrapper(data)
        for key, _schema in schema.get('properties', {}).iteritems():
            # set default
            type_ = _schema.get('type', 'object')
            if ('default' not in _schema
                    and key in schema.get('required', [])
                    and type_ in required_defaults):
                _schema['default'] = required_defaults[type_]

            # get value
            if data.has(key):
                result[key] = _normalize(_schema, data.get(key))
            elif 'default' in _schema:
                result[key] = _schema['default']
            elif key in schema.get('required', []):
                errors.append(dict(name='property_missing',
                                   message='`%s` is required' % key))
        return result

    def _normalize_list(schema, data):
        result = []
        if isinstance(data, (list, tuple)):
            for item in data:
                result.append(_normalize(schema.get('items'), item))
        elif 'default' in schema:
            result = schema['default']
        return result

    def _normalize_default(schema, data):
        if data is None:
            return schema.get('default')
        else:
            return data

    def _normalize(schema, data):
        if not schema:
            return None
        funcs = {
            'object': _normalize_dict,
            'array': _normalize_list,
            'default': _normalize_default,
        }
        type_ = schema.get('type', 'object')
        if not type_ in funcs:
            type_ = 'default'

        return funcs[type_](schema, data)

    return _normalize(schema, data), errors

