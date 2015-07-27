import urllib, os

from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify
from django.db.models import Q
from django.conf import settings

from .manager import LegacyURLManager

class AdminLinkSet( models.Model ):

	title = models.CharField( _("Title"), max_length = 255, blank = False )
	order = models.PositiveIntegerField('Order', null = True,
		help_text="Order in which this link set appears." ) 
	@staticmethod
	def autocomplete_search_fields():
		return ("id__iexact", "title__icontains",)

	def __unicode__(self):
		return self.title

	class Meta:
		ordering = [ 'order']
		verbose_name = "Admin Panel Link Set"
		verbose_name_plural = "Admin Panel Link Sets"


class AdminLinkItem( models.Model ):
	
	parent = models.ForeignKey('AdminLinkSet', blank = True, null = True, on_delete=models.SET_NULL)

	title = models.CharField(_("Display Name"), max_length = 255, blank = False)
	order = models.PositiveIntegerField('Order', null = True,
		help_text="Order in which this link appears in the set." )    

	url = models.CharField(_("URL"), max_length = 255, blank = True,
		help_text="Enter the full path for an external link, i.e. http://www.website.com or relative path for internal link, i.e. /login/" )
		
	class Meta:

		ordering = [ 'order']
		verbose_name = "Link"
		verbose_name_plural = "Links"
 

class LegacyURL( models.Model ):

	title = models.CharField(_("Title (if known)"), max_length = 255, 
		blank = False, null=True)
	url = models.CharField(_("URL"), max_length = 255, blank = False,
		db_index=True)

	#MANUAL
	redirect_to_url = models.CharField(_("Redirect to URL"), max_length = 255, 
		blank = True, null=True)
	
	#RELATED TO OBJECT
	try:
		content_type = models.ForeignKey(ContentType, blank = True, null=True, 
			on_delete=models.SET_NULL,
			limit_choices_to={"model__in": settings.LEGACY_URL_MODEL_CHOICES})		
	except:
		content_type = models.ForeignKey(ContentType, blank = True, null=True, 
			on_delete=models.SET_NULL)

	object_id = models.PositiveIntegerField(blank = True, null=True)
	content_object = generic.GenericForeignKey('content_type', 'object_id')

	_redirect_path = models.CharField(_("Redirect Path (derived)"), 
		max_length = 255, null=True, blank = True)
	
	created = models.DateTimeField ( _("Time created"), auto_now_add = True )
	modified = models.DateTimeField ( _("Time modified"), auto_now = True )

	objects = LegacyURLManager()

	def __unicode__(self):
		return 'Legacy URL %s(%s) -> %s'%(self.title, self.url, self._redirect_path)

	@staticmethod
	def autocomplete_search_fields():
		return ("id__iexact", "url__icontains","title__icontains", "_redirect_path__icontains")
	   
	@property
	def has_redirect_url(self):
		url = self.get_redirect_url()
		if url:
			return True
		return False

	def get_redirect_url(self):
		if self._redirect_path:
			return self._redirect_path
		return self.compute_get_redirect_url()	

	def compute_get_redirect_url(self):
		if self.content_object:
			try:
				url = self.content_object.get_absolute_url()
				return url
			except:
				print "ERROR RETRIEVING ABSOLUTE URL From %s"%(self.content_object)			
		
		return self.redirect_to_url

	def save(self, *args, **kwargs):
		self._redirect_path = self.compute_get_redirect_url()
		super(LegacyURL, self).save(*args, **kwargs)

	@staticmethod
	def create_legacy_url(target_url, target_name, referer_url=None, referer_title=None):
		link, link_created = LegacyURL.objects.get_or_create(url=target_url)

		if link_created or target_url != target_name:
			link.title = target_name
			link.save()


		if referer_url:
			referer_link, referer_created = LegacyURLReferer.objects.get_or_create(legacy_url=link,referer_url=referer_url)
			if referer_created:
				if settings.DEBUG:
					print "Create new referer %s %s to %s"%(referer_title, referer_url, target_url)
				referer_link.referer_title = referer_title
				referer_link.save()

		return link

	class Meta:
		ordering = [ 'url']

class LegacyURLReferer(models.Model):

	legacy_url = models.ForeignKey('LegacyURL')
	referer_title = models.CharField(_("Title (if known)"), max_length = 255, blank = False, null=True)
	referer_url = models.CharField(_("URL"), max_length = 255, blank = False)

	created = models.DateTimeField ( _("Time created"), auto_now_add = True )
	modified = models.DateTimeField ( _("Time modified"), auto_now = True )