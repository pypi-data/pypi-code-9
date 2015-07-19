import os
import sys
import json
from glob import glob
from fnmatch import fnmatch

import env2config.services
import env2config.util as util
from env2config.interface import ServiceDefinition


logger = util.create_logger()


ENV_INJECT_KEY = 'ENV_INJECT'


def _tag_path(root, tags):
    tag_string = ','.join(
        '{0}={1}'.format(key, str(value))
        for key, value in sorted(tags.items(), key=lambda p: p[0])
    )
    return os.path.join(root, tag_string)


def _service_path(root, service_name):
    return os.path.join(root, service_name)


def _version_path(root, version):
    return os.path.join(root, version)


def _parse_inject_src(src, potential_filenames):
    src = src.strip()
    if src.startswith('/'):
        # absolute path refers to a local file, not a configured default
        src_user = os.path.expanduser(src)
        globbed = glob(src_user)
        if len(globbed) == 0:
            logger.warn('spec src %s not found. Was expanded to %s', src, src_user)

        for abs_src in globbed:
            src_filename = os.path.basename(abs_src)

            for filename in potential_filenames:
                if fnmatch(filename, src_filename):
                    yield abs_src, filename

    else:
        # relative path refers to a supported default
        for filename in potential_filenames:
            if fnmatch(filename, src):
                yield filename, filename


def _inject_string_to_dict(string, potential_filenames):
    logger.debug('reading injection spec "%s"', string)
    config_pairs = string.split(',')
    config_dict = {}
    override = set()
    for config_pair in config_pairs:
        src, dest = config_pair.split(':')

        for src, matching in _parse_inject_src(src, potential_filenames):
            config_dict[src] = dest
            override.add(matching)

    logger.debug('parsed injection spec as %s', config_dict)

    return config_dict, override


def build(service_name, version, root_config_dir, tags):
    '''Build Step'''

    service_class = ServiceDefinition.get_service_class(service_name)
    service = service_class(version, tags)

    default_configs = service.default_configs()

    # Create all of the directories that we need.
    # Go one-by-one to improve error reporting.

    # e.g. ./default_configs
    if not os.path.exists(root_config_dir):
        logger.debug('creating root path: %s', root_config_dir)
        os.mkdir(root_config_dir)

    # e.g. ./default_configs/scala=2.11-distribution=kafka/
    if tags != {}:
        tag_root = _tag_path(root_config_dir, tags)
        if not os.path.exists(tag_root):
            logger.debug('creating tags root path %s', tag_root)
            os.mkdir(tag_root)
        service_parent_root = tag_root
    else:
        service_parent_root = root_config_dir

    # e.g. ./default_configs/kafka
    # e.g. ./default/configs/scala=2.11-distribution=apache/kafka
    service_root = _service_path(service_parent_root, service_name)
    if not os.path.exists(service_root):
        logger.debug('creating service root path: %s', service_root)
        os.mkdir(service_root)

    # e.g. ./default_configs/redis/3.0.1
    # e.g. ./default/configs/scala=2.11-distribution=apache/kafka/2.8.0.2
    version_root = _version_path(service_root, version)
    if not os.path.exists(version_root):
        logger.debug('creating version root path %s', version_root)
        os.mkdir(version_root)

    default_paths = {}
    for name, get_content in default_configs.items():
        path = os.path.join(version_root, name)
        logger.debug('considering default config file %s', path)

        if not os.path.exists(path):
            logger.debug('downloading  default config file %s to %s', name, path)
            content = get_content()
            with open(path, 'w') as f:
                f.write(content)
        else:
            logger.debug('file exists, not downloaded')

        default_paths[name] = path

    return True


def inject(root_config_dir):
    '''Inject Step'''

    configs_to_inject = []
    logger.debug('injecting configs from directory %s', root_config_dir)

    def find_service(root, service, tags):
        # e.g. ./default_configs/redis
        logger.debug('found service %s', service_name)
        service_name_directory = os.path.join(root, service_name)
        for version in os.listdir(service_name_directory):
            logger.debug('found service %s version %s', service_name, version)
            # second level, folders as versions
            # e.g. ./default_configs/redis/3.0.1
            version_directory = os.path.join(service_name_directory, version)
            configs_to_inject.append(
                (service_name, version, version_directory, tags)
            )

    # e.g. ./default_configs
    for service_or_tag_name in os.listdir(root_config_dir):
        # first level, folders are service names or tag directories
        # tag directories are located by finding an '=' in the name

        if '=' in service_or_tag_name:
            tag_name = service_or_tag_name
            tag_directory = os.path.join(root_config_dir, tag_name)
            logger.debug('found tags %s', tag_name)

            tag_strings = tag_name.split(',')
            tags = util.tags_to_dict(tag_strings)
            logger.debug('parsed tags %s', tags)

            for service_name in os.listdir(tag_directory):
                find_service(tag_directory, service_name, tags)

        else:
            service_name = service_or_tag_name
            find_service(root_config_dir, service_name, {})

    results = []
    for service_name, version, version_directory, tags in configs_to_inject:
        result = _inject_service(service_name, version, version_directory, tags)
        results.append(result)

    return all(results)


def _inject_service(service_name, version, config_dir, tags):
    logger.debug('injecting configs for service %s version %s', service_name, version)

    # Load the service class and instantiate it.
    service_class = ServiceDefinition.get_service_class(service_name)
    service = service_class(version, tags)

    # Determine which configuration files to inject by overriding
    # defaults defined by the service with arguments supplied in the
    # ENV_INJECT variable

    env_prefix = service_name.upper()

    default_filenames = list(service.default_configs().keys())

    builtin = service.config_mapping()
    logger.debug('considering default injectable configs %s', builtin)

    env_inject_string = os.environ.get(ENV_INJECT_KEY)
    if env_inject_string is None:
        env_inject = {}
        env_overriden = set()
    else:
        env_inject, env_overriden = _inject_string_to_dict(env_inject_string, default_filenames)

    not_overriden = dict((k, v) for k, v in builtin.items() if k not in env_overriden)
    configs_to_inject = dict(not_overriden, **env_inject)
    logger.debug('resolved to inject configs %s', configs_to_inject)

    # Collect injectable configs from all environment variables
    # beginning with the service prefix.
    # e.g. REDIS_FOO=1 => {'foo': '1'}

    injectables = {}
    blacklist = service.ignore_env_names()
    for env_name, env_value in os.environ.items():
        if env_name in blacklist:
            logger.debug('env variable %s ignore because it is in the service blacklist')
            continue

        if env_name == ENV_INJECT_KEY:
            logger.debug('env variable %s ignored because it is the injection key')
            continue

        if env_name.startswith(env_prefix):
            logger.debug('found injectable env variable %s')
            start = env_name.find('_') + 1
            config_part = env_name[start:]

            config_filename, config_part = service.config_multiplex(config_part)
            config_name = service.convert_name(config_part)
            config_value = service.convert_value(env_value)

            logger.debug('found potential inject (name: %s, value: %s) into %s', config_name, config_value, config_filename)
            injectables[config_name] = (config_filename, config_value)

    processor = service.Processor(
        service=service,
        config_dir=config_dir,
        configs_to_inject=configs_to_inject,
        injectables=injectables,
    )
    processor.process()

    return True
