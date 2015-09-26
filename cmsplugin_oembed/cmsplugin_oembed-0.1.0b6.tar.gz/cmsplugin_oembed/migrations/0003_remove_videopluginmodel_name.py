# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cmsplugin_oembed', '0002_videopluginmodel_max_width'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='videopluginmodel',
            name='name',
        ),
    ]
