# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('luhublog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='twitter_url',
            field=models.URLField(verbose_name=b'URL Perfil Facebook', blank=True),
        ),
        migrations.AlterField(
            model_name='author',
            name='facebook_page_url',
            field=models.URLField(verbose_name=b'URL Pagina Facebook', blank=True),
        ),
    ]
