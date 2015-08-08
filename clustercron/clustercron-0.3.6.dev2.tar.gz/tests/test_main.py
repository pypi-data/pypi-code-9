"""
Tests for `clustercron` module.
"""

from __future__ import print_function
from __future__ import unicode_literals
import logging
import pytest
from clustercron import elb
from clustercron import main


def test_clustercron_returns_None_when_lb_type_is_not_elb():
    '''
    Test if `main.clustercron` returns None when `lb_type` is not 'elb'.
    '''
    assert main.clustercron('really_not_elb', 'mylbname', 'command') == None


def test_clustercron_returns_2_when_master_and_command_exits_2(monkeypatch):
    '''
    Test if `main.clustercron` returns 2 when `lb.master` and command exits
    with 2.
    '''
    class ElbMock(object):
        def __init__(self, name):
            self.master = True

    class PopenMock(object):
        def __init__(self, command, stdout, stderr):
            self.returncode = 2

        def communicate(self):
            return (None, None)

    monkeypatch.setattr(elb, 'Elb', ElbMock)
    monkeypatch.setattr('subprocess.Popen', PopenMock)

    assert main.clustercron('elb', 'mylbname', 'a_command') == 2


def test_clustercron_returns_0_when_master_and_command_is_none(monkeypatch):
    '''
    Test if `main.clustercron` returns 0 when `lb.master` and `command` is
    None.
    '''
    class ElbMock(object):
        def __init__(self, name):
            self.master = True

    monkeypatch.setattr(elb, 'Elb', ElbMock)

    assert main.clustercron('elb', 'mylbname', None) == 0


def test_clustercron_returns_1_when_not_master(monkeypatch):
    '''
    Test if `main.clustercron` returns 1 when not `lb.master`
    '''
    class ElbMock(object):
        def __init__(self, name):
            self.master = False

    monkeypatch.setattr(elb, 'Elb', ElbMock)

    assert main.clustercron('elb', 'mylbname', None) == 1


def test_Optarg_init():
    opt_arg_parser = main.Optarg([])
    assert opt_arg_parser.arg_list == []
    assert opt_arg_parser.args == {
        'version': False,
        'help': False,
        'verbose': 0,
        'lb_type': None,
        'lb_name': None,
        'command': [],
        'syslog': False,
    }


def test_opt_arg_parser_usage():
    opt_arg_parser = main.Optarg([])
    assert opt_arg_parser.usage == '''usage:
    clustercron [options] elb <loadbalancer_name> [<cron_command>]
    clustercron --version
    clustercron (-h|--help)

    options:
        (-v|--verbose)  Info logging. Add extra `-v` for debug logging.
        (-s|--syslog)   Log to (local) syslog.

Clustercron is cronjob wrapper that tries to ensure that a script gets run
only once, on one host from a pool of nodes of a specified loadbalancer.

Without specifying a <cron_command> clustercron will only check if the node
is the `master` in the cluster and will return 0 if so.
'''


@pytest.mark.parametrize('arg_list,args', [
    (
        [],
        {
            'version': False,
            'help': False,
            'verbose': 0,
            'lb_type': None,
            'lb_name': None,
            'command': [],
            'syslog': False,
        }
    ),
    (
        ['-h'],
        {
            'version': False,
            'help': True,
            'verbose': 0,
            'lb_type': None,
            'lb_name': None,
            'command': [],
            'syslog': False,
        }
    ),
    (
        ['whatever', 'nonsense', 'lives', 'here', '-h'],
        {
            'version': False,
            'help': True,
            'verbose': 0,
            'lb_type': None,
            'lb_name': None,
            'command': [],
            'syslog': False,
        }
    ),
    (
        ['--help'],
        {
            'version': False,
            'help': True,
            'verbose': 0,
            'lb_type': None,
            'lb_name': None,
            'command': [],
            'syslog': False,
        }
    ),
    (
        ['--help', 'whatever', 'nonsense', 'lives', 'here'],
        {
            'version': False,
            'help': True,
            'verbose': 0,
            'lb_type': None,
            'lb_name': None,
            'command': [],
            'syslog': False,
        }
    ),
    (
        ['--version'],
        {
            'version': True,
            'help': False,
            'verbose': 0,
            'lb_type': None,
            'lb_name': None,
            'command': [],
            'syslog': False,
        }
    ),
    (
        ['whatever', 'nonsense', '--version', 'lives', 'here', 'elb'],
        {
            'version': True,
            'help': False,
            'verbose': 0,
            'lb_type': None,
            'lb_name': None,
            'command': [],
            'syslog': False,
        }
    ),
    (
        ['-v', 'elb', 'my_lb_name', 'update', '-r', 'thing'],
        {
            'version': False,
            'help': False,
            'verbose': 1,
            'lb_type': 'elb',
            'lb_name': 'my_lb_name',
            'command': ['update', '-r', 'thing'],
            'syslog': False,
        }
    ),
    (
        ['-v', '-v', 'elb', 'my_lb_name', 'update', '-r', 'thing'],
        {
            'version': False,
            'help': False,
            'verbose': 2,
            'lb_type': 'elb',
            'lb_name': 'my_lb_name',
            'command': ['update', '-r', 'thing'],
            'syslog': False,
        }
    ),
    (
        ['elb', 'my_lb_name', 'update', '-r', 'thing'],
        {
            'version': False,
            'help': False,
            'verbose': 0,
            'lb_type': 'elb',
            'lb_name': 'my_lb_name',
            'command': ['update', '-r', 'thing'],
            'syslog': False,
        }
    ),
    (
        ['elb', 'my_lb_name'],
        {
            'version': False,
            'help': False,
            'verbose': 0,
            'lb_type': 'elb',
            'lb_name': 'my_lb_name',
            'command': [],
            'syslog': False,
        }
    ),
    (
        ['elb'],
        {
            'version': False,
            'help': False,
            'verbose': 0,
            'lb_type': 'elb',
            'lb_name': None,
            'command': [],
            'syslog': False,
        }
    ),
    (
        ['elb', '-v'],
        {
            'version': False,
            'help': False,
            'verbose': 0,
            'lb_type': 'elb',
            'lb_name': None,
            'command': [],
            'syslog': False,
        }
    ),
    (
        ['elb', 'my_lb_name', '-v'],
        {
            'version': False,
            'help': False,
            'verbose': 0,
            'lb_type': 'elb',
            'lb_name': 'my_lb_name',
            'command': [],
            'syslog': False,
        }
    ),
    (
        ['-v', '-v', '-s', 'elb', 'my_lb_name', 'test', '-v'],
        {
            'version': False,
            'help': False,
            'verbose': 2,
            'lb_type': 'elb',
            'lb_name': 'my_lb_name',
            'command': ['test', '-v'],
            'syslog': True,
        }
    ),
])
def test_opt_arg_parser(arg_list, args):
        print(arg_list)
        optarg = main.Optarg(arg_list)
        optarg.parse()
        assert optarg.args == args


def test_command_version(monkeypatch):
    '''
    Test if `cluster.command` returns 2 with '--version'
    '''
    monkeypatch.setattr('sys.argv', ['clustercron', '--version'])
    assert main.command() == 2


def test_command_elb_lb_name_a_command_arguments(monkeypatch):
    '''
    Test if `cluster.command` returns 1 with 'elb', 'lb_name' and 'a_command'
    arguments.
    '''
    monkeypatch.setattr(
        'sys.argv',
        ['clustercron', 'elb', 'lb_name', 'a_command']
    )
    monkeypatch.setattr(
        main,
        'clustercron',
        lambda lb_type, lb_name, commmand: 0
    )
    assert main.command() == 0


def test_command_nosense(monkeypatch):
    monkeypatch.setattr(
        'sys.argv',
        ['clustercron', 'bla', 'ara', 'dada', '-r', 'thing'],
    )
    assert main.command() == 3


@pytest.mark.parametrize(
    'verbose,syslog,log_level',
    [
        (0, False, logging.ERROR),
        (1, False, logging.INFO),
        (2, False, logging.DEBUG),
        (0, True, logging.ERROR),
        (1, True, logging.INFO),
        (2, True, logging.DEBUG),

    ]
 )
def test_setup_logging_level(verbose, syslog, log_level):
    main.setup_logging(verbose, syslog)
    logger = logging.getLogger()
    assert logger.handlers[0].level == log_level
