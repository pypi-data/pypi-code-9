# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

class CrudModel(models.Model):
    class Meta:
        abstract = True


class Application(models.Model):
    name = models.CharField(max_length=60, unique=True, verbose_name=u"nome")
    python_name = models.CharField(max_length=255, unique=True, verbose_name=u"Nome no Python")
    managers = models.ManyToManyField(User, verbose_name=u"gestores", related_name='managed_applications')
    enabled = models.BooleanField(default=True, verbose_name=u"ativa")

    def __unicode__(self):
        return self.name

    url_name = 'aplicacao'

    class Meta:
        verbose_name = u'aplicação'
        verbose_name_plural = u'aplicações'


class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    application = models.ForeignKey(Application, verbose_name=u'aplicação')
    name = models.CharField(max_length=60, verbose_name=u'nome')
    description = models.TextField(verbose_name=u'descrição')
    users = models.ManyToManyField(User, verbose_name=u'usuários', blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'perfil'
        verbose_name_plural = u'perfis'
