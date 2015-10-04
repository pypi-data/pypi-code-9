from django.core.management.base import BaseCommand
from django.conf import settings

from garelay.server import tasks
from garelay.tracker.models import TrackingEvent


class Command(BaseCommand):
    help = 'Register events with Google Analytics.'

    def handle(self, *args, **kwargs):
        events = TrackingEvent.objects.all().exclude(status='registered')
        self.stdout.write('Registering %s events in batches of %s.\n' % (
            events.count(),
            settings.GARELAY_REGISTER_BATCH_SIZE))
        tasks.register_events()
        self.stdout.write('Done.\n')
