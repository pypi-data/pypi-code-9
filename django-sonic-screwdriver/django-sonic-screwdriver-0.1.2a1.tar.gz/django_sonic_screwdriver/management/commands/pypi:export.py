from subprocess import call
from optparse import make_option
from django.core.management.base import BaseCommand


class Command(BaseCommand):

	help = 'Tag your project.'

	option_list = BaseCommand.option_list + (
		make_option('--upload', '-u', action='store_true', dest='upload', default=False,
					help=''),
	)

	def handle(self, *args, **options):
		call(['python', 'setup.py', 'sdist', 'bdist_wheel', 'upload'])

		if options['upload']:
			call(['python', 'setup.py', 'sdist', 'bdist_wheel', 'upload'])
