from django.conf import settings
from django.utils.module_loading import import_module
from django.core.management.base import BaseCommand
from fontforge_watcher import FontforgeWatcher

class Command(BaseCommand):
    args = ''
    help = 'ex: ./manage.py fontforge_watcher'

    def handle(self, *args, **options):

        watcher = FontforgeWatcher(command=self)
        watcher.watch()