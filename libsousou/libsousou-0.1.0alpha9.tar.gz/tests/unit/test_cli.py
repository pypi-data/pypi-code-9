import unittest

from libsousou.cli.baseparser import BaseParser
from libsousou.cli.test import Command as TestCommand


class CommandLineInterfaceTestCase(unittest.TestCase):

    def setUp(self):
        self.parser = BaseParser(exit=lambda x, *a, **kw: x)
        self.parser.add_command(TestCommand)
        self.args = ['testcommand', 'foo','--named','bar']

    def test_run(self):
        # Invoke run and assert that TestCommand.executed
        # is True.
        self.parser.run(self.args)
        self.assertTrue(TestCommand.executed)

    def test_run_from_command_line(self):
        # Invoke run_from_command_line and assert that TestCommand.executed
        # is True.
        self.parser.run_from_command_line(self.args)
        self.assertTrue(TestCommand.executed)

    def test_non_existing_subcommand_exits_nonzero(self):
        # Invoke run_from_command_line with a non existing command name.
        # It must produce a nonzero exit code.
        exitcode = self.parser.run_from_command_line(['foo'])
        self.assertNotEqual(exitcode, 0)

    def test_register_commands(self):
        # Invoke the register_commands method and assert that the TestCommand
        # may be invoked.
        parser = BaseParser(exit=lambda x, *a, **kw: x)
        parser.register_commands(
            ['.'.join([TestCommand.__module__])]
        )


if __name__ == '__main__':
    unittest.main()
