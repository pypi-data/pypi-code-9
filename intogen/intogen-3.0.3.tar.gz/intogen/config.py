import inspect
import logging
import sys
import bgdata
from shutil import copyfile
import intogen
from intogen.constants.configuration import MAIN_SCRIPT_CONFIGURATION
import os
from configobj import ConfigObj, flatten_errors, get_extra_values, interpolation_engines, TemplateInterpolation, \
    MissingInterpolationOption
import time
from validate import Validator, VdtTypeError, ValidateError
from bgdata.configobj import BgDataInterpolation
from intogen.executor import drmaa
from intogen.setup import DATA_DEPENDENCIES
from intogen.utils import get_nested
from intogen.executor.drmaa import TaskExecutor
from intogen.generators import ProjectsGenerator, ProjectGroupsGenerator

_CONFIG_SINGLETON = None


def get_intogen_home():
    intogen_home = os.path.expandvars(os.path.expanduser(
        os.getenv('INTOGEN_HOME', '~/.intogen/')
    ))

    # Remove last slash if present
    intogen_home = intogen_home.rstrip(os.path.sep)
    return os.path.join(os.path.sep, intogen_home)


class IntogenInterpolation(TemplateInterpolation):

    _BGDATA_ENGINE = BgDataInterpolation(None)

    def _fetch(self, key):

        if key == "intogen_home":
            return get_intogen_home(), self.section

        if key in DATA_DEPENDENCIES:
            project, dataset, version = DATA_DEPENDENCIES[key]
            path = bgdata.get_path(project, dataset, version)
            return path, self.section

        raise MissingInterpolationOption(key)

    def interpolate(self, key, value):
        value = TemplateInterpolation.interpolate(self, key, value)
        return self._BGDATA_ENGINE.interpolate(key, value)


# Register custom interpolation engine
interpolation_engines['intogen'] = IntogenInterpolation


def get_config(options=None, tasks=None):
    global _CONFIG_SINGLETON
    if _CONFIG_SINGLETON is None:
        _CONFIG_SINGLETON = ConfigManager(options, tasks)

    return _CONFIG_SINGLETON


class ConfigManager(object):
    def manage_main_log(self, options):
        main_log_dir = options.results_dir if options.results_dir is not None else self.get_system_config("results_dir")
        if not os.path.exists(main_log_dir):
            os.makedirs(main_log_dir)

        # define main log file
        timestamp = str(time.time()).split(".")[0]
        logfile = "{0}/{1}.{2}".format(main_log_dir, "intogen", timestamp)
        logging.getLogger().addHandler(logging.FileHandler(logfile))

        # symlink last main log file
        symlink_path = os.path.join(main_log_dir, "intogen.log")
        if os.path.exists(symlink_path):
            os.remove(symlink_path)
        os.symlink(os.path.basename(logfile), symlink_path)

    def register_config_specifications(self, config_specs, tasks):

        if tasks is not None:
            for task in tasks:
                logging.debug("Registering config for task '{}'".format(task))
                for spec, validation in task.get_configuration_definitions().items():
                    if spec in config_specs:
                        if config_specs[spec] != validation:
                            raise RuntimeError("Validataion specification conflict for '{}': ".format(spec) +
                                               "first validation: '{}', repeated validation: '{}'".format(config_specs[spec],
                                                                                                          validation))
                    config_specs[spec] = validation

        for task in intogen.tasks.__all__:
            module = sys.modules["intogen.tasks." + task]
            registered = False
            for name, member in inspect.getmembers(module):
                if name is 'IntogenTask':
                    continue
                # go get configuration from all classes extending IntogenTask
                elif inspect.isclass(member) and 'IntogenTask' in [str(x.__name__) for x in inspect.getmro(member)]:
                    logging.debug("Registering config for task '{}'".format(task))
                    for spec, validation in member.get_configuration_definitions().items():
                        if spec in config_specs:
                            if config_specs[spec] != validation:
                                raise RuntimeError("Validataion specification conflict for '{}': ".format(spec) +
                                                   "first validation: '{}', repeated validation: '{}'".format(config_specs[spec],
                                                                                                              validation))
                        config_specs[spec] = validation
                    registered = True
            if not registered:
                logging.warning("Task '" + task + "' does not register any configuration")

    def validate_system_conf(self, validation):
        if validation != True:
            for section, prop, error in flatten_errors(self.system_config, validation):
                logging.error("system.conf entry problem at {0} property '{1}': {2}".format(section, prop, error))
            exit(1)

        validation_error = False
        for validation in get_extra_values(self.system_config):
            validation_error = True
            logging.error("Invalid system.conf property '{0}' at {1}.".format(validation[1], validation[0]))
        if validation_error:
            raise Exception("Revisit .conf files and fix the erroneous configuration")

    def validate_task_conf(self, validation):
        if not validation:
            for section, prop, error in flatten_errors(self.system_config, validation):
                logging.error("task.conf entry problem at {0} property '{1}': {2}".format(section, prop, error))
            exit(1)

    def __init__(self, options=None, tasks=None):

        # Config the global logging
        log_level = logging.INFO if not drmaa.DEBUGGING else logging.DEBUG
        logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', datefmt='%H:%M:%S', level=log_level)

        # Make home directory if not exists
        self.home_path = get_intogen_home()
        if not os.path.exists(self.home_path):
            os.makedirs(self.home_path)

        # Configuration specifications
        config_specs = ConfigObj()

        # register configuration from main intogen
        for config, system_validation in MAIN_SCRIPT_CONFIGURATION.items():
            config_specs[config] = system_validation
        # register configuration from each task
        self.register_config_specifications(config_specs, tasks)

        # Read global configuration
        # System conf
        self.system_config = ConfigObj(interpolation='intogen', configspec=config_specs)

        config_filenames = set(['system.conf'])
        if tasks is not None:
            config_filenames.update([t.get_configuration_filename() for t in tasks])
        for config_filename in config_filenames:
            system_conf_path = os.path.join(self.home_path, '{}'.format(config_filename))

            if not os.path.exists(system_conf_path):
                config_template = os.path.join(os.path.dirname(__file__), "templates", config_filename + ".template")
                if os.path.exists(config_template):
                    copyfile(config_template, system_conf_path)
                else:
                    logging.error("file {} not found!".format(system_conf_path))
                    continue

            self.system_config.merge(ConfigObj(system_conf_path, interpolation='intogen'))

        # Task conf
        task_conf_file = os.path.join(self.home_path, 'task.conf')
        task_validation_file = os.path.join(self.home_path, 'task.validation')

        if not os.path.exists(task_validation_file):
            task_validation_template = os.path.join(os.path.dirname(__file__), "templates", "task.validation")
            copyfile(task_validation_template, task_validation_file)

        if not os.path.exists(task_conf_file):
            task_conf_template = os.path.join(os.path.dirname(__file__), "templates", "task.conf.template")
            copyfile(task_conf_template, task_conf_file)

        # Load task configuration files
        self.task_config = ConfigObj(interpolation='intogen', configspec=task_validation_file)
        if os.path.exists(task_conf_file):
            self.task_config.merge(ConfigObj(task_conf_file, interpolation='intogen'))
        else:
            logging.error("file {} not found!".format(task_conf_file))

        # Load scheduler configuration files
        scheduler_file = os.path.join(self.home_path, 'scheduler.conf')
        if not os.path.exists(scheduler_file):
            scheduler_file_template = os.path.join(os.path.dirname(__file__), "templates", "scheduler.conf.template")
            copyfile(scheduler_file_template, scheduler_file)

        # create log-file for intogen-call
        if options is not None:
            self.manage_main_log(options)

        # Prepare output folder and read project configuration
        # only at the main configuration
        if options is not None:
            main_log_dir = options.results_dir if options.results_dir is not None else self.get_system_config("results_dir")

            pool = None
            if eval(self.system_config.get('pool_analysis_enabled')):
                pool = self.system_config.get('pool_name')

            self.projects_generator = ProjectsGenerator(
                options.input_files,
                results_dir=main_log_dir,
                annotation_file=options.annotation_file,
                config_files=options.configuration_files,
                pool_name=pool)
            self.task_config.merge(ConfigObj(self.projects_generator.config))
            self.project_combination_generator = \
                ProjectGroupsGenerator(self.projects_generator.get_project_confs(),
                                       results_dir=main_log_dir
                )

            # Scheduler configuration specifications
            config_specs = ConfigObj()
            config_specs['jobs'] = "integer(default=None)"
            config_specs['queue'] = "string_list(default=None)"
            config_specs['__many__'] = {}
            config_specs['__many__']['cores'] = "integer(default=None)"
            config_specs['__many__']['queue'] = "string_list(default=None)"

            scheduler_config = ConfigObj(scheduler_file, interpolation='intogen', configspec=config_specs)
            # Validate configuration
            validator = Validator()
            scheduler_validation = scheduler_config.validate(validator, preserve_errors=True)

            if not scheduler_validation:
                for section, prop, error in flatten_errors(self.system_config, scheduler_validation):
                    logging.error("scheduler.conf file problem at {0} property '{1}' {2}".format(section, prop, error))
                exit(1)

            for scheduler_validation in get_extra_values(scheduler_config):
                logging.warning("Unknown scheduler.conf property '{0}' at {1}.".format(scheduler_validation[1], scheduler_validation[0]))

            # Create task executor
            self.executor = TaskExecutor(options, scheduler_config)

        # Validate configuration

        validator = Validator({
            "file": file_exist_validation,
            "dir": dir_exist_validation
        })

        system_validation = self.system_config.validate(validator, preserve_errors=True)
        self.validate_system_conf(system_validation)

        task_validation = self.task_config.validate(validator, preserve_errors=True)
        self.validate_task_conf(task_validation)

    def get_project_config(self, project: str, keys: str):

        value = get_nested(self.task_config, [project] + keys.split("."))

        if value is None:
            value = get_nested(self.task_config, keys.split("."))
            logging.debug("#CONF-TASK#\t{}: {} (DEFAULT value)".format(keys, value))
        else:
            logging.debug("#CONF-TASK#\t{}: {} ({} value)".format(keys, value, project))

        if value is None:
            logging.warning("#CONF-TASK# not found or is None: {} in {}".format(keys, project))

        return value

    def get_system_config(self, key):
        return self.system_config.get(key)

    def get_bulk_config(self, key_list):
        conf = {}
        key_list = list(key_list)
        key_list.sort()
        for key in key_list:
            value = self.system_config.get(key)
            conf[key] = value
            logging.info("#CONF#\t{}: {}".format(key, value))

        return conf

    def get_executor(self):
        return self.executor

    def get_projects_generator(self):
        return self.projects_generator

    def get_projects_combination_generator(self):
        return self.project_combination_generator


def dir_exist_validation(path_to_file):
    if os.path.exists(path_to_file) and os.path.isdir(path_to_file):
        return path_to_file
    else:
        raise ValidationError(path_to_file, "The path does not exist or is not a directory")


def file_exist_validation(path_to_file):
    if os.path.exists(path_to_file) and os.path.isfile(path_to_file):
        return path_to_file
    else:
        raise ValidationError(path_to_file, "The path does not exist or is not a file")


class ValidationError(VdtTypeError):
    def __init__(self, value, message):
        ValidateError.__init__(self, 'the value "{}" is wrong. {}'.format(value, message))


