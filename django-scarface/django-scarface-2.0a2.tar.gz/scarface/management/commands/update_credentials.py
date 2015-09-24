# coding=utf8
from optparse import make_option
import sys

__author__ = 'dreipol GmbH'

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    args = '<New credentials>'
    help = 'Update an SNS Application (Platform) with new Credentials'

    def handle(self, *args, **options):
        if not args:
            self.stdout.write("Paste the new credentials as it would be in the settings:\n")
            args = sys.stdin.readlines()

        for arg in args:
            print arg