import json

from django.test import TestCase

from model_logging import models
from . import factories


class TestLogEntry(TestCase):
    model = models.LogEntry

    def test_fields(self):
        expected = [
            'id',
            'date_created',
            'creator',
            'creator_id',
            'operation',
            'data',
            'user',
            'user_id',
            'model_path',
        ]

        fields = self.model._meta.get_all_field_names()
        self.assertCountEqual(fields, expected)


class TestLogEntryManager(TestCase):
    manager = models.LogEntry.objects

    def test_log(self):
        """Assert log() creates a LogEntry object correctly."""
        user = factories.UserFactory.create()
        data = {
            'log_entry_creator': user,
            'operation': models.LogEntry.OPERATION_ADDED,
            'model': models.LogEntry,
            'user': user,
            'json_data': json.dumps({'item': 42}),
        }

        self.manager.log(**data)

        entry = self.manager.get()
        self.assertEqual(entry.creator, data['log_entry_creator'])
        self.assertEqual(entry.operation, data['operation'])
        self.assertEqual(entry.model_path, 'model_logging.models.LogEntry')
        self.assertEqual(entry.user, data['user'])
        self.assertEqual(entry.data, data['json_data'])

    def test_retrieve_for_user(self):
        entry, _ = factories.LogEntryFactory.create_batch(2)
        model = models.LogEntry

        retrieved = self.manager.retrieve_for_user(model=model, user=entry.user)
        self.assertEqual(list(retrieved), [entry])

    def test_retrieve_for_creator(self):
        entry, _ = factories.LogEntryFactory.create_batch(2)
        model = models.LogEntry

        retrieved = self.manager.retrieve_for_creator(model=model, creator=entry.creator)
        self.assertEqual(list(retrieved), [entry])
