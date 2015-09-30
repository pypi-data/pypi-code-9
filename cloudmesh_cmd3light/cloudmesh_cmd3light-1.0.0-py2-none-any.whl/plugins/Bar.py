from __future__ import print_function
from cloudmesh_cmd3light.command import command


from cloudmesh_cmd3light.command import command, Cmd3Command
from cloudmesh_cmd3light.console import Console

class BarCommand(Cmd3Command):

    topics = {"bar": "example"}

    def __init__(self, context):
        self.context = context
        if self.context.debug:
            print("init Bar")

    @command
    def do_bar(self, arg, arguments):
        """
        ::

          Usage:
                bar -f FILE
                bar FILE
                bar list

          This command does some useful things.

          Arguments:
              FILE   a file name

          Options:
              -f      specify the file

        """
        print(arguments)
