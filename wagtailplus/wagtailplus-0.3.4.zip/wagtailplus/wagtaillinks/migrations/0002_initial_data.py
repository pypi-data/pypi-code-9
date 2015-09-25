# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import VERSION as DJANGO_VERSION
from django.db import migrations


def add_link_permissions_to_admin_groups(apps, schema_editor):
    ContentType = apps.get_model('contenttypes.ContentType')
    Permission  = apps.get_model('auth.Permission')
    Group       = apps.get_model('auth.Group')

    # Get link permissions
    link_content_type, _created = ContentType.objects.get_or_create(
        model       = 'document',
        app_label   = 'wagtaildocs',
        defaults    = {'name': 'link'} if DJANGO_VERSION < (1, 8) else {}
    )

    add_link_permission, _created = Permission.objects.get_or_create(
        content_type    = link_content_type,
        codename        = 'add_link',
        defaults        = {'name': 'Can add link'}
    )
    change_link_permission, _created = Permission.objects.get_or_create(
        content_type    = link_content_type,
        codename        = 'change_link',
        defaults        = {'name': 'Can change link'}
    )
    delete_link_permission, _created = Permission.objects.get_or_create(
        content_type    = link_content_type,
        codename        = 'delete_link',
        defaults        = {'name': 'Can delete link'}
    )

    # Assign it to Editors and Moderators groups
    for group in Group.objects.filter(name__in=['Editors', 'Moderators']):
        group.permissions.add(
            add_link_permission,
            change_link_permission,
            delete_link_permission
        )


class Migration(migrations.Migration):

    dependencies = [
        ('wagtaillinks', '0001_initial'),

        # Need to run wagtailcores initial data migration to make sure the groups are created
        ('wagtailcore', '0002_initial_data'),
    ]

    operations = [
        migrations.RunPython(add_link_permissions_to_admin_groups),
    ]
