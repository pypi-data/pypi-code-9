# flake8: noqa
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('quizblock', '__first__'),
        ('pagetree', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionUserLock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question_used', models.NullBooleanField()),
                ('question_current', models.NullBooleanField()),
                ('question', models.ForeignKey(to='quizblock.Question')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='QuizRandom',
            fields=[
                ('quiz_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='quizblock.Quiz')),
                ('quiz_name', models.CharField(max_length=50)),
                ('quiz_type', models.TextField(blank=True)),
            ],
            options={
            },
            bases=('quizblock.quiz',),
        ),
        migrations.AddField(
            model_name='questionuserlock',
            name='quiz',
            field=models.ForeignKey(to='quizblock_random.QuizRandom'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='questionuserlock',
            name='section',
            field=models.ForeignKey(to='pagetree.Section'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='questionuserlock',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
