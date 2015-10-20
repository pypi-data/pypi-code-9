from StringIO import StringIO

from django.test import TestCase
from django.conf import settings

from garelay.management.commands import relay_events, register_events


class CommandsTest(TestCase):

    def test_relay_events(self):
        cmd = relay_events.Command()
        cmd.stdout = StringIO()
        cmd.handle()
        self.assertEqual(
            cmd.stdout.getvalue(),
            'Relaying 0 events in batches of %s.\nDone.\n' % (
                settings.GARELAY_RELAY_BATCH_SIZE,))

    def test_register_events(self):
        cmd = register_events.Command()
        cmd.stdout = StringIO()
        cmd.handle()
        self.assertEqual(
            cmd.stdout.getvalue(),
            'Registering 0 events in batches of %s.\nDone.\n' % (
                settings.GARELAY_REGISTER_BATCH_SIZE,))
