#!/usr/bin/env python


from cleo import Command, InputArgument, InputOption
from cleo import Application
from probe.utils import h5_walk
import sys

class H5WalkCommand(Command):
	name = 'utils:h5_walk'

	description = 'Walks throught directories and prints information about h5-files'

	arguments = []

	options = [
        {
            'name': 'path',
            'shortcut': 'p',
            'description': 'Name of directory where function starts its searching',
            'value_required': False,
            'default': ".",
        }
		,{
		    "name": "filename",
			"shortcut": "f",
			"description": "Name of file to write csv-table in",
			"value_required": False,
			"default": sys.stdout,
		}
	]

	@staticmethod
	def execute(i, o):
		path = i.get_option('path')
		filename = i.get_option("filename")
		h5_walk(path=path, filename=filename)

if __name__ == '__main__':
    application = Application()
    application.add(H5WalkCommand())
    application.run()
