# coding=utf-8
from django.utils import timezone

from user_hash.models import UserHash

__author__ = 'franki'

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    # args = '<poll_id poll_id ...>'
    help = u'Cleanup expired UserHash entries from the database.'

    def handle(self, *args, **options):
        UserHash.objects.filter(expires__lt=timezone.now()).delete()
