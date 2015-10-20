import logging
from datetime import timedelta

from django.conf import settings
from django.utils import timezone

from garelay import celery_app
from garelay.tracker.models import TrackingEvent


@celery_app.task(ignore_result=True)
def cleanup_events():
    events = TrackingEvent.objects.all().filter(
        created_at__lte=timezone.now() - timedelta(
            seconds=settings.GARELAY_EVENT_EXPIRY))
    captured_event_count = events.filter(status='captured').count()
    relayed_event_count = events.filter(status='relayed').count()
    if captured_event_count or relayed_event_count:
        logging.warning(
            'Cleaning up %s captured and %s relayed events.' % (
                captured_event_count, relayed_event_count,))
    events.delete()
