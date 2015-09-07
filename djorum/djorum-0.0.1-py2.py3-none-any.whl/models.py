# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse

from autoslug import AutoSlugField
from mptt.models import MPTTModel, TreeForeignKey


class Topic(models.Model):
    title = models.CharField(max_length=60)
    description = models.CharField(max_length=255, blank=True, null=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now=True)
    slug = AutoSlugField(unique=True, populate_from='title')
    closed = models.BooleanField(blank=True, default=False, help_text='Only you can post in this Topic, '
                                                                      'Others can still reply to posts)')

    def __str__(self):     # TODO: order these
        return self.title.title()

    def get_absolute_url(self):
        return reverse('forum:topic_posts', args=[self.slug])

    @property # TODO: Whats this?
    def post_count(self):
        return self.post_set.count()

    def last_post(self):
        return self.post_set.last()


class Post(models.Model):
    title = models.CharField(max_length=60)
    body = models.TextField(max_length=1000, blank=True, null=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    modified = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now=True)
    slug = AutoSlugField(unique=True, populate_from='title')
    closed = models.BooleanField(blank=True, default=False)
    topic = models.ForeignKey(Topic, null=True)

    def __str__(self):
        return self.title.title()

    @property
    def reply_count(self):
        return self.reply_set.count()

    @property
    def last_reply(self):
        return self.reply_set.last()

    def get_absolute_url(self):
        if self.topic:
            topic_slug = self.topic.slug
        else:
            topic_slug = None
        return reverse('forum:post', args=[topic_slug, self.slug])


class Reply(MPTTModel):
    body = models.TextField(max_length=10000)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    post = models.ForeignKey(Post)
    topic = models.ForeignKey(Topic)
    user_ip = models.GenericIPAddressField(blank=True, null=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    slug = AutoSlugField(unique=True, populate_from='creator')

    def __str__(self):
        return "%s - %s" % (self.creator, self.post)

    def short(self):
        return "%s \n%s" % (self.creator, self.created.strftime("%b %d, %I:%M %p"))

    short.allow_tags = True

    def get_absolute_url(self):
        return reverse('forum:post', args=[self.post.slug])

    class MPTTMeta:
        order_insertion_by = ['created']


class ProfaneWord(models.Model): # TODO: necessary?
    word = models.CharField(max_length=60)

    def __str__(self):
        return self.word
