import argparse
import sys

from libsousou.module_loading import import_string



class ParserExit(Exception):
    pass


def exit_parser(exitcode, *args, **kwargs):
    raise ParserExit(exitcode, *args)


class BaseParser(object):
    """
    Command-line argument parser base class that registers all
    subcommands.
    """

    def __init__(self, program_name="", exit=sys.exit):
        self._parser = argparse.ArgumentParser() if not program_name\
            else argparse.ArgumentParser(program_name)
        self._subparsers = self._parser.add_subparsers(dest="subparser_name")
        self._exit = lambda x, *a, **kw: exit

        # This is a hack. The ArgumentParser invokes its exit() method
        # if the command-parsing failed. But *we* want to decide wether
        # to exit the current interpreter or not.
        self._parser.exit = exit_parser

    def run_from_command_line(self, *args, **kwargs):
        """Run a command with the specified command-line arguments."""
        # Note that the return value is only useful when something else
        # than sys.exit was passed to BaseParser.__init__
        try:
            self.run(*args, **kwargs)
            return self._exit(0)
        except ParserExit as e:
            return self._exit(*e.args)

    def run(self, *args, **kwargs):
        """Execute the command identified by a list holding the command-line
        parameters.
        """
        args = self.parse_args(*args, **kwargs)
        return args.func(args)

    def register_commands(self, command_list):
        """Registers commands to the base parser.

        Args:
            command_list: a list of strings specifying the dotted
                path to modules holding commands.

        Returns:
            None
        """
        for module_path in command_list:
            Command = import_string(module_path + '.Command')
            self.add_command(Command)

    def add_command(self, command_class):
        """Adds a command to the parser."""
        command = command_class()
        command.add_to_subparsers(self._subparsers)

    def parse_args(self, *args, **kwargs):
        return self._parser.parse_args(*args, **kwargs)


parser = BaseParser()
