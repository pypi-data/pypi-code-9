import logging
import datetime
from optparse import make_option
from django.core.management import BaseCommand
import sys
from blacklist import models

log = logging.getLogger('remove_request_logs')


class Command(BaseCommand):
    args = 'from'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **opts):
        if len(args) < 1:
            print('Please, provide data in %y%m%d or %y%m%d%H%M%S format to remove old logs')
            sys.exit(1)
        from_date = args[0]
        try:
            from_date = datetime.datetime.strptime(from_date, '%y%m%d' if len(from_date) <= 6 else '%y%m%d%H%M%S')
        except ValueError:
            print('Parameter does not match neither %y%m%d or %y%m%d%H%M%S format. '
                  'Please, provide valid date')
            sys.exit(2)
        query = models.RequestLog.objects.filter(created__lt=from_date)
        print('removing %d logs from %s' % (query.count(), from_date.isoformat()))
        query.delete()
