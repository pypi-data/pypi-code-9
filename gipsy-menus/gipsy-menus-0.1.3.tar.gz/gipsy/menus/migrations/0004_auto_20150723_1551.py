# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0003_auto_20150723_0923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menunode',
            name='stub',
            field=models.SlugField(null=True, default=None, choices=[(None, 'No stub'), (b'main', 'Main'), (b'header', 'Header'), (b'footer', 'Footer'), (b'aside', 'Aside')], blank=True, unique=True, verbose_name='stub'),
        ),
    ]
