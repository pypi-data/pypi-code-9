# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import stacks_twitter.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hashtag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hashtag', models.CharField(unique=True, max_length=140, verbose_name='Hashtag', db_index=True)),
            ],
            options={
                'verbose_name': 'Hashtag',
                'verbose_name_plural': 'Hashtags',
            },
        ),
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tweet_id', stacks_twitter.fields.TweetIDField(help_text=b'Enter a link to a tweet or a Tweet ID in this field.', unique=True, max_length=255, verbose_name='Tweet Link / Tweet ID')),
                ('text', models.TextField(max_length=140, verbose_name='Tweet Text', blank=True)),
                ('tweet_link', models.URLField(verbose_name='Link To Tweet', max_length=255, editable=False, blank=True)),
                ('hashtags', models.ManyToManyField(to='stacks_twitter.Hashtag', blank=True)),
            ],
            options={
                'verbose_name': 'Tweet',
                'verbose_name_plural': 'Tweets',
            },
        ),
        migrations.CreateModel(
            name='TwitterUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(unique=True, max_length=15, verbose_name='Twitter Username')),
                ('verbose_name', models.CharField(max_length=140, verbose_name='Verbose Name', blank=True)),
                ('profile_image_url', models.URLField(max_length=255, verbose_name='URI/URL', blank=True)),
            ],
            options={
                'verbose_name': 'Twitter User',
                'verbose_name_plural': 'Twitter Users',
            },
        ),
        migrations.AddField(
            model_name='tweet',
            name='user',
            field=models.ForeignKey(verbose_name='User', blank=True, to='stacks_twitter.TwitterUser'),
        ),
    ]
