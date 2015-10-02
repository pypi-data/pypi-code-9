import json

from django.http import HttpResponseBadRequest, JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from garelay.tracker.models import TrackingEvent


@csrf_exempt
def server(request):
    try:
        tracking_events = json.loads(request.body)
    except ValueError:
        return HttpResponseBadRequest()

    response = []
    for tracking_event in tracking_events:
        record, _ = TrackingEvent.objects.get_or_create(
            uuid=tracking_event['uuid'])
        record.update_fields(tracking_event)
        record.status = 'captured'
        record.relayed_at = timezone.now()
        record.save()
        response.append({
            'uuid': record.uuid,
        })
    return JsonResponse(response, safe=False)
