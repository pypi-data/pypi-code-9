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


class LoginForm(ModelForm):
    '''
    From for user login
    '''
    login = forms.EmailField(
        widget=forms.TextInput(attrs={'ng-model': 'login.login', 'required': 'True'}),
        label='Логин или емайл'
    )

    # username = forms.CharField(
    #     widget=forms.TextInput(attrs={'ng-model': 'login.username', 'required': 'True'}),
    #     label='Логин'
    # )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'ng-model': 'login.password', 'required': 'True', 'type': 'password'}),
        label='Пароль'
    )
    #
    # remember_me = forms.BooleanField(
    #     widget=forms.CheckboxInput(attrs={'ng-model': 'login.remember_me'}),
    #     initial=True,
    #     label="Запомнить меня",
    #     required=False
    # )

    class Meta:
        model = User
        fields = ('login', 'password')


class RegisterForm(ModelForm):
    '''
    Form for user registration
    '''
    username = forms.CharField(
        widget=forms.TextInput(attrs={'ng-model': 'register.username', 'required': 'True'}),
        label='Логин'
    )

    # first_name = forms.CharField(
    #     widget=forms.TextInput(attrs={'ng-model': 'register.first_name', 'ng-initial': 'True', 'required': 'False'}),
    #     label='Имя'
    # )
    #
    # last_name = forms.CharField(
    #     widget=forms.TextInput(attrs={'ng-model': 'register.last_name ', 'ng-initial': 'True', 'required': 'False'}),
    #     label='Фамилия'
    # )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'ng-model': 'register.email', 'ng-initial': 'True', 'required': 'True', 'type': 'email'}),
        label='Email'
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'ng-model': 'register.password', 'required': 'True', 'type': 'password'}),
        label='Пароль'
    )

    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'ng-model': 'register.confirm_password', 'required': 'True', 'type': 'password'}),
        label='Подвердите пароль')

    # city = forms.CharField(
    #     widget=forms.TextInput(attrs={'ng-model': 'register.city', 'ng-initial': 'True', 'required': 'True'}),
    #     label='Город')
    #
    # phone = forms.CharField(
    #     widget=forms.TextInput(attrs={'ng-model': 'register.phone', 'ng-initial': 'True'}),
    #     label='Телефон')

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']


