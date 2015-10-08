from __future__ import unicode_literals

__author__ = 'vinay'

import datetime

from django.conf import settings
from django.db import models
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from jsonfield import JSONField
from tagging.fields import TagField

from .managers import ContentManager
from .utils import cacheable, stale_cache, get_public_data
from .validators import validate_url_path, validate_and_get_template


class Category(models.Model):
    """Category model."""
    # TODO: Create a migration to add Static Page as first entry
    title = models.CharField(_('title'), max_length=100, unique=True, db_index=True)
    description = models.TextField(_('description'))

    class Meta:
        verbose_name_plural = _('categories')
        ordering = ('title',)

    def __unicode__(self):
        return self.title

    def delete(self, using=None):
        assert self.pk is not 1, (
            'Will not delete {} category. Shit breaks if it happens'.format(self.title)
        )
        super(Category, self).delete(using=using)


def cms_authors():
    User = get_user_model()
    users = User.objects.filter(
        Q(user_permissions__codename='change_content', user_permissions__content_type__app_label='cfblog') |
        Q(groups__permissions__codename='change_content', groups__permissions__content_type__app_label='cfblog') |
        Q(is_superuser=True)).distinct()

    return {'pk__in': users.values('pk')}


class Content(models.Model):
    STATUS_CHOICES = (
        (1, _('Draft')),
        (2, _('Public')),
    )
    url = models.CharField(_('url path'),
                           max_length=255, db_index=True, unique=True, validators=[validate_url_path])
    template = models.CharField(verbose_name=_('template'), max_length=255, validators=[validate_and_get_template])
    status = models.IntegerField(_('status'), choices=STATUS_CHOICES, default=1)
    publish = models.DateTimeField(_('publish'), default=datetime.datetime.now)
    title = models.CharField(_('title'), max_length=200)
    category = models.ForeignKey('Category')
    tags = TagField()
    tease = models.TextField(_('tease'), blank=True,
                             help_text=_('Concise text suggested. Does not appear in RSS feed.'))
    # TODO: Include S3ImageField
    # thumbnail = ImageWithThumbsField(upload_to=get_image_path, sizes=(('s', 500, 500), ('r', 450, 600), ('t', 200, 260)), null=True, blank=True)
    notes_todos = models.TextField(_('Notes and Todos'), blank=True)
    auth_data = JSONField(verbose_name=_('author data'), default={},
                          help_text=_("Don't edit this unless you know what this means"))
    public_data = JSONField(verbose_name=_('public data'), default={},
                            help_text=_("Don't edit this unless you know what this means"))
    author = models.ForeignKey(settings.AUTH_USER_MODEL, limit_choices_to=cms_authors)
    created_on = models.DateTimeField(_('created on'), auto_now_add=True)
    modified_on = models.DateTimeField(_('modified on'), auto_now=True)
    objects = ContentManager()

    class Meta:
        ordering = ('-publish',)
        get_latest_by = 'publish'

    @property
    def is_public(self):
        return self.status == 2

    def publish_cms_content(self):
        self.public_data = self.auth_data
        self.status = 2
        self.save()

    def __unicode__(self):
        return self.title

    @cacheable('cfblog_content_{id}')
    def html(self):
        return get_public_data(self)

    @stale_cache('cfblog_content_{id}')
    def save(self, *args, **kwargs):
        super(Content, self).save(*args, **kwargs)

    def get_previous_post(self):
        return self.get_previous_by_publish(Q(status__gte=2), ~Q(category_id=1))

    def get_next_post(self):
        return self.get_next_by_publish(Q(status__gte=2), ~Q(category_id=1))

    def get_absolute_url(self):
        return self.url
