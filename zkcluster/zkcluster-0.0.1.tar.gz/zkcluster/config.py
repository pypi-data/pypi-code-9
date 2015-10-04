from logging.config import fileConfig
import re

from .util import compat
from . import exc


class Config(object):
    def __init__(self, prefix="zk_"):
        self.services = {}
        self.sources = []
        self.prefix = prefix

    def add_config(self, config):
        for section in config.sections():
            if section.startswith("%sservice" % self.prefix):
                self.add_service_config(dict(config.items(section)))

    def add_config_from_config_string(self, string):
        file_config = compat.SafeConfigParser()
        file_config.readfp(compat.StringIO(string))
        self.sources.append("<string>")
        self.add_config(file_config)

    def add_config_from_config_file(self, fname):
        file_config = compat.SafeConfigParser()
        file_config.read(fname)
        self.add_config(file_config)
        self.sources.append(fname)

    def load_logging_configs(self):
        for fname in self.sources:
            self._attempt_logging_config(fname)

    def _attempt_logging_config(self, fname):
        try:
            fileConfig(fname, disable_existing_loggers=False)
        except compat.configparser.NoSectionError:
            pass

    def add_service_config(self, service_cfg):
        cfg_dict = {}
        for element in server_config_names:
            if element.name in service_cfg:
                raw_value = service_cfg[element.name]
                element.apply_fixer(raw_value, cfg_dict)
            else:
                element.apply_default(cfg_dict)
        self.services[cfg_dict['name']] = cfg_dict

    @classmethod
    def from_config_string(cls, string, prefix="zk_"):
        config = Config(prefix=prefix)
        config.add_config_from_config_string(string)
        return config

    @classmethod
    def from_config_file(cls, fname, prefix="zk_"):
        config = Config(prefix=prefix)
        config.add_config_from_config_file(fname)
        return config

    def config_for_servicename(self, service_name):
        try:
            service_cfg = self.services[service_name]
        except KeyError:
            raise exc.ConfigurationException(
                "No such service config: %r" % service_name)
        else:
            return service_cfg


class Fixer(object):

    def apply_to_dict(self, key, fixed_value, dest_dict):
        dest_dict[key] = fixed_value

    def fix_value(self, value):
        if value == 'none':
            value = None

        if value is not None:
            value = self.fix_non_none_value(value)
        return value

    def fix_non_none_value(self, value):
        return value

    def __call__(self, key, raw_value, dest_dict):
        self.apply_to_dict(
            key, self.fix_value(raw_value), dest_dict
        )


class BoolFixer(Fixer):
    def fix_non_none_value(self, value):
        if value.lower() in ('true', 1, 'yes'):
            return True
        elif value.lower() in ('false', 0, 'no'):
            return False
        else:
            raise ValueError("Invalid boolean string: %r" % value)


class IntFixer(Fixer):
    def fix_non_none_value(self, value):
        return int(value)


class StringListFixer(Fixer):
    def fix_non_none_value(self, value):
        return list(
            [e for e in
                [elem.strip() for elem in re.split(r', +', value)]
                if e])


class SAURLFixer(Fixer):
    def fix_non_none_value(self, value):
        return url.make_url(value)


class HostFixer(Fixer):
    def __init__(self, default_port=None):
        self.default_port = default_port

    def fix_value(self, value):
        lines = re.split("\n", value.strip())
        hosts = []
        for line in lines:
            # skip commented lines
            if re.match('^\s*#', line):
                continue

            host_rec = {}
            tokens = re.split("(?:\s|(=))+", line.strip())

            host_rec['name'] = tokens.pop(0)

            while tokens:
                token_key = tokens.pop(0)
                if tokens and tokens[0] == "=":
                    tokens.pop(0)
                    try:
                        token_value = tokens.pop(0)
                    except IndexError:
                        raise exc.ConfigurationException(
                            "Expected value after symbol %r: %r" %
                            (token_key, line))
                    else:
                        if token_key == 'hostname':
                            port_key = 'port'
                        elif token_key == 'bind':
                            port_key = 'bind_port'
                        else:
                            port_key = None

                        if port_key:
                            if ':' in token_value:
                                host, port = token_value.split(":", 1)
                                port = IntFixer().fix_value(port)
                                host_rec[port_key] = port
                            elif port_key == 'port':
                                host = token_value
                                host_rec[port_key] = self.default_port
                            elif port_key == 'bind_port':
                                host = token_value
                            host_rec[token_key] = host

                elif token_key is not None:
                    host_rec[token_key] = True

            if 'hostname' not in host_rec:
                raise exc.ConfigurationException(
                    "hostname is required in host record: %r" % line)

            if 'bind' not in host_rec:
                host_rec['bind'] = '0.0.0.0'
            if 'bind_port' not in host_rec:
                host_rec['bind_port'] = host_rec['port']
            hosts.append(host_rec)
        return hosts


class ConfigElement(object):
    __slots__ = 'name', 'fixer', 'default'

    def __init__(self, name, fixer=Fixer, default=None, fixer_defaults={}):
        self.name = name
        self.fixer = fixer(**fixer_defaults)
        self.default = default

    def apply_fixer(self, raw_value, cfg_dict):
        self.fixer(self.name, raw_value, cfg_dict)

    def apply_default(self, cfg_dict):
        if self.default is _REQUIRED:
            raise exc.ConfigurationException(
                "Argument %r is required" % self.name)
        self.fixer.apply_to_dict(self.name, self.default, cfg_dict)

_REQUIRED = object()

server_config_names = [
    ConfigElement('name', default=_REQUIRED),
    ConfigElement(
        'nodes', HostFixer, default=_REQUIRED,
        fixer_defaults={"default_port": 5084}),
    ConfigElement('use_auth', BoolFixer, False),
    ConfigElement('auth_key', default=None),
    ConfigElement('auth_secret', default=None),
    ConfigElement('cluster_servers', BoolFixer, True),
    ConfigElement('ssl_keyfile'),
    ConfigElement('ssl_certfile'),
]


_CFG = Config()

