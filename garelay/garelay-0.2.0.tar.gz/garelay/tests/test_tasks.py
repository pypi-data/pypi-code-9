import json
from datetime import timedelta

from django.test import TestCase, override_settings
from django.utils import timezone

from ..tasks import cleanup_events

from garelay.tracker.models import TrackingEvent


expiry_time = timedelta(minutes=10)
expired = timedelta(minutes=11)


@override_settings(
    GARELAY_EVENT_EXPIRY=expiry_time.total_seconds())
class CleanupTaskTest(TestCase):

    def mk_event(self, status, data=json.dumps({}), created_at=None,
                 captured_at=None):
        te = TrackingEvent.objects.create(
            status=status,
            data=data,
            captured_at=captured_at or timezone.now()
        )
        if created_at:
            te.created_at = created_at
            te.save()
        return te

    def test_cleanup_events_noop(self):
        self.mk_event('registered')
        self.mk_event('registered')
        cleanup_events()
        self.assertEqual(TrackingEvent.objects.count(), 2)

    def test_cleanup_registered(self):
        self.mk_event('registered', created_at=timezone.now())
        self.mk_event('registered', created_at=timezone.now() - expired)
        self.assertEqual(TrackingEvent.objects.count(), 2)
        cleanup_events()
        self.assertEqual(TrackingEvent.objects.count(), 1)

    def test_cleanup_relayed(self):
        self.mk_event('relayed', created_at=timezone.now())
        self.mk_event('relayed', created_at=timezone.now() - expired)
        self.assertEqual(TrackingEvent.objects.count(), 2)
        cleanup_events()
        self.assertEqual(TrackingEvent.objects.count(), 1)

    def test_cleanup_captured(self):
        self.mk_event('captured', created_at=timezone.now())
        self.mk_event('captured', created_at=timezone.now() - expired)
        self.assertEqual(TrackingEvent.objects.count(), 2)
        cleanup_events()
        self.assertEqual(TrackingEvent.objects.count(), 1)
