import os
import sys
import logging
import traceback

import tingyun.api.initial.import_hook
from tingyun.api.log_file import initialize_logging
import tingyun.api.settings
from tingyun.api.exception import ConfigurationError
from tingyun.api.mapper import map_log_level, map_app_name, map_key_words

try:
    import ConfigParser  # for python2.x
except ImportError:
    import configparser as ConfigParser  # for python3.x


__all__ = ['initialize']

_detect_done = False
_configuration_done = False
_module_import_hook_registry = {}
_module_import_hook_results = {}
_logger = logging.getLogger(__name__)
_settings = tingyun.api.settings.global_settings()
_config_parser = ConfigParser.RawConfigParser()
_catch_settings = []

# import returns them to caller.
sys.meta_path.insert(0, tingyun.api.initial.import_hook.ImportHookFinder())


def _module_import_hook(target_module, hook_module, function):

    def _detect(target_module):

        try:
            getattr(tingyun.api.initial.import_hook.import_module(hook_module), function)(target_module)
            _module_import_hook_results[(target_module.__name__, hook_module, function)] = ''
        except Exception as _:
            _logger.error("error occurred: %s" % traceback.format_exception(*sys.exc_info()))

    return _detect


def _process_setting(section, option, getter='get', mapper=None):
    """used to check the configuration section/option is right or not. and set it to the settings. At there we didn't
    check the validity of the value,left to next node

    """
    
    try:
        value = getattr(_config_parser, getter)(section, option)
        if mapper:
                value = mapper(value)

        # use the default value in settings
        if value is None:
            return

        target = _settings
        fields = option.split('.', 1)

        while True:
            if len(fields) == 1:
                setattr(target, fields[0], value)
                break
            else:
                target = getattr(target, fields[0])
                fields = fields[1].split('.', 1)

        # catch the settings for debug
        _catch_settings.append((option, value))
    except ConfigParser.NoSectionError:
        _logger.info("No section[%s] in configure file", section)
    except ConfigParser.NoOptionError:
        _logger.info("No option[%s] in configure file", option)
    except Exception as err:
        _logger.warning("Parse config file errors,  section[%s]-option[%s] will use default value instead. %s", err)


def _process_configuration(section):
    """ used to process the ini file config mapping to settings
    :param section: ini config file section
    :return:
    """
    _process_setting(section, 'license_key', "get", None)
    _process_setting(section, 'enabled', "get", map_key_words)
    _process_setting(section, 'app_name', "get", map_app_name)
    _process_setting(section, 'audit_mode', "get", map_key_words)
    _process_setting(section, 'auto_action_naming', "get", map_key_words)
    _process_setting(section, 'ssl', "get", map_key_words)
    _process_setting(section, 'action_tracer.log_sql', "get", map_key_words)
    _process_setting(section, 'daemon_debug', "get", map_key_words)
    _process_setting(section, 'enable_profile', "get", map_key_words)


def _load_configuration(config_file=None, log_file=None, log_level=None):
    """load the the hole configuration
    """
    _logger.debug("configure file is: %s", config_file)
    global _configuration_done

    if _configuration_done:
        return

    _configuration_done = True
    if not _config_parser.read(config_file):
        raise ConfigurationError("Unable to fetch the configure file, %s", config_file)
    
    _settings.config_file = config_file
    _process_setting('tingyun', 'log_file', 'get', None)  # section, option in tingyun.ini, 'get' in configParser
    _process_setting('tingyun', 'log_level', 'get', map_log_level)
    
    if not log_file:
        log_file = _settings.log_file
        
    if not log_level:
        log_level = _settings.log_level
    
    initialize_logging(log_file, log_level)
    _process_configuration('tingyun')


def _process_module_definition_wrapper(target_module, hook_module, hook_function='detect'):
    """deal and register the hook for specified modules
    """
    _logger.debug("Loading target module %s, with wrapper function %s", target_module, hook_function)
    _module_import_hook_registry[target_module] = (hook_module, hook_function)
    _module_import_hook_results.setdefault((target_module, hook_module, hook_function), None)
    tingyun.api.initial.import_hook.register_import_hook(target_module, _module_import_hook(target_module, hook_module,
                                                                                            hook_function))


def _process_module_builtin():
    """deal the supported builtin default modules, such as django. and so on
    """
    _process_module_definition_wrapper('django.core.handlers.base', 'tingyun.hooks.framework_django',
                                       'detect_django_core_handlers_base')
    _process_module_definition_wrapper("django.core.handlers.wsgi", "tingyun.hooks.framework_django",
                                       "detect_django_core_handlers_wsgi")
    _process_module_definition_wrapper("django.views.generic.base", "tingyun.hooks.framework_django",
                                       "detect_django_views_generic_base")
    _process_module_definition_wrapper('django.core.urlresolvers', 'tingyun.hooks.framework_django',
                                       'detect_django_core_urlresolvers')

    # for detect template
    _process_module_definition_wrapper('django.template.loader_tags', 'tingyun.hooks.framework_django',
                                       'detect_django_template_loader_tags')
    _process_module_definition_wrapper('django.template.base', 'tingyun.hooks.framework_django',
                                       'detect_django_template')

    # for django core function
    _process_module_definition_wrapper('django.http.multipartparser', 'tingyun.hooks.framework_django',
                                       'detect_django_http_multipartparser')
    _process_module_definition_wrapper('django.core.mail', 'tingyun.hooks.framework_django',
                                       'detect_django_core_mail')
    _process_module_definition_wrapper('django.core.mail.message', 'tingyun.hooks.framework_django',
                                       'detect_django_core_mail_message')

    # detect the database: sql/nosql the comment part is not current verified
    # mysql
    _process_module_definition_wrapper('MySQLdb', 'tingyun.hooks.database_dbapi2')
    _process_module_definition_wrapper('pymysql', 'tingyun.hooks.database_dbapi2')
    _process_module_definition_wrapper('oursql', 'tingyun.hooks.database_dbapi2')

    # oracle
    _process_module_definition_wrapper('cx_Oracle', 'tingyun.hooks.database_dbapi2')

    # database DB-API interface IBM Data Servers DB2 Informix
    # _process_module_definition_wrapper('ibm_db_dbi', 'tingyun.hooks.database_dbapi2')

    # postgres SQL
    _process_module_definition_wrapper('postgresql.interface.proboscis.dbapi2', 'tingyun.hooks.database_dbapi2')
    _process_module_definition_wrapper('psycopg2', 'tingyun.hooks.database_dbapi2')
    _process_module_definition_wrapper('psycopg2ct', 'tingyun.hooks.database_dbapi2')
    _process_module_definition_wrapper('psycopg2cffi', 'tingyun.hooks.database_dbapi2')

    # ODBC A Python DB API 2 module for ODBC
    _process_module_definition_wrapper('pyodbc', 'tingyun.hooks.database_dbapi2')

    # nosql memcached
    _process_module_definition_wrapper('memcache', 'tingyun.hooks.memcache_memcache')

    # nosql mongodb
    _process_module_definition_wrapper('pymongo.mongo_client', 'tingyun.hooks.database_mongo', "detect_mongo_client")
    _process_module_definition_wrapper('pymongo.connection', 'tingyun.hooks.database_mongo', "detect_connection")
    _process_module_definition_wrapper('pymongo.collection', 'tingyun.hooks.database_mongo', "detect_collection")

    # nosql redis
    _process_module_definition_wrapper('redis.connection', 'tingyun.hooks.database_redis', "detect_connection")
    _process_module_definition_wrapper('redis.client', 'tingyun.hooks.database_redis', "detect_client_operation")

    _process_module_definition_wrapper('urllib', 'tingyun.hooks.external_urllib')  # Python 2
    _process_module_definition_wrapper('urllib2', 'tingyun.hooks.external_urllib2')
    _process_module_definition_wrapper('urllib3.request', 'tingyun.hooks.external_urllib3')


def initialize(config_file=None):
    """ init entrance
    """
    _logger.debug("initializing python agent...")
    global _detect_done

    if not os.path.isfile(config_file):
        _logger.error('python agent configure file is not found, agent stop to start.')
        return False

    _load_configuration(config_file=config_file)

    if not _detect_done:
        _detect_done = True
        _process_module_builtin()

    return True
