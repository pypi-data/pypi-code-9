from django.core.management.base import BaseCommand, CommandError
from lisa_api.lisa.configuration import CONF
from django.conf import settings
from django.utils.translation import ugettext as _


class Command(BaseCommand):
    help = _('Handle the lisa api configuration file')

    def add_arguments(self, parser):
        parser.add_argument('--save',
                            action='store_true',
                            dest='save',
                            default=False,
                            help=_('Filename where the configuration will be saved'))

        parser.add_argument('--filename',
                            dest='filename',
                            default=settings.BASE_DIR + '/lisa_api.ini',
                            help=_('Save the configuration of lisa'))

    def handle(self, *args, **options):
        if options['save']:
            CONF.save(filename=options['filename'])
            self.stdout.write(_('Successfully saved the configuration'))
        else:
            raise CommandError(_('You must specify an option and a filename. Check the help'))
