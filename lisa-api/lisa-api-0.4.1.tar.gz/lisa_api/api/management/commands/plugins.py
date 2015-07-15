from django.core.management.base import BaseCommand, CommandError
from cookiecutter.main import cookiecutter
from django.utils.translation import ugettext as _


class Command(BaseCommand):
    help = _('Handle the plugin creation')

    def add_arguments(self, parser):
        parser.add_argument('--create',
                            dest='create',
                            action='store_true',
                            help=_('Create a plugin'))

    def handle(self, *args, **options):
        if options['create']:
            cookiecutter('https://github.com/project-lisa/cookiecutter-lisa-plugins.git')
            self.stdout.write(_('Successfully created the plugin'))
        else:
            raise CommandError(_('You must specify an option'))
