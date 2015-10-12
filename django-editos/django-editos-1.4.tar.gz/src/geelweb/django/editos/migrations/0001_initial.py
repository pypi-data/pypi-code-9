# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Edito',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(help_text=None, max_length=100)),
                ('link', models.URLField(help_text=None, blank=True)),
                ('button_label', models.CharField(default=b'Go !', help_text=None, max_length=20, blank=True)),
                ('image', models.FileField(help_text=None, upload_to=b'editos')),
                ('text_content', models.CharField(help_text=None, max_length=400, blank=True)),
                ('display_from', models.DateField(help_text=None)),
                ('display_until', models.DateField(help_text=None)),
                ('active', models.BooleanField(default=True, help_text=None)),
                ('text_theme', models.CharField(default=b'light', help_text=None, max_length=10, blank=True, choices=[(b'light', b'Light'), (b'dark', b'Dark')])),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
