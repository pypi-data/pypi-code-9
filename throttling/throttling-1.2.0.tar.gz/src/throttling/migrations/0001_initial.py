# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Access',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('scope', models.CharField(max_length=100)),
                ('count', models.IntegerField(default=0)),
                ('datemark', models.DateTimeField(default=django.utils.timezone.now, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Consumer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip', models.IPAddressField(null=True, blank=True)),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='access',
            name='consumer',
            field=models.ForeignKey(to='throttling.Consumer'),
        ),
        migrations.AlterUniqueTogether(
            name='consumer',
            unique_together=set([('user', 'ip')]),
        ),
        migrations.AlterUniqueTogether(
            name='access',
            unique_together=set([('consumer', 'scope')]),
        ),
    ]
