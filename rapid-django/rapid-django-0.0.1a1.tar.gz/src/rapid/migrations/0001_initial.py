# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=60, verbose_name='nome')),
                ('python_name', models.CharField(unique=True, max_length=255, verbose_name='Nome no Python')),
                ('enabled', models.BooleanField(default=True, verbose_name='ativa')),
                ('managers', models.ManyToManyField(related_name='managed_applications', verbose_name='gestores', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'aplica\xe7\xe3o',
                'verbose_name_plural': 'aplica\xe7\xf5es',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=60, verbose_name='nome')),
                ('description', models.TextField(verbose_name='descri\xe7\xe3o')),
                ('application', models.ForeignKey(verbose_name='aplica\xe7\xe3o', to='rapid.Application')),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='usu\xe1rios', blank=True)),
            ],
            options={
                'verbose_name': 'perfil',
                'verbose_name_plural': 'perfis',
            },
        ),
    ]
