from __future__ import print_function
import os
import sys

from builtins import input
from cloudmesh_cmd3light.command import command, Cmd3Command
from cloudmesh_cmd3light.console import Console


class CommandsCommands(Cmd3Command):

    topics = {"commands": "shell"}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print("init command commands")

            # self.register_command_topic('cloud', 'admin')

    @command
    def do_commands(self, arg, arguments):
        """
        ::

            Usage:
                commands

            Prints all registered commands
        """
        print (arguments)
        print (vars())

        names  = [cls.__name__ for cls in Cmd3Command.__subclasses__()]

        classes  = [cls for cls in Cmd3Command.__subclasses__()]

        name_list = '\n'.join(names)

        Console.ok("Registered Commands")
        Console.ok("===================")
        for name in names:
            Console.ok(name)
        print()

        Console.ok("Registered Classes")
        Console.ok("===================")
        for c in classes:
            Console.ok(str(c))

