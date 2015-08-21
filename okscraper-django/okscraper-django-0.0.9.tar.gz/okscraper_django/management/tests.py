from django.utils import unittest
from okscraper_django.management.base_commands import BaseDbLogCommand
from okscraper_django.models import ScraperRun


class TestBaseDbLogCommand(BaseDbLogCommand):
    def _handle(self, *args, **options):
        self._log_debug('debug')
        self._log_info('info')
        self._log_warn('warn')
        self._log_error('error')


class DbLogCommandTestCase(unittest.TestCase):

    def test(self):
        command = TestBaseDbLogCommand()
        args = []
        options = {}
        command.handle(*args, **options)
        self.assertListEqual(
            list(command._scraper_run.logs.order_by('time').values('status', 'text')),
            [{'status': u'DEBUG', 'text': u'debug'}, {'status': u'INFO', 'text': u'info'}, {'status': u'WARNING', 'text': u'warn'}, {'status': u'ERROR', 'text': u'error'}]
        )
