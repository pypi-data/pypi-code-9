# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', models.FileField(upload_to=b'sticky/files/', verbose_name=b'\xd0\xa4\xd0\xb0\xd0\xb9\xd0\xbb')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'File',
                'verbose_name_plural': 'Files',
            },
        ),
    ]
