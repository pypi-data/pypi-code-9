#! -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User


class Poll(models.Model):
    """ Poll

    * Poll has question and description fields
    """

    question = models.CharField('Question Name', max_length=255)
    description = models.TextField('Description', blank=True)
    """ Description field allows Blank """

    null_field = models.CharField('Null Test', null=True, max_length=255)
    blank_field = models.CharField('Blank Test', blank=True, max_length=255)
    both_field = models.CharField('Both Test',
                                  null=True, blank=True, max_length=255)
    index_field = models.CharField('Index Test', db_index=True, max_length=255)

    class Meta:
        verbose_name = 'Poll'


class Choice(models.Model):
    """ Choice

    * Choice has poll reference
    * Choice has choices field
    """

    CHOICES = (
        (1, 'test1'),
        (2, 'test2'),
        (3, 'test3'),
    )

    poll = models.ForeignKey(Poll, verbose_name='Poll')
    choice = models.SmallIntegerField('Choice',
                                      max_length=255, choices=CHOICES)

    class Meta:
        verbose_name = 'Choice'


class Vote(models.Model):
    """ Vote

    * Vote has user reference
    * Vote has poll reference
    * Vote has choice reference
    """

    user = models.ForeignKey(User, verbose_name='Voted User')
    poll = models.ForeignKey(Poll, verbose_name='Voted Poll')
    choice = models.ForeignKey(Choice, verbose_name='Voted Choice')

    class Meta:
        verbose_name = 'Vote'
        unique_together = (('user', 'poll'))
