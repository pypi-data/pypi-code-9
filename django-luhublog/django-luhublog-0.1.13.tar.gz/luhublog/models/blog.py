# -*- encoding: utf-8 -*-

from datetime import datetime, timedelta

from django.db import models
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse

from model_utils.models import TimeStampedModel

class BlogManager(models.Manager):
	def get_blog(self):
		site = Site.objects.get_current()
		blog = self.filter(site=site)
		if len(blog) > 0:
			return blog[0]
		return None

class Blog(TimeStampedModel):

	title = models.CharField(
				verbose_name='Nombre del blog',
				max_length=60)
	tag_line = models.CharField(
				verbose_name='Descripción del blog',
				max_length=140)
	entries_per_page = models.IntegerField(
				verbose_name='Entradas por pagina',
				default=10)
	recents = models.IntegerField(
				verbose_name='Numero de entradas recientes a mostrar',
				default=5)

	site = models.OneToOneField(
				Site,
				verbose_name='Site')

	objects = BlogManager()

	def __unicode__(self):
		return self.title

	def save(self, *args, **kwargs):
		super(Blog, self).save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse('luhublog-detail')

	@property
	def full_url(self):
		return "http://%s%s" % ( self.site.domain, self.get_absolute_url() )

	def get_recents_entries(self):
		return self.entry_set.all()[:blog.recents]


class BlogSocialMedia(TimeStampedModel):
	blog = models.OneToOneField(Blog, verbose_name='Blog', related_name='social_media')

	facebook = models.URLField(verbose_name='Facebook URL', blank=True) 
	twitter = models.URLField(verbose_name='Twitter URL', blank=True)
	google_plus = models.URLField(verbose_name='Google plus URL', blank=True)
	instagram = models.URLField(verbose_name='Instagram URL', blank=True)
	linkedin = models.URLField(verbose_name='Linkedin URL', blank=True)
	youtube = models.URLField(verbose_name='YouTube URL', blank=True)
	pinterest = models.URLField(verbose_name='Pinterest URL', blank=True)

	class Meta:
		verbose_name='Red social del blog'
		verbose_name='Redes sociales de los blogs'

	def get_username_twitter(self):
		if self.twitter:
			twitter_base = "twitter.com/"
			twitter_url = self.twitter
			if not twitter_url.find(twitter_base) == -1:
				username = twitter_url[ twitter_url.find(twitter_base) + len(twitter_base) : ]
				if username.endswith('/'):
					username = username[:len(username)-1]
					return username
				return username
			else:
				return None
		else:
			return None


	



