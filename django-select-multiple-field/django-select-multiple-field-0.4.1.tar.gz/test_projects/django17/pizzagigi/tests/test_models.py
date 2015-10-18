# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .migration_helpers import DjangoMigrationTestCase

from pizzagigi.models import Pizza


class MyMigrationTestCase(DjangoMigrationTestCase):

    start_migration = '0001_initial'
    dest_migration = '0002_auto__20150214_1944'
    django_application = 'suthern'

    def test_field_survives_migration(self):
        self.migrate_to_dest()

        choice_1 = Pizza.PEPPERONI
        order = Pizza()
        order.toppings = choice_1
        order.save()

        self.assertEqual(order.toppings, [choice_1])
