from __future__ import print_function
import spex
import argparse
from argparse import _HelpAction, _SubParsersAction, Namespace
import multiprocessing


class SplitValues(argparse.Action):
    def __init__(self, option_strings, dest, **kwargs):
        if 'default' not in kwargs:
            kwargs['default'] = []
        super(SplitValues, self).__init__(option_strings, dest, **kwargs)

    def __call__(self, _parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values.split(','))


class ConfAction(argparse.Action):
    def __init__(self, option_strings, dest, **kwargs):
        if 'default' not in kwargs:
            kwargs['default'] = {}
        super(ConfAction, self).__init__(option_strings, dest, **kwargs)

    def __call__(self, _parser, namespace, values, option_string=None):
        key, value = values.split('=')
        if not hasattr(namespace, self.dest):
            setattr(namespace, self.dest, dict(key=value))
        else:
            getattr(namespace, self.dest)[key] = value


class NamespacingParser(argparse.ArgumentParser):
    def parse_args(self, *args, **kw):
        res = argparse.ArgumentParser.parse_args(self, *args, **kw)
        for sub_parser in self._subparsers._actions:  # noqa
            if not isinstance(sub_parser, _SubParsersAction):
                continue
            values = sub_parser.choices[res.entrypoint]
            subparseargs = {}
            for action in values._optionals._actions:  # noqa
                if isinstance(action, _HelpAction):
                    continue
                args = action.dest
                if hasattr(res, args): # pop the argument
                    subparseargs[args] = getattr(res, args)
                    delattr(res, args)
            res.application_args = Namespace(**subparseargs)
        return res


def add_parser_options(parser, defaults=None):
    defaults = defaults if defaults is not None else {}

    parser.add_argument('--files',
                        dest='files',
                        action=SplitValues,
                        help='Comma-separated list of files to be placed in the working directory of each executor')

    parser.add_argument('--jars',
                        dest='jars',
                        action=SplitValues,
                        help='Comma-separated list of local jars to include on the driver')

    parser.add_argument('--py-files',
                        dest='py_files',
                        action=SplitValues,
                        help='Comma-separated list of .zip, .egg, or .py files to place')

    parser.add_argument('--master',
                        dest='master',
                        default=defaults.get('master', 'local[%d]' % multiprocessing.cpu_count()),
                        help='The spark master uri, typically one of local[<cores>], mesos://zk://quorum')

    parser.add_argument('--name',
                        dest='name',
                        default=defaults.get('name', parser.prog),
                        help='The name of your application')

    parser.add_argument('--conf',
                        dest='conf',
                        action=ConfAction,
                        help='Arbitrary Spark configuration properties as PROP=VALUE pairs')

    parser.add_argument('--executor-memory',
                        dest='executor_memory',
                        default=defaults.get('executor_memory', '1g'),
                        help='Memory per executor (e.g. 1000M, 2G)')

    parser.add_argument('--spark-home',
                        dest='spark_home',
                        help='The location of the spark home to use, can be provided as SPARK_HOME')

    parser.add_argument('--total-executor-cores',
                        dest='total_executor_cores',
                        default=defaults.get('total_executor_cores', 8),
                        type=int,
                        help='Total number of cores to use in coarse grained mode')

    parser.add_argument('--verbose',
                        dest='verbose',
                        default=defaults.get('verbose', False),
                        action='store_true',
                        help='Print additional debug output')

    parser.add_argument('--version',
                        dest='version',
                        default=False,
                        action='version',
                        version=spex.__version__,
                        help='Print out the version and exit')

    parser.add_argument('--driver-memory',
                        dest='driver_memory',
                        default=defaults.get('driver_memory', '1g'),
                        help='Memory for driver (e.g. 1000M, 2G)')

    parser.add_argument('--coarse-mode',
                        dest='coarse_mode',
                        action='store_true',
                        default=defaults.get('coarse_mode', True),
                        help='Run the given PySpark application in coarse grained mode (default)')

    parser.add_argument('--fine-mode',
                        dest='coarse_mode',
                        action='store_false',
                        help='Run the given PySpark application in fine grained mode')

    parser.add_argument('--task-cpus',
                        dest='task_cpus',
                        default=defaults.get('task_cpus', 4),
                        type=int,
                        help='The number of CPUs each task requires')

    parser.add_argument('--local-dir',
                        dest='local_dir',
                        default=defaults.get('local_dir', None),
                        help='The temp / scratch directory PySpark will use')

    parser.add_argument('--event-log',
                        dest='event_log',
                        default=defaults.get('event_log', None),
                        help='Store the spark event log for future analysis')

    parser.add_argument('--python-mem-ratio',
                        dest='python_mem_ratio',
                        default=defaults.get('python_mem_ratio', 0.5),
                        type=float,
                        help='The amount of memory to take from the executor memory '
                             'and give to Python surrogate processes')


def create_parser(entry_points, bootstrap_spex_config):
    parser = NamespacingParser(description='PySpark bundled project', prog=bootstrap_spex_config.spex_name)
    add_parser_options(parser, bootstrap_spex_config.spark_config._asdict())

    parser.add_argument('-m', dest='_module', action='store_true')
    parser.set_defaults(**bootstrap_spex_config.spark_config._asdict())

    subparsers = parser.add_subparsers(title='commands', dest='entrypoint')
    for name, entry_point in entry_points.items():
        subparser = subparsers.add_parser(name, help=entry_point.help())
        entry_point.configure_arg_parser(subparser)
        subparser.set_defaults(application=entry_point)

    return parser
