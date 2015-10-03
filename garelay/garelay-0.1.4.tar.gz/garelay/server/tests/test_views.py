import json

from django.test import TestCase
from django.test.client import Client
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.core.serializers.json import DjangoJSONEncoder

from garelay.tracker.models import TrackingEvent


class ServerTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_tracking_event(self):
        event = TrackingEvent.objects.create(uuid='the-uuid')
        event.update_fields({
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
        })
        event.save()
        self.assertFalse(event.relayed_at)
        self.assertFalse(event.registered_at)
        self.assertFalse(event.status)
        response = self.client.post(
            reverse('server'),
            data=json.dumps([event.to_dict()], cls=DjangoJSONEncoder),
            content_type='application/json')
        data = json.loads(response.content)
        self.assertTrue(data, [{'uuid': 'the-uuid'}])
        reloaded_event = TrackingEvent.objects.get(pk=event.pk)
        self.assertTrue(reloaded_event.relayed_at)
        self.assertFalse(reloaded_event.registered_at)
        self.assertEqual(reloaded_event.status, 'captured')
