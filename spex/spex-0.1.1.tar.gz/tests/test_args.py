import pytest

import spex
from spex.args import create_parser
from spex.entrypoint import get_entry_points, DaemonApplication
from spex.config import SpexConfig, SparkConfig


_BOOTSTRAP_CONFIG = SpexConfig(
    spex_name='bootstrap',
    spex_root='spex_root',
    spex_file='spex_file',
    spex_conf='spex_conf',
    entry_point='entry_point',
    spark_distro='spark_distro',
    spark_config=SparkConfig(
        files=[],
        jars=[],
        py_files=[],
        master='local[1]',
        name='name',
        conf={},
        executor_memory='1g',
        spark_home='spark_home',
        total_executor_cores=10,
        verbose=False,
        driver_memory='1g',
        coarse_mode=True,
        task_cpus=4,
        local_dir='local_dir',
        event_log=None,
        python_mem_ratio=0.5,
    )
)


def parse(args, entry_points=None, bootstrap_config=None):
    entry_points = entry_points if entry_points else get_entry_points()
    bootstrap_config = bootstrap_config if bootstrap_config else _BOOTSTRAP_CONFIG
    parser = create_parser(entry_points, bootstrap_config)
    return parser.parse_args(args)


def a(arg_str, defaulted=('driver', '/not/a/file')):
    args = arg_str.split()
    if defaulted:
        args += defaulted
    return args


def test_driver():
    args = parse(a(''))
    assert args.application != DaemonApplication, 'The driver mode is not set'
    assert args.application_args.scripts == ['/not/a/file']


def test_daemon():
    args = parse(a('-m pyspark.daemon', defaulted=()))
    assert args.application == DaemonApplication, 'Should be in daemon mode'


def test_spark_home():
    args = parse(a(''))
    assert args.spark_home == 'spark_home'

    args = parse(a('--spark-home /this/is/a/test'))
    assert args.spark_home == '/this/is/a/test'

def test_master():
    args = parse(a(''))
    assert args.master == 'local[1]'

    args = parse(a('--master=mesos://zk://test'))
    assert args.master == 'mesos://zk://test'


def test_executor_mem():
    args = parse(a(''))
    assert args.executor_memory == '1g'

    args = parse(a('--executor-memory=8g'))
    assert args.executor_memory == '8g'


def test_driver_mem():
    args = parse(a(''))
    assert args.driver_memory == '1g'

    args = parse(a('--driver-memory=10g'))
    assert args.driver_memory == '10g'


def test_name():
    args = parse(a(''))
    assert args.name == 'name'

    args = parse(a('--name test-app'))
    assert args.name == 'test-app'


def test_jars():
    args = parse(a(''))
    assert args.jars == []

    args = parse(a('--jars test1.jar'))
    assert args.jars == ['test1.jar']

    args = parse(a('--jars test1.jar,test2.jar'))
    assert args.jars == ['test1.jar', 'test2.jar']


def test_files():
    args = parse(a(''))
    assert args.files == []

    args = parse(a('--files test1.file'))
    assert args.files == ['test1.file']

    args = parse(a('--files test1.file,test2.file'))
    assert args.files == ['test1.file', 'test2.file']


def test_pyfiles():
    args = parse(a(''))
    assert args.py_files == []

    args = parse(a('--py-files test1.file'))
    assert args.py_files == ['test1.file']

    args = parse(a('--py-files test1.file,test2.file'))
    assert args.py_files == ['test1.file', 'test2.file']


def test_version(capsys):
    with pytest.raises(SystemExit) as exit:
        parse(a('--version'))
        assert exit.code == 0

        out, err = capsys.readouterr()
        assert out == spex.__version__


def test_help(capsys):
    with pytest.raises(SystemExit) as exit:
        parse(a('--help'))
        assert exit.code == 0

        out, err = capsys.readouterr()
        assert 'usage' in out


def test_coarse_mode():
    args = parse(a(''))
    assert args.coarse_mode

    args = parse(a('--coarse-mode'))
    assert args.coarse_mode

    args = parse(a('--fine-mode'))
    assert not args.coarse_mode


def test_verbose():
    args = parse(a(''))
    assert not args.verbose

    args = parse(a('--verbose'))
    assert args.verbose


def test_num_cores():
    args = parse(a(''))
    assert args.total_executor_cores == 10

    args = parse(a('--total-executor-cores 32'))
    assert args.total_executor_cores == 32


def test_conf_option():
    args = parse(a(''))
    assert args.conf == {}

    args = parse(a('--conf test=othervalue --conf spark.io.compression.codec=lz4'))
    assert args.conf == {'test': 'othervalue', 'spark.io.compression.codec': 'lz4'}

    args = parse(a('--conf test=value'))
    assert args.conf['test'] == 'value'

    args = parse(a('--conf spark.io.compression.codec=snappy'))
    assert args.conf['spark.io.compression.codec'] == 'snappy'


def test_cpus_per_task():
    args = parse(a(''))
    assert args.task_cpus == 4

    args = parse(a('--task-cpus 16'))
    assert args.task_cpus == 16


def test_local_dir():
    args = parse(a(''))
    assert args.local_dir == 'local_dir'

    args = parse(a('--local-dir /some/where/else'))
    assert args.local_dir == '/some/where/else'


def test_event_log():
    args = parse(a(''))
    assert args.event_log is None

    args = parse(a('--event-log hdfs://urx/event/logs'))
    assert args.event_log == 'hdfs://urx/event/logs'


def test_python_mem():
    args = parse(a(''))
    assert args.python_mem_ratio == 0.5

    args = parse(a('--python-mem-ratio 0.9'))
    assert args.python_mem_ratio == 0.9


def test_application_parser():
    args = parse(a(''))
    assert args.application_args.scripts == ['/not/a/file']
    assert args.application
    print args.application
    assert not hasattr(args, 'script')
