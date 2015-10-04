from django.core.management.base import BaseCommand
from django.conf import settings

from garelay.tracker import tasks
from garelay.tracker.models import TrackingEvent


class Command(BaseCommand):
    help = 'Relay events to the configured GARELAY_SERVER.'

    def handle(self, *args, **kwargs):
        events = TrackingEvent.objects.filter(
            status='captured').exclude(status='relayed')
        self.stdout.write('Relaying %s events in batches of %s.\n' % (
            events.count(),
            settings.GARELAY_RELAY_BATCH_SIZE))
        tasks.relay_events()
        self.stdout.write('Done.\n')
