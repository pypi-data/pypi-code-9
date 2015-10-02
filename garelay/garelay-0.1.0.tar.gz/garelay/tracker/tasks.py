import json

from django.conf import settings
from django.utils import timezone
from django.core.serializers.json import DjangoJSONEncoder

from garelay import celery_app
from garelay.tracker.models import TrackingEvent

import requests


@celery_app.task(ignore_result=True)
def relay_events():
    pending_events = TrackingEvent.objects.filter(
        status='captured').exclude(status='relayed')
    while pending_events.exists():
        next_batch = pending_events[:settings.GARELAY_RELAY_BATCH_SIZE]
        payload = [event.to_dict() for event in next_batch]
        response = requests.post(
            settings.GARELAY_SERVER,
            auth=settings.GARELAY_CREDENTIALS,
            data=json.dumps(payload, cls=DjangoJSONEncoder),
            headers={
                'content-type': 'application/json',
                'accept': 'application/json',
            },
            timeout=settings.GARELAY_RELAY_TIMEOUT)
        # This will kill the task if we don't have Internet connectivity
        response.raise_for_status()
        uuids = [event['uuid'] for event in response.json()]
        TrackingEvent.objects.filter(uuid__in=uuids).update(
            status='relayed', relayed_at=timezone.now())
