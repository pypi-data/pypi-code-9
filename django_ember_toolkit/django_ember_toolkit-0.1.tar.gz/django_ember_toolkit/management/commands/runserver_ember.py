import os
import subprocess

from django.conf import settings
from django.core.management import call_command

from ._base import EmberCommand


class Command(EmberCommand):
    help = 'Generate a new Ember app for use with your Django project'

    def handle(self, *args, **options):
        call_command('generate_ember_config')

        self.notify('Running server at {}, UI at {}'.format(
            'http://localhost:8000',
            'http://localhost:4200'))
        django_process = subprocess.Popen(
            ['./manage.py', 'runserver'],
            cwd=settings.BASE_DIR)
        ember_process = subprocess.Popen(
            ['ember', 'serve', '--proxy', 'http://localhost:8000'],
            cwd=self.get_full_ember_path())

        django_process.wait()
        ember_process.kill()
