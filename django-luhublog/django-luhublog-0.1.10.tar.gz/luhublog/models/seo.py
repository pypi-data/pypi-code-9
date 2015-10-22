# -*- encoding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.contrib.sites.models import Site

from model_utils.models import TimeStampedModel

from sorl.thumbnail import ImageField

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from luhublog.models import Author, Blog, Entry

GPLUS_TYPE_CHOICES = (
	('Article', _('Article')),
	('Blog', _('Blog')),
	('Book', _('Book')),
	('Event', _('Event')),
	('LocalBusiness', _('LocalBusiness')),
	('Organization', _('Organization')),
	('Person', _('Person')),
	('Product', _('Product')),
	('Review', _('Review')),
)

#https://dev.twitter.com/cards/types
TWITTER_TYPE_CHOICES = (
	('summary', _('Summary')),
	('summary_large_image', _('Summary large image')),
)

class TwitterCard(TimeStampedModel):

	site = models.CharField(
			verbose_name='twitter:site',
			max_length=30,
			help_text='@empresa')

	creator = models.CharField(
			verbose_name='twitter:creator',
			max_length=30,
			help_text='@autor')

	title = models.CharField(
			verbose_name='twitter:title',
			max_length=70,
			help_text='Máximo 70 caracteres')

	description = models.CharField(
			verbose_name='twitter:description',
			max_length=200,
			help_text='Máximo 200 caracteres')

	image = ImageField(
			verbose_name='twitter:site',
			upload_to="seo/twitter_cards/",
			help_text='Imagen de 280px por 150px')

	image_thumbnail = ImageSpecField(
			source='image',
			processors=[ResizeToFill(280, 150)],
			format='JPEG',
			options={'quality': 70})

	content_type = models.ForeignKey(ContentType)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type', 'object_id')

	class Meta:
		verbose_name= 'Twitter Card'

	def clean(self, *args, **kwargs):
		if not self.site.startswith('@') or not self.creator.startswith('@'):
			raise ValidationError("twitter:site o twitter.author debe comenzar por @")
		super(TwitterCard, self).clean(*args, **kwargs)

	def get_image_url(self):
		site = Site.objects.get_current()
		return "http://%s%s" % (site.domain, self.image_thumbnail.url)

	
# http://ogp.me/#types
OG_TYPE_CHOICES = (
	('article', _('Article')),
	('website', _('Website')),
	('blog', _('Blog')),
	('book', _('Book')),
	('game', _('Game')),
	('movie', _('Movie')),
	('food', _('Food')),
	('city', _('City')),
	('country', _('Country')),
	('actor', _('Actor')),
	('author', _('Author')),
	('politician', _('Politician')),
	('company', _('Company')),
	('hotel', _('Hotel')),
	('restaurant', _('Restaurant')),
)

class OpenGraph(TimeStampedModel):
	
	og_type = models.CharField(
			verbose_name=_('Resource type'), 
			max_length=255, 
			choices=OG_TYPE_CHOICES,
			default="blog"
	)

	og_title = models.CharField(
			_('Open Graph Title'), 
			max_length=255, 
			default='', 
			blank=True,
			help_text='titulo'
	)

	og_description = models.CharField(
			_('Open Graph Description'), 
			max_length=300, 
			default='', 
			blank=True,
			help_text='Facebook can display up to 300 characters, but I suggest treating anything above 200 as something extra.'
	)

	og_app_id = models.CharField(
			_('Facebook App ID'), 
			max_length=255, 
			default='', 
			blank=True
	)

	og_image = ImageField(
			verbose_name='twitter:site',
			upload_to="seo/opengraph/",
			help_text='Imagen de 1200px por 630px')

	og_image_thumbnail = ImageSpecField(
			source='og_image',
			processors=[ResizeToFill(1200, 630)],
			format='JPEG',
			options={'quality': 70})

	content_type = models.ForeignKey(ContentType)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type', 'object_id')

	class Meta:
		verbose_name = "Social Metadata"

	def get_og_image_url(self):
		site = Site.objects.get_current()
		return "http://%s%s" % (site.domain, self.og_image_thumbnail.url)

	@property
	def og_site_name(self):
		blog = Blog.objects.get_blog()
		return blog.title
	




