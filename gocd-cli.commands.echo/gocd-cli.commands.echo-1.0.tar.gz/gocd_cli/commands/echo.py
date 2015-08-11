from __future__ import print_function
from gocd_cli.command import BaseCommand

__all__ = ['Echo']
__version__ = '1.0'


class Echo(BaseCommand):
    usage = ' '
    usage_summary = 'Will print the passed in string to standard out.'

    def __init__(self, server, string):
        self.server = server
        self.output = string

    def run(self):
        print(self.output)
