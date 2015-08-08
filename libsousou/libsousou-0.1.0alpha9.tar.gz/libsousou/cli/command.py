import abc
import sys

from libsousou.cli.argument import Argument


class BaseCommand(metaclass=abc.ABCMeta):
    """Base class for all commands handled by :class:`~libsousou.cli.BaseParser`."""

    #: The description of the command on the command-line help.
    description = None

    #: A list of :class:`libsousou.cli.Argument` instances specifying default arguments
    #: of the command.
    default_args = None

    #: A list of :class:`libsousou.cli.Argument` instances specifying the arguments
    #: of the commands.
    args = None

    #: Specifies the help text of the command.
    help_text = None

    #: Describes usage information that will be displayed with sub-command help,
    #: by default the name of the program and any positional arguments before
    #: the subparser argument.
    prog = None

    @property
    def arguments(self):
        return (tuple(self.args or [])) + tuple(self.default_args or [])

    @abc.abstractproperty
    def command_name(self):
        """Specifies the name of the command. Must be unique within a Python
        process."""
        raise NotImplementedError

    def __init__(self):
        self._parser = None

    def execute(self, args):
        self.handle(args)
        return 0

    @abc.abstractmethod
    def handle(self, args):
        """Handles the command.

        Args:
            args: the parsed command line arguments.
        """

    def add_to_subparsers(self, subparsers):
        """Add the command to subparsers."""
        args = [self.command_name]
        kwargs = {}
        if self.help_text:
            kwargs['help'] = self.help_text
        if self.prog:
            kwargs['prog'] = self.prog
        self._parser = subparsers.add_parser(*args, **kwargs)
        for arg in self.arguments:
            Argument.add_to_subparser(arg, self._parser)
        self._parser.set_defaults(func=self.execute)
