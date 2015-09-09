# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stacks_contentgroup', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contentgroup',
            name='display_title',
            field=models.CharField(default='Foo', help_text=b'The displayed-to-the-user title of this Content Group.', max_length=120, verbose_name='Title'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='content',
            name='title',
            field=models.CharField(help_text=b'The displayed-to-the-user title of this content.', max_length=120, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='contentgroup',
            name='name',
            field=models.CharField(help_text=b'The internal name/signifier of this content.', max_length=120, verbose_name='Name'),
        ),
    ]
