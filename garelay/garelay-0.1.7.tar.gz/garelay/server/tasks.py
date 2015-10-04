from django.conf import settings

from garelay import celery_app
from garelay.tracker.models import TrackingEvent


@celery_app.task(ignore_result=True)
def register_events():
    # Limit to 1000 requests registered at GA per minute.
    # That's roughly 16 per scond
    events = TrackingEvent.objects.all().exclude(status='registered')
    for event in events[:settings.GARELAY_REGISTER_BATCH_SIZE]:
        event.register()
        event.save()
