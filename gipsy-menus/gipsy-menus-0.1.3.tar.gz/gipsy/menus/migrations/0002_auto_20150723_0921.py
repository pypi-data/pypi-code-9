# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menunode',
            name='stub',
            field=models.SlugField(choices=[(b'main', 'Main'), (b'header', 'Header'), (b'footer', 'Footer'), (b'aside', 'Aside')], blank=True, null=True, verbose_name='stub'),
        ),
    ]
