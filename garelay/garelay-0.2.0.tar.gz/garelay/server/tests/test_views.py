import json
from datetime import timedelta

from django.test import TestCase
from django.test.client import Client
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.core.serializers.json import DjangoJSONEncoder

from garelay.tracker.models import TrackingEvent


class ServerTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.event = {
            'uuid': 'the-uuid',
            'tracking_id': 'tracking_id',
            'client_id': 'client_id',
            'user_agent': 'user_agent',
            'data': {
                'foo': 'bar'
            },
            'created_at': timezone.now(),
            'updated_at': timezone.now(),
            'captured_at': timezone.now(),
            'relayed_at': None,
            'registered_at': None,
        }

    def test_tracking_event(self):
        response = self.client.post(
            reverse('server'),
            data=json.dumps([self.event], cls=DjangoJSONEncoder),
            content_type='application/json')
        data = json.loads(response.content)
        self.assertEqual(data, [{'uuid': 'the-uuid'}])
        event_record = TrackingEvent.objects.get(uuid=self.event['uuid'])
        self.assertTrue(event_record.relayed_at)
        self.assertFalse(event_record.registered_at)
        self.assertEqual(event_record.status, 'captured')

    def test_tracking_event_idempotence(self):
        response = self.client.post(
            reverse('server'),
            data=json.dumps([self.event], cls=DjangoJSONEncoder),
            content_type='application/json')
        data = json.loads(response.content)
        self.assertTrue(data, [{'uuid': 'the-uuid'}])

        cloned_event = self.event.copy()
        cloned_event['captured_at'] = (
            cloned_event['captured_at'] - timedelta(days=10))

        response = self.client.post(
            reverse('server'),
            data=json.dumps([cloned_event], cls=DjangoJSONEncoder),
            content_type='application/json')

        data = json.loads(response.content)
        self.assertEqual(data, [])

        event_record = TrackingEvent.objects.get(uuid=self.event['uuid'])
        self.assertEqual(event_record.captured_at.day,
                         self.event['captured_at'].day)
        self.assertTrue(event_record.relayed_at)
        self.assertFalse(event_record.registered_at)
        self.assertEqual(event_record.status, 'captured')
