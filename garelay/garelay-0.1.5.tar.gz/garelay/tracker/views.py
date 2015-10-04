from uuid import uuid4
import json

from django.http import HttpResponse
from django.views.decorators.cache import never_cache
from django.utils import timezone

from .models import TrackingEvent


PIXEL_GIF_DATA = ("R0lGODlhAQABAIAAAAAAAP///yH5"
                  "BAEAAAAALAAAAAABAAEAAAIBRAA7").decode('base64')


def get_tracker_uuid(request):
    return request.session.setdefault('tracker_uuid', uuid4().hex)


@never_cache
def tracker(request, tracking_id, path):
    client_id = get_tracker_uuid(request)
    data = {
        'dp': path,
        'uip': request.META.get('REMOTE_ADDR') or '',
        'dr': request.META.get('HTTP_REFERER') or '',
        'ul': request.META.get('HTTP_ACCEPT_LANGUAGE') or '',
    }
    data.update(request.GET)
    TrackingEvent.objects.create(
        tracking_id=tracking_id,
        client_id=client_id,
        user_agent=request.META.get('HTTP_USER_AGENT') or '',
        data=json.dumps(data),
        captured_at=timezone.now(),
        status='captured')
    return HttpResponse(PIXEL_GIF_DATA, content_type='image/gif')
