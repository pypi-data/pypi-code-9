import json

from django.test import TestCase
from django.utils import timezone

from ..tasks import register_events

from garelay.tracker.models import TrackingEvent

from UniversalAnalytics import Tracker

from mock import patch


class TaskTest(TestCase):

    @patch.object(Tracker.Tracker, 'send')
    def test_register_events(self, mocked_send):
        TrackingEvent.objects.create(
            status='registered', data=json.dumps({}),
            captured_at=timezone.now())
        TrackingEvent.objects.create(
            status='relayed', data=json.dumps({}),
            captured_at=timezone.now())
        register_events()
        self.assertEqual(mocked_send.call_count, 1)
