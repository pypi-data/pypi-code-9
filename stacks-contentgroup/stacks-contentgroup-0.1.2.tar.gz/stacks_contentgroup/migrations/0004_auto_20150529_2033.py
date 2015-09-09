# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stacks_contentgroup', '0003_auto_20150528_1526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contentgroup',
            name='display_title',
            field=models.CharField(help_text=b'The displayed-to-the-user title of this Content Group.', max_length=120, verbose_name='Title', blank=True),
        ),
    ]
