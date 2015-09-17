# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stacks_twitter', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='tweet_link',
            field=models.URLField(max_length=255, verbose_name='Link To Tweet', blank=True),
        ),
        migrations.AlterField(
            model_name='twitteruser',
            name='profile_image_url',
            field=models.URLField(max_length=255, verbose_name='Profile Image URL', blank=True),
        ),
    ]
