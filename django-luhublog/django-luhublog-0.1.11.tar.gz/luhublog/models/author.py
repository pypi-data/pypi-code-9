# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from model_utils.models import TimeStampedModel
from model_utils.managers import QueryManager

from luhublog.managers import entries_published


@python_2_unicode_compatible
class Author( TimeStampedModel ):

    user = models.OneToOneField(
                settings.AUTH_USER_MODEL,
                verbose_name='Perfil de usuario',
                related_name='weblog_author')

    name = models.CharField(
                verbose_name='Nombre / seudónimo del autor',
                max_length=200,
                blank=True,
                default="")

    headline = models.CharField(
                verbose_name='Corta descripción',
                max_length=255,
                blank=True,
                default="")

    twitter = models.CharField(
                verbose_name='Twitter',
                max_length=50,
                help_text='@EsLuhu',
                blank=True,
                default="")

    facebook_page_url = models.URLField(
                verbose_name='URL Pagina Facebook',
                blank=True)

    twitter_url = models.URLField(
                verbose_name='URL Perfil Facebook',
                blank=True)

    google_plus_url = models.URLField(
                verbose_name='URL Perfil Google Plus',
                blank=True)


    is_active = models.BooleanField(
                _("is active"),
                default=True)

    objects = models.Manager()
    activated = QueryManager(is_active=True).order_by('-created')

    class Meta:
        """
        Author's meta informations.
        """
        ordering = ['-created',]
        verbose_name = 'Autor'
        verbose_name_plural = 'Autores'

    def __str__(self):
        """
        If the user has a full name, use it instead of the username.
        """
        if not self.name:
            name = self.user.get_full_name()
            if name == "":
                return self.user.email
            return name
        return self.name

    def save(self, *args, **kwargs):
        if self.twitter:
            if not self.twitter[0] == "@":
                self.twitter = "@"+self.twitter
        super(Author, self).save(*args, **kwargs)

    @property
    def full_name(self):
        if not self.name == "":
            return self.name
        return self.user.get_full_name()
            
    def entries_published(self):
        """
        Returns author's published entries.
        """
        return entries_published(self.entries)