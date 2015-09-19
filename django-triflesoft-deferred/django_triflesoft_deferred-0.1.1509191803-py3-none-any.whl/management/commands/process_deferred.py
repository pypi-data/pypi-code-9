from optparse import make_option

from django.core.management.base import BaseCommand

from deferred.models import Failure
from deferred.models import Task


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option(
            '-r',
            action='store',
            dest='retries',
            type='int',
            help='Maximum retry count'),
    )

    args = '-r RETRY_COUNT'
    help = 'Process Task Queue.'

    def handle(self, *args, **options):
        if not options['retries']:
            MAX_RETRIES = 10
        else:
            MAX_RETRIES = int(options['retries'])

        have_new  = True

        while have_new:
            have_new = False
            tasks = Task.objects.filter(is_processed=False).order_by('-retry_count', '-priority')

            for task in tasks[:10]:
                have_new |= task.retry_count == 0
                obj = task.to_object()

                try:
                    obj()
                    task.is_processed = True
                    task.is_succeeded = True
                    task.save()
                except Exception as e:
                    task.retry_count += 1

                    if task.retry_count >= MAX_RETRIES:
                        task.is_processed = True
                        task.is_succeeded = False

                    task.save()

                    failure = Failure()
                    failure.task = task
                    failure.exception_type = type(e).__name__
                    failure.exception_args = e.args
                    failure.save()
