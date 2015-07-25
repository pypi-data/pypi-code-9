# -*- coding: utf-8 -*-

import datetime, sys, os, re

from django.db import models
from django.forms import ModelForm
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django import forms
from autoslug import AutoSlugField

from sorl.thumbnail import ImageField
from PIL import Image
from autoslug import AutoSlugField
from datetime import date, datetime
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.html import format_html

from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager

from django.core.urlresolvers import reverse

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from da_mailer.helper import *


class UserProfile(models.Model):
    '''
    User profile
    '''
    user = models.OneToOneField(User)

    second_name = models.CharField(
        max_length=50,
        default="",
        blank=True
    )

    avatar = models.ImageField(
        upload_to='avatars',
        blank=True
    )

    AVATAR_CHOICES = (
        ('/static/images/avatar/common.png', 'общая'),
        ('/static/images/avatar/glasses.png', 'очки'),
    )

    phone = models.CharField(
        max_length=50,
        default="",
        blank=True
    )

    city = models.CharField(max_length=100, default="", blank=True)

    points = models.IntegerField(
        default=0,
        blank=True
    )

    template_avatar = models.CharField(
        max_length=100,
        blank=True,
        default='/static/images/avatar/common.png',
        choices=AVATAR_CHOICES,

    )

    color = models.CharField(
        max_length=30,
        default='#2aa4e9',
        blank=True
    )

    phone_confirmed = models.BooleanField(
        default=False,
    )

    personal_data_confirmed = models.BooleanField(
        default=False,
    )

    # relations = models.ManyToManyField(
    #     'self',
    #     related_name='relations',
    #     blank=True,
    # )

    def __str__(self):
        return "%s's profile" % self.user

    def last_project(self):
        return "poo"

class RelationType(models.Model):
    name = models.CharField(
        max_length=200,
    )

    slug = models.CharField(
        max_length=200,
    )

    def __unicode__(self):
        return self.name


class Relation(models.Model):
    first_person = models.ForeignKey(
        User,
        related_name='first_person'
    )

    second_person = models.ForeignKey(
        User,
        related_name='second_person'
    )

    type = models.ForeignKey(
        RelationType
    )

    description = models.TextField(
        blank=True
    )


def create_user_profile(sender, instance, created, **kwargs):
    # if created:
    profile, created = UserProfile.objects.get_or_create(user=instance)


post_save.connect(create_user_profile, sender=User)
