# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def populate_display_title(apps, schema_editor):
    """
    Populates display_title for ContentGroup
    """
    ContentGroup = apps.get_model("stacks_contentgroup", "ContentGroup")
    for cg in ContentGroup.objects.all():
        cg.display_title = cg.name
        cg.save()


class Migration(migrations.Migration):

    dependencies = [
        ('stacks_contentgroup', '0002_auto_20150528_1526'),
    ]

    operations = [
        migrations.RunPython(
            populate_display_title
        )
    ]
