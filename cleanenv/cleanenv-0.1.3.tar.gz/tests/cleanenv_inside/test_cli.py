from argparse import ArgumentParser
from flexmock import flexmock

from cleanenv.cleanenv_inside import cli
from cleanenv.commands import create
from cleanenv.cleanenv_inside.commands import exec_


def test_standalone_command_main():
    flexmock(ArgumentParser) \
        .should_receive('parse_args') \
        .and_return(flexmock(environment_path='/env'))
    flexmock(exec_).should_receive('run_command')

    cli.standalone_command_main(exec_)


def test_main():
    flexmock(ArgumentParser) \
        .should_receive('parse_args') \
        .and_return(flexmock(command='create'))

    flexmock(create).should_receive('add_command_line_arguments')
    flexmock(create).should_receive('run_command')

    cli.main()


def test_get_plugin():
    class NoCommandPlugin(object):
        pass
    plugin = cli._get_plugin(NoCommandPlugin)
    assert not plugin

    class NoCommandPlugin2(object):
        add_command_line_arguments = lambda: None
    plugin = cli._get_plugin(NoCommandPlugin2)
    assert not plugin

    class CommandPlugin(object):
        add_command_line_arguments = lambda: None
        run_command = lambda: None
    plugin = cli._get_plugin(CommandPlugin)
    assert plugin

    class CommandEnvironmentPlugin(CommandPlugin):
        NEEDS_ENVIRONMENT = True
    plugin = cli._get_plugin(CommandEnvironmentPlugin)
    assert plugin
