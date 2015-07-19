from abc import ABCMeta, abstractmethod

from future.utils import with_metaclass

import env2config.util as util
from env2config.processors import LineProcessor, RewriteProcessor

logger = util.create_logger()


class PluginMount(ABCMeta):
    '''Based on http://martyalchin.com/2008/jan/10/simple-plugin-framework/
    '''
    def __init__(cls, name, bases, attrs):
        if not hasattr(cls, '_plugins'):
            # This branch only executes when processing the mount point itself.
            # So, since this is a new plugin type, not an implementation, this
            # class shouldn't be registered as a plugin. Instead, it sets up a
            # list where plugins can be registered later.
            cls._plugins = {}
        else:
            # This must be a plugin implementation, which should be registered.
            # Simply appending it to the list is all that's needed to keep
            # track of it later.
            if hasattr(cls, 'service_name'):
                logger.debug('registering plugin: %s = %s', cls.service_name, cls)
                cls._plugins[cls.service_name] = cls
            else:
                logger.debug('class %s not registered as a plugin because it lacks a "service_name" property', cls)


class ServiceDefinition(with_metaclass(PluginMount, object)):

    def __init__(self, version, tags):
        self.version = version
        self.tags = tags

    @classmethod
    def get_service_class(cls, service_name):
        return cls._plugins[service_name]

    @abstractmethod
    def default_configs(self):
        raise NotImplementedError()

    @abstractmethod
    def config_mapping(self):
        raise NotImplementedError()

    def config_multiplex(self, config_name):
        configs = self.default_configs()
        assert len(configs) == 1, \
            'You must override config_multiplex if a service has more than one config'
        config = list(configs.keys())[0]
        return config, config_name

    def ignore_env_names(self):
        return []

    def convert_name(self, config_name):
        return config_name

    def convert_value(self, config_value):
        return config_value


class LineOriented(ServiceDefinition):
    Processor = LineProcessor

    @abstractmethod
    def match_line(self, line, config_name):
        raise NotImplementedError()

    @abstractmethod
    def inject_line(self, old_line, config_name, config_value):
        raise NotImplementedError()

    @abstractmethod
    def comment_line(self, content):
        raise NotImplementedError()


class RewriteOriented(ServiceDefinition):
    Processor = RewriteProcessor
    @abstractmethod
    def parse_file(self, text_content):
        raise NotImplementedError()

    @abstractmethod
    def inject_file(self, default_model, config_model):
        raise NotImplementedError()
