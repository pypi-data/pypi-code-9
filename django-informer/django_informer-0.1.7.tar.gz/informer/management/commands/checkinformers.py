# coding: utf-8

"""django informer commands"""

from django.conf import settings
from django.core.management.base import BaseCommand

from informer.checker.base import BaseInformer, InformerException


class Command(BaseCommand):
    help = 'Check all Informers.'

    def add_arguments(self, parser):
        parser.add_argument(
            'informers',
            nargs='*',
            help='Provide one (or more) Informer names to check.')

        parser.add_argument(
            '--list',
            action='store_true',
            dest='list',
            default=False,
            help='All Informers that appear in the settings.')

    def _get_informers(self, names):
        """
        Get a list from informers
        """
        DJANGO_INFORMERS = getattr(settings, 'DJANGO_INFORMERS', ())

        if not names:
            return DJANGO_INFORMERS

        result = []

        for name in names:
            result += [i for i in DJANGO_INFORMERS if name in i]

        return result

    def handle(self, *args, **options):
        self.stdout.write(' Django Informer Management Command')
        self.stdout.write('-' * 79)
        self.stdout.write(' Get informations from each Informer.\n\n')
        self.stdout.write(
            ' For a complete help and documentation, visit '
            'http://github.com/rodrigobraga/informer.')

        DJANGO_INFORMERS = getattr(settings, 'DJANGO_INFORMERS', ())

        if not DJANGO_INFORMERS:
            self.stdout.write('\n No informer was found.')
            self.stdout.write('-' * 79)
            self.stdout.write(' Missing configuration. ')

            return

        if options['list']:
            self.stdout.write(
                '\n Below the informers that appear in settings.')
            self.stdout.write('-' * 79)

            for namespace, classname in DJANGO_INFORMERS:
                self.stdout.write(' %s.%s' % (namespace, classname))

            return

        names = options['informers']

        informers = self._get_informers(names)

        self.stdout.write('\n Checking Informers.')
        self.stdout.write('-' * 79)

        output = '\t Checking {0}... {1}'

        for namespace, classname in informers:
            try:
                cls = BaseInformer.get_class(namespace, classname)
                informer = cls()

                operational, message = informer.check()
            except InformerException as error:
                self.stderr.write(output.format(classname, error))
            except Exception as error:
                self.stderr.write('A generic exception occurred: %s' % error)
            else:
                self.stdout.write(output.format(classname, message))
