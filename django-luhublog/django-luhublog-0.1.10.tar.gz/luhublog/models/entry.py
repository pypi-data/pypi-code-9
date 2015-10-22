# -*- encoding: utf-8 -*-

import os
import bleach

from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.text import Truncator
from django.utils.html import strip_tags
from django.utils.html import linebreaks
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible
from django.utils.text import Truncator
from django.templatetags.static import static
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site

from froala_editor.fields import FroalaField

from sorl.thumbnail import ImageField
from sorl.thumbnail import get_thumbnail

from taggit.managers import TaggableManager

from bs4 import BeautifulSoup

from model_utils.models import TimeStampedModel
from model_utils import Choices
from model_utils.fields import StatusField

from luhublog.managers import entries_published, EntryPublishedManager
from luhublog.models import Blog, Author

def rename_filename(instance, filename):
	file_name, file_extension = os.path.splitext(filename)
	file_name = slugify(filename)
	file_name = file_name[:-(len(file_extension)-1)]
	folder = instance.__class__.__name__.lower()
	return "blog/%s/%s%s" % (folder, file_name, file_extension)


class EntryCategory( TimeStampedModel):

	blog = models.ForeignKey(
					Blog,
					verbose_name='Site',
					blank=True,
					editable=False)

	name = models.CharField(
					verbose_name='Nombre',
					max_length=60)
	slug = models.SlugField(
					verbose_name='ULR Slug')

	description = models.CharField(
					verbose_name='Descripción',
					max_length=255,
					blank=True)

	image_cover = ImageField(
					verbose_name='Imagen de portada',
					upload_to=rename_filename,
					blank=True,
					null=True)

	tags = TaggableManager(
					blank=True)

	class Meta:
		verbose_name = 'Categoría'
		verbose_name_plural = "Categorías"

	def __unicode__(self):
		return self.name

	def save(self, *args, **kwargs):
		if not self.id:
			self.blog = Blog.objects.get_blog()
		super(EntryCategory, self).save(*args, **kwargs)


class Entry( TimeStampedModel):

	blog = models.ForeignKey(
					Blog,
					verbose_name='Site',
					blank=True,
					editable=False)

	STATUS = Choices('DRAFT', 'HIDDEN', 'PUBLISHED')

	category = models.ForeignKey(
					EntryCategory,
					verbose_name='Categoría',
					blank=True,
					null=True)

	title = models.CharField(
					verbose_name='title', 
					max_length=100)

	slug = models.SlugField(
					verbose_name='slug', 
					unique=True,
					help_text="Used to build the entry's URL.")
	
	lead_entry = models.CharField(
					verbose_name='Encabezado',
					max_length=255,
					blank=True)

	image_header = ImageField(
					verbose_name='Imagen de encabezado',
					upload_to=rename_filename,
					blank=True,
					null=True)
	
	image_caption = ImageField(
					verbose_name='Imagen de la entrada',
					upload_to=rename_filename,
					blank=True,
					null=True)

	content = FroalaField(
					verbose_name='Cuerpo de la entrada')

	status = StatusField()

	author = models.ForeignKey(
					Author,
					verbose_name='Autor de la entrada',
					related_name='entries')

	start_publication = models.DateTimeField(
					verbose_name='Fecha de publicación',
					db_index=True, 
					blank=True, 
					null=True)

	related = models.ManyToManyField(
		'self',
		blank=True,
		verbose_name=_('related entries'))

	# SEO

	seo_title = models.CharField(
			verbose_name='Meta Title',
			max_length=60,
			blank=True,
			default="",
			help_text='Google typically displays the first 50-60 characters of a title tag'
	)

	seo_description = models.CharField(
			verbose_name='Meta Description',
			max_length=155, 
			default='', 
			blank=True,
			help_text='The description should optimally be between 10-155 characters'
	)

	seo_keywords = models.CharField(
			verbose_name='Meta Keywords',
			max_length=400, 
			default='', 
			blank=True,
			help_text='Opcional'
	)

	objects = EntryPublishedManager()
	default = models.Manager()

	tags = TaggableManager(
					blank=True)

	class Meta:
		"""
		Entry's meta informations.
		"""
		ordering = ['-created']
		get_latest_by = '-start_publication'
		verbose_name = _('Entrada')
		verbose_name_plural = _('Entradas')
		index_together = [['slug', 'created'],
						  ['status', 'created', 'start_publication']]

	@property
	def status_display(self):
		return self.STATUS[self.status]

	@property
	def publication_date(self):
		"""
		Return the publication date of the entry.
		"""
		return self.start_publication or self.created

	@property
	def is_actual(self):
		"""
		Checks if an entry is within his publication period.
		"""
		now = timezone.now()
		if self.start_publication and now < self.start_publication:
			return False
		return True

	@property
	def is_visible(self):
		"""
		Checks if an entry is visible and published.
		"""
		return self.is_actual and self.status == PUBLISHED

	@property
	def previous_entry(self):
		"""
		Returns the previous published entry if exists.
		"""
		return self.previous_next_entries[0]

	@property
	def next_entry(self):
		"""
		Returns the next published entry if exists.
		"""
		return self.previous_next_entries[1]

	@property
	def previous_next_entries(self):
		"""
		Returns and caches a tuple containing the next
		and previous published entries.
		Only available if the entry instance is published.
		"""
		previous_next = getattr(self, 'previous_next', None)

		if previous_next is None:
			if not self.is_visible:
				previous_next = (None, None)
				setattr(self, 'previous_next', previous_next)
				return previous_next

			entries = list(self.__class__.published.all())
			index = entries.index(self)
			try:
				previous = entries[index + 1]
			except IndexError:
				previous = None

			if index:
				next = entries[index - 1]
			else:
				next = None
			previous_next = (previous, next)
			setattr(self, 'previous_next', previous_next)
		return previous_next

	# @property
	# def short_url(self):
	#     """
	#     Returns the entry's short url.
	#     """
	#     return get_url_shortener()(self)

	@property
	def word_count(self):
		"""
		Counts the number of words used in the content.
		"""
		return len(strip_tags(self.content).split())

	@property
	def related_published(self):
		"""
		Returns only related entries published.
		"""
		return entries_published(self.related)

	@property
	def summary(self):
		short = bleach.clean(self.content, tags=bleach.ALLOWED_TAGS, strip=True)
		return Truncator(short).chars(200)

	def get_image_caption(self):
		if self.image_caption:
			return self.image_caption.url

		soup = BeautifulSoup(self.content, "html.parser")
		img = soup.img
		if img:
			url = img.attrs.get('src')
			return url
		return static( settings.BLOG_ENTRY_CAPTION_DEFAULT )

	def get_image_header(self):
		if self.image_header:
			return self.image_header.url
		return None

	def save(self, *args, **kwargs):

		if not self.id:
			self.blog = Blog.objects.get_blog()

		if self.status == "PUBLISHED" and not self.start_publication:
			self.start_publication = timezone.now()
		super(Entry, self).save(*args, **kwargs)

	# @models.permalink
	def get_absolute_url(self):
		return reverse('luhublog-detail', kwargs={ 'slug' : self.slug } )

	@property
	def full_url(self):
		return "http://%s%s" % (self.blog.site.domain, self.get_absolute_url() )
	

	def __str__(self):
		title = Truncator(self.title).chars(30)
		return '%s: %s' % (title, self.status_display)

