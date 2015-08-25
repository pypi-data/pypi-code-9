import logging
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from ...models import export_view, get_report_path

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Export database view reports that are too expensive to run live.'

    def handle(self, prefix='v_', *args, **kwargs):
        for view_name in settings.OFF_PEAK_VIEWS:
            file_path = get_report_path(view_name[len(prefix):])
            yesterday_path = get_report_path(
                view_name[len(prefix):], date='yesterday')
            logger.info("Exporting view: {view} to {file}".format(
                view=view_name, file=file_path))
            with open(file_path, 'w') as f:
                export_view(view_name, f, prefix)

            logger.info("Deleting yesterday's report: {path}".format(
                path=yesterday_path))
            try:
                os.remove(yesterday_path)
            except OSError:
                pass
