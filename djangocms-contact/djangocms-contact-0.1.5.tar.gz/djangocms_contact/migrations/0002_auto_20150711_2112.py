# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djangocms_contact', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactmessage',
            name='subject',
            field=models.CharField(verbose_name='Subject', max_length=255, blank=True),
            preserve_default=True,
        ),
    ]
