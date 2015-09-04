from __future__ import absolute_import

from celery import shared_task
from django.core import management


@shared_task
def update_newswall():
    management.call_command('update_newswall', interactive=False)
    return {'result': 'Update newswall OK'}
