# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fluent_contents', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TwitterRecentEntriesItem',
            fields=[
                ('contentitem_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='fluent_contents.ContentItem')),
                ('title', models.CharField(help_text='You may use Twitter markup here, such as a #hashtag or @username.', max_length=200, verbose_name='title', blank=True)),
                ('twitter_user', models.CharField(help_text='Display Tweets from a Twitter user specified by @username', max_length=75, verbose_name='@username')),
                ('amount', models.PositiveSmallIntegerField(default=5, verbose_name='number of results')),
                ('widget_id', models.CharField(help_text="See <a href='https://twitter.com/settings/widgets' target='_blank'>https://twitter.com/settings/widgets</a> on how to obtain one.", max_length=75, verbose_name='widget id')),
                ('footer_text', models.CharField(help_text='You may use Twitter markup here, such as a #hashtag or @username.', max_length=200, verbose_name='footer text', blank=True)),
                ('include_replies', models.BooleanField(default=False, verbose_name='include replies?')),
            ],
            options={
                'db_table': 'contentitem_fluentcms_twitterfeed_twitterrecententriesitem',
                'verbose_name': 'Recent twitter entries',
                'verbose_name_plural': 'Recent twitter entries',
            },
            bases=('fluent_contents.contentitem',),
        ),
        migrations.CreateModel(
            name='TwitterSearchItem',
            fields=[
                ('contentitem_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='fluent_contents.ContentItem')),
                ('title', models.CharField(help_text='You may use Twitter markup here, such as a #hashtag or @username.', max_length=200, verbose_name='title', blank=True)),
                ('query', models.CharField(default=b'', help_text="<a href='https://dev.twitter.com/web/embedded-timelines/search' target='_blank'>Twitter search syntax</a> is allowed.", max_length=200, verbose_name='search for')),
                ('amount', models.PositiveSmallIntegerField(default=5, verbose_name='number of results')),
                ('widget_id', models.CharField(help_text="See <a href='https://twitter.com/settings/widgets' target='_blank'>https://twitter.com/settings/widgets</a> on how to obtain one.", max_length=75, verbose_name='widget id')),
                ('footer_text', models.CharField(help_text='You may use Twitter markup here, such as a #hashtag or @username.', max_length=200, verbose_name='footer text', blank=True)),
                ('include_replies', models.BooleanField(default=False, verbose_name='include replies?')),
            ],
            options={
                'db_table': 'contentitem_fluentcms_twitterfeed_twittersearchitem',
                'verbose_name': 'Twitter search timeline',
                'verbose_name_plural': 'Twitter search timeline',
            },
            bases=('fluent_contents.contentitem',),
        ),
    ]
