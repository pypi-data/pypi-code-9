# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
    ]

    if django.VERSION >= (1, 8):
        dependencies.append(
            ('contenttypes', '0002_remove_content_type_name'),
        )

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('path', models.CharField(unique=True, max_length=255)),
                ('depth', models.PositiveIntegerField()),
                ('numchild', models.PositiveIntegerField(default=0)),
                ('name', models.CharField(unique=True, max_length=255, verbose_name='Name')),
                ('tag', models.ForeignKey(editable=False, to='taggit.Tag')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField(verbose_name='Object ID')),
                ('created', models.DateTimeField(verbose_name='Created')),
                ('modified', models.DateTimeField(verbose_name='Modified')),
                ('title', models.CharField(max_length=255, verbose_name='Title', blank=True)),
                ('url', models.CharField(max_length=255, verbose_name='URL', blank=True)),
                ('live', models.BooleanField(default=True, verbose_name='Live?')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'ordering': ('title',),
                'verbose_name': 'Entry',
                'verbose_name_plural': 'Entries',
            },
        ),
        migrations.CreateModel(
            name='EntryTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('entry', models.ForeignKey(related_name='entry_tags', to='wagtailrelations.Entry')),
                ('tag', models.ForeignKey(related_name='relation_entries', to='taggit.Tag')),
            ],
            options={
                'ordering': ('tag__name', 'entry__title'),
                'verbose_name': 'Entry Tag',
                'verbose_name_plural': 'Entry Tags',
            },
        ),
        migrations.AlterUniqueTogether(
            name='entrytag',
            unique_together=set([('tag', 'entry')]),
        ),
    ]
