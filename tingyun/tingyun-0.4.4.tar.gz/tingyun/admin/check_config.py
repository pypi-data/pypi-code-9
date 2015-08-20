from __future__ import print_function
from tingyun.api.settings import global_settings
from tingyun.api.mapper import ENV_CONFIG_FILE, CONFIG_ITEM

try:
    import ConfigParser  # for python2.x
except ImportError:
    import configparser as ConfigParser  # for python3.x

_config_parser = ConfigParser.RawConfigParser()


def check_config(args):
    """
    :param args:
    :return:
    """
    import sys
    import os

    name = 'check-config'
    options = '[config file absolutely path]'
    description = "Executes the command line for check the configuration config. " \
                  "default use environment variable %s" % ENV_CONFIG_FILE

    def print_tips(msgs, level="Errors"):
        """
        :param msgs:
        :return:
        """
        print("----------------------%s------------------------" % level)
        for msg in msgs:
            print("  ", msg)

        print("----------------------End---------------------------")

        if "Errors" == level:
            sys.exit(1)

    errors = []
    warnings = []
    config_file = os.environ.get(ENV_CONFIG_FILE, "")

    if (len(args) > 0) and len(args) != 1:
        print('tingyun-admin check-config %s' % options)
        sys.exit(1)

    if 1 == len(args):
        config_file = args[0]

    print("Use config file:", config_file)

    env_msg = ''
    if 0 == len(args):
        env_msg = "Please set the environment variable[%s] for agent config file." % ENV_CONFIG_FILE

    if not os.path.exists(config_file):
        errors.append("Errors: config file is not exist. " + env_msg)
        print_tips(errors)
        return

    if not _config_parser.read(config_file):
        errors.append("Errors: unable to read the config file. please check the file permission.")
        print_tips(errors)
        return

    # check the config detail.
    default_settings = global_settings()
    multi_attr = {"action_tracer.log_sql": default_settings.action_tracer.log_sql}
    for item in CONFIG_ITEM:
        ret = _process_setting(item["section"], item["key"], 'get', item["mapper"])
        if ret[0] < 0:
            errors.append(ret[2])
            break

        if 0 == ret[0] and 'log_file' != item["key"] and 'license_key' != item["key"]:
            if item["key"] in multi_attr:
                v = multi_attr[item["key"]]
            else:
                v = getattr(default_settings, item["key"]) if 'log_level' != item["key"] else "logging.DEBUG"
            warnings.append(ret[2] + " Use default value [%s] instead." % v)
            continue

        if 'log_file' == item["key"] and not ret[1]:
            warnings.append("config option <log_file> is not defined, agent log will output to stderr.")
            continue

        if 'log_file' == item["key"] and ret[1]:
            try:
                with open(ret[1], "a+") as fd:
                    fd.write("agent check log file config input message.\n")
            except Exception as _:
                warnings.append("Current user[%s] not allowed to access the log file[%s]."
                                % (os.environ["USER"], ret[1]))

        if 'license_key' == item["key"] and not ret[1]:
            errors.append("config option <license_key> is not defined, agent will not work well.")
            continue

    if warnings:
        print_tips(warnings, "Warning")

    if errors:
        print_tips(errors)

    if not errors:
        print("\nCheck agent config file success!!")


def _process_setting(section, option, getter='get', mapper=None):
    """
    Return: [errorCode, value, errMsg]

    """
    try:
        map_value = ""
        value = getattr(_config_parser, getter)(section, option)
        if mapper:
                map_value = mapper(value)

        # use the default value in settings
        if map_value is None:
            return [0, None, "%s=%s, %s is not supported." % (option, value, value)]

        return [1, value, ""]

    except ConfigParser.NoSectionError:
        return [-1, None, "Section [%s] is not specified." % section]
    except ConfigParser.NoOptionError:
        return [0, None, "Option <%s> is not exist." % option]
    except Exception as err:
        return [-1, None, err]
