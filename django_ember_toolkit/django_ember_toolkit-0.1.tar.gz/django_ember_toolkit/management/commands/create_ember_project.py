import subprocess

from django.conf import settings

from ._base import EmberCommand


class Command(EmberCommand):
    help = 'Generate a new Ember app for use with your Django project'

    def handle(self, *args, **options):
        self.assert_required_settings('EMBER_APP_NAME')

        self.notify(
            'Generating new Ember project at: \n' +
            self.get_full_ember_path())

        # create the project using ember-cli
        subprocess.check_call(
            [
                'ember', 'new', self.get_setting('EMBER_APP_NAME'),
                '--dir', self.get_full_ember_path()
            ],
            cwd=settings.BASE_DIR)

        # install and scaffold the Ember adapter for Django REST Framework
        self.run_ember_command('install', 'ember-django-adapter')

        self.run_ember_command('generate', 'drf-adapter', 'application')
        self.run_ember_command('generate', 'drf-serializer', 'application')

        # install the modified config file
        self.write_initial_config()
