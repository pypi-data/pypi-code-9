# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chain',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='ChainElement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('joiner', models.CharField(blank=True, max_length=3, choices=[('AND', 'and'), ('OR', 'or')])),
                ('negated', models.BooleanField(default=False)),
                ('order', models.PositiveSmallIntegerField()),
                ('chain', models.ForeignKey(to='django_condition_chain.Chain')),
            ],
        ),
        migrations.CreateModel(
            name='Condition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('module', models.CharField(help_text='Module in which the condition function resides', max_length=128)),
                ('function', models.CharField(help_text='The function which returns True or False to determine the result of this condition', max_length=64)),
            ],
        ),
        migrations.AddField(
            model_name='chainelement',
            name='condition',
            field=models.ForeignKey(to='django_condition_chain.Condition'),
        ),
        migrations.AlterUniqueTogether(
            name='chainelement',
            unique_together=set([('chain', 'order')]),
        ),
    ]
