import json

from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse

from ..models import TrackingEvent


class ViewsTest(TestCase):

    def setUp(self):
        self.client = Client(
            HTTP_USER_AGENT='The Agent',
            HTTP_ACCEPT_LANGUAGE='en-gb',
            HTTP_REFERER='/foo')

    def test_tracker_response_headers(self):
        response = self.client.get(reverse('tracker', kwargs={
            'tracking_id': 'UA-F00-1',
            'path': '',
        }))
        self.assertEqual(response['Content-Type'], 'image/gif')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Cache-Control'], 'max-age=0')
        self.assertTrue(response['Expires'])

    def test_tracking_event(self):
        self.assertEqual(TrackingEvent.objects.count(), 0)
        path = reverse('tracker', kwargs={
            'tracking_id': 'UA-F00-1',
            'path': '',
        })
        self.client.get(path)
        [event] = TrackingEvent.objects.all()
        self.assertTrue(event.uuid)
        self.assertTrue(event.created_at)
        self.assertTrue(event.updated_at)
        self.assertTrue(event.captured_at)
        self.assertFalse(event.relayed_at)
        self.assertFalse(event.registered_at)
        self.assertEqual(event.tracking_id, 'UA-F00-1')
        self.assertEqual(event.client_id, self.client.session['tracker_uuid'])
        self.assertEqual(event.user_agent, 'The Agent')
        self.assertEqual(event.status, 'captured')
        self.assertEqual(json.loads(event.data), {
            'ul': 'en-gb',
            'dr': '/foo',
            'uip': '127.0.0.1',
            'dp': '',
        })
        self.assertEqual(TrackingEvent.objects.count(), 1)

    def test_tracking_path(self):
        path = reverse('tracker', kwargs={
            'tracking_id': 'UA-F00-1',
            'path': '/foo/bar/baz.html',
        })
        self.client.get(path)
        [event] = TrackingEvent.objects.all()
        self.assertEqual(
            json.loads(event.data)['dp'],
            '/foo/bar/baz.html')
