import json
import logging

from uuid import uuid4

from django.db import models
from django.db.models import signals
from django.utils import timezone
from django.dispatch import receiver

from UniversalAnalytics import Tracker


class TrackingEvent(models.Model):
    uuid = models.CharField(max_length=255)
    tracking_id = models.CharField(max_length=255)
    client_id = models.CharField(max_length=255)
    user_agent = models.TextField()
    data = models.TextField(default='{}')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    captured_at = models.DateTimeField(null=True)
    relayed_at = models.DateTimeField(null=True)
    registered_at = models.DateTimeField(null=True)
    status = models.CharField(max_length=255, choices=(
        ('captured', 'Captured'),
        ('relayed', 'Relayed'),
        ('registered', 'Registered')
    ), null=True)

    class Meta:
        ordering = ['created_at']

    def update_fields(self, data):
        self.tracking_id = data['tracking_id']
        self.client_id = data['client_id']
        self.user_agent = data['user_agent']
        self.data = json.dumps(data['data'])
        self.captured_at = data['captured_at']
        self.relayed_at = data['relayed_at']
        self.registered_at = data['registered_at']

    def to_dict(self):
        payload = dict(
            (field.name, getattr(self, field.name))
            for field in self._meta.fields
            if field.name not in ['id', 'status'])
        payload['data'] = json.loads(payload['data'])
        return payload

    def register(self):
        tracker = Tracker.create(self.tracking_id,
                                 client_id=self.client_id,
                                 user_agent=self.user_agent)
        payload = json.loads(self.data)

        # back date
        delta = timezone.now() - self.captured_at
        if delta.seconds > (4 * 60 * 60):
            logging.warning('Queue time exceeds 4 hours, '
                            'may be ignored by Google Analytics.')

        # GA requires milliseconds
        payload['qt'] = delta.total_seconds() * 1000

        tracker.send('pageview', payload)
        self.registered_at = timezone.now()
        self.status = 'registered'


@receiver(signals.pre_save, sender=TrackingEvent)
def tracking_event_auto_uuid(sender, instance, **kwargs):
    if not instance.uuid:
        instance.uuid = uuid4().hex
