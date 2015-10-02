import json

import responses

from django.conf import settings
from django.test import TestCase
from django.utils import timezone

from ..models import TrackingEvent
from ..tasks import relay_events


class TaskTest(TestCase):

    def setUp(self):
        responses.add(responses.POST, settings.GARELAY_SERVER,
                      status=200, content_type='application/json',
                      body=json.dumps([
                          {'uuid': 'uuid-1'},
                          {'uuid': 'uuid-3'},
                      ]))

    @responses.activate
    def test_register_events(self):
        TrackingEvent.objects.create(
            uuid='uuid-1',
            status='captured', data=json.dumps({}),
            captured_at=timezone.now())
        TrackingEvent.objects.create(
            uuid='uuid-2',
            status='relayed', data=json.dumps({}),
            captured_at=timezone.now())
        TrackingEvent.objects.create(
            uuid='uuid-3',
            status='captured', data=json.dumps({}),
            captured_at=timezone.now())
        self.assertEqual(
            TrackingEvent.objects.filter(status='relayed').count(), 1)
        relay_events()
        self.assertEqual(
            TrackingEvent.objects.filter(status='relayed').count(), 3)
