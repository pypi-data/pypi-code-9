import json
from mimetypes import MimeTypes
import urllib

from django.contrib import admin
from django.contrib import messages
from django.contrib.auth.admin import UserAdmin as ContribUserAdmin
from django.contrib.admin.filters import SimpleListFilter
from django.contrib.admin.models import LogEntry, ADDITION
from django.contrib.admin.widgets import AdminFileWidget
from django.contrib.admin.util import flatten_fieldsets
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.db.models import get_model



from .models import *
from .forms import *

csrf_protect_m = method_decorator(csrf_protect)
sensitive_post_parameters_m = method_decorator(sensitive_post_parameters())


class TagListFilter(SimpleListFilter):
    title = 'tag'
    parameter_name = 'tag'
    def lookups(self, request, model_admin):

      media_tag_model = get_model(settings.MEDIA_TAG_MODEL.split('.')[0], settings.MEDIA_TAG_MODEL.split('.')[1])
      tags = media_tag_model.objects.all()
      items = ()
      for tag in tags:
        items += ((str(tag.id), str(tag.title),),)
      return items

    def queryset(self, request, queryset):
      tag_id = request.GET.get(self.parameter_name, None)
      if tag_id:
        return queryset.filter(tags=tag_id)
      return queryset

class HasImageFilterSpec(SimpleListFilter):
  title = u'Has Image'
  parameter_name = u'_has_image'

  def lookups(self, request, model_admin):
    return (
      ('1', _('Has Image'), ),
      ('0', _('Doesn\'t have Image'), ),
    )

  def queryset(self, request, queryset):
    kwargs = {
    '%s'%self.parameter_name : None,
    }
    if self.value() == '0':
      return queryset.filter( image__exact = '' )  
    if self.value() == '1':
      return queryset.exclude( image__exact = '' )  
      
    return queryset

class HasIconImageFilterSpec(SimpleListFilter):
  title = u'Has Icon Image'
  parameter_name = u'_has_icon_image'

  def lookups(self, request, model_admin):
    return (
      ('1', _('Has Icon Image'), ),
      ('0', _('Doesn\'t have Icon Image'), ),
    )

  def queryset(self, request, queryset):
    kwargs = {
    '%s'%self.parameter_name : None,
    }
    if self.value() == '0':
      return queryset.filter( image__isnull=True )  
    if self.value() == '1':
      return queryset.exclude( image__isnull=True )  
      
    return queryset        

class HasFileFilterSpec(SimpleListFilter):
  title = u'Has File'
  parameter_name = u'_file_image'

  def lookups(self, request, model_admin):
    return (
      ('1', _('Has File'), ),
      ('0', _('Doesn\'t have File'), ),
    )

  def queryset(self, request, queryset):
    kwargs = {
    '%s'%self.parameter_name : None,
    }
    if self.value() == '0':
      return queryset.filter( media_file__exact = '' )  
    if self.value() == '1':
      return queryset.exclude( media_file__exact = '' )  
      
    return queryset        


class BaseMediaTagAdmin(admin.ModelAdmin):

  autocomplete_lookup_fields = {
    'fk': ['created_by','modified_by']
  }
  raw_id_fields = ('created_by','modified_by',)

  prepopulated_fields = {"slug": ("title",)}
  fieldsets = (
    ( 'Media', 
      { 'fields': ( 
        ('title','slug'),
        'admin_description'
      ) 
    } ),
    ("Meta", {
      'fields': (
        ('created','created_by',),   
        ('modified','modified_by',),             
      ),
      'classes': ( 'grp-collapse', )
    })        
  )
  list_display = ( 'title','slug', )
  
  readonly_fields  = ('created','modified',) 
  search_fields = ("title", "admin_description",)
  csv_fields = flatten_fieldsets(fieldsets)  

  def save_model(self, request, obj, form, change):
    if not getattr(obj, "created_by"):
      obj.created_by = request.user
    obj.modified_by = request.user
    super(BaseMediaTagAdmin, self). save_model(request, obj, form, change)

class BaseImageAdmin(admin.ModelAdmin):

  form = BaseAdminImageAddForm

  autocomplete_lookup_fields = {
    'fk': ['creator'],
    'm2m': ['users','tags']
  }
  raw_id_fields = ('creator','users','tags')
   
  fieldsets = (
    ( 'Media', { 'fields': ( 
      ('admin_thumbnail','image',),
      ('image_variants','image_variant_shortlinks'),
      ('width', 'height'),
      ('display_size', 'size'),
      'title',
      'credit',
      'caption', 
      'alt', 
      'clean_filename_on_upload',
      'allow_file_to_override',
      'use_png',
      'admin_description',
      'legacy_url',
      'tags'
      ) 


    } ),   
    ("Meta", {
      'fields': (
        ('created','modified',),
        ('creator','users',),                
      ),
      'classes': ( 'grp-collapse', )
    })      
  )




  list_display = ( 'admin_file','admin_thumbnail','pk', 'title', 'caption',
    'credit', 'admin_description', 'width', 'height', 'display_size', 'size', 
    'created', 'modified','tag_list')
  list_editable = ('admin_description',)
  list_display_links = ('pk', 'title', 'caption', 'credit',)
  list_filter = ['creator','users', 'is_searchable', TagListFilter, 
    HasImageFilterSpec, 'created']
  sortable_field_name = ('admin_thumbnail',)
  readonly_fields  = ('admin_file','created','modified','admin_thumbnail','image_variants', 
    'image_variant_shortlinks', 'display_size', 'size', 'width', 'height', 'tag_list')
  search_fields = ("title", "caption", "credit", "admin_description", 
    "legacy_url")
  csv_fields = flatten_fieldsets(fieldsets)  
  
  

  def administrative_description(self, obj):
    return obj.admin_description
  administrative_description.allow_tags = True

  def admin_thumbnail(self, obj):
    if obj.image:
      try:
        return "<img src='%s' />"%(obj.thumbnail.url)
      except:
        return "Error displaying image"
  admin_thumbnail.allow_tags = True

  def admin_file(self, obj):
    if obj.image:
      return obj.image
    return ''

  def image_variants(self, obj):
    if obj.image:
      base_image =  '<a href="%s">Original Size (%spx x %spx)</a><br />'%(obj.image_url, obj.image_width, obj.image_height)
      for variant in obj.__class__.variants:
        gussied_name = variant.replace("_", " ").title()
        base_image +=  '<a href="%s">%s (%spx x %spx)</a><br />'%(obj.get_variant_url(variant), gussied_name, obj.get_variant_width(variant), obj.get_variant_height(variant))

      return base_image
  image_variants.allow_tags = True


  def image_variant_shortlinks(self, obj):
    if obj.image:
      try:
        url = reverse('image_variant_redirect_view', kwargs={'pk':obj.pk, 'variant_name':'image'})          
        base_image =  '<a href="%s">Original Size (%spx x %spx)</a><br />'%(url, obj.image_width, obj.image_height)
        for variant in obj.__class__.variants:
          gussied_name = variant.replace("_", " ").title()
          url = reverse('image_variant_redirect_view', kwargs={'pk':obj.pk, 'variant_name':variant})                
          base_image +=  '<a href="%s">%s (%spx x %spx)</a><br />'%(url, gussied_name, obj.get_variant_width(variant), obj.get_variant_height(variant))
        return base_image
      except:
        return "Not implemented."
  image_variant_shortlinks.allow_tags = True

  def tag_list(self, obj):
    
    output = ''
    all_tags = obj.tags.all()
    if len(all_tags) > 1:
      output += '<span>Tags: </span>'

    elif len(all_tags) > 0:
      output += '<span>Tag: </span>'

    for tag in all_tags:
      output += ('<a href="?tags__id__exact=%s">%s</a> '%(tag.pk, tag.title))
    return output

  tag_list.allow_tags = True

  def get_form(self, request, obj=None, **kwargs):
    form = super(BaseImageAdmin, self).get_form(request, obj, **kwargs)
    form.base_fields['creator'].initial = request.user
    form.base_fields['users'].initial = [request.user]
    form.base_fields['image'].required = False
    return form

  def add_view(self, request, form_url='', extra_context=None):
    default_response = super(BaseImageAdmin, self).add_view(request, form_url, extra_context)

    if request.method == 'POST' and "batch" in request.POST:

      response = batch_upload_image_response(request)
      if response != None:
        return response

    return default_response


def batch_upload_image_response(request):
  try:
    latest_log_entry = LogEntry.objects.filter(action_flag=ADDITION).order_by('-action_time')[0]
    ct = ContentType.objects.get_for_id(latest_log_entry.content_type_id)
    obj = ct.get_object_for_this_type(pk=latest_log_entry.object_id)
    if obj:
      
      mime = MimeTypes()
      url = urllib.pathname2url(obj.image_url)
      mime_type = mime.guess_type(url)
      data = {
        "files":[
          {
            "url": obj.image_url,
            "thumbnailUrl": obj.thumbnail_url,
            "name": obj.title,
            "type": mime_type[0],
            "size": obj.image.size
          }
        ]
      }
      return HttpResponse(json.dumps(data), content_type='application/json')
  except:
    return None




class BaseDocumentAdmin(admin.ModelAdmin):

  form = BaseAdminDocumentAddForm
  
  autocomplete_lookup_fields = {
    'fk': ['creator','image'],
    'm2m': ['users', 'tags']
  }
  raw_id_fields = ('creator','image','users', 'tags')
   
  fieldsets = (
    ( 'Media', { 'fields': ( 
      ('media_file',),
      ('admin_thumbnail','image',),
      ('display_size', 'size'),
      'title',
      'is_searchable',
      'clean_filename_on_upload',
      'allow_file_to_override',
      ('admin_description',),
      'legacy_url',
      'tags'
      ) 
    } ),
    ("Meta", {
      'fields': (
        ('created','modified',),
        ('creator','users',),                
      ),
      'classes': ( 'grp-collapse', )
    })        
  )
  list_display = ( 'admin_thumbnail', 'title', 'admin_description', 
    'display_size', 'size','created', 'modified', 'tag_list','redirect_link', )
  
  list_display_links = ('admin_thumbnail', 'title', )
  list_filter = ['creator','users', 'is_searchable', 'tags', 
  HasFileFilterSpec, HasIconImageFilterSpec]

  readonly_fields  = ('created','modified','admin_thumbnail','redirect_link', 
    'display_size', 'size', 'tag_list') 
  search_fields = ("title", "admin_description", "legacy_url")
  csv_fields = flatten_fieldsets(fieldsets)  

  def redirect_link(self, obj):
    try:
      url = obj.get_redirect_link()
      if url:
        return "Redirect Shortlink: <a href='%s'>%s</a>"%(url, url)
      else:
        return ''
    except:
      return ''
  redirect_link.allow_tags = True
  

  def admin_thumbnail(self, obj):
    if obj.image:
      if obj.image.image:
        try:
          return "<img src='%s' />"%(obj.image_thumbnail_url)
        except:
          return "Error displaying Image"
  admin_thumbnail.allow_tags = True

  def tag_list(self, obj):
    
    output = ''
    all_tags = obj.tags.all()
    if len(all_tags) > 1:
      output += '<span>Tags: </span>'

    elif len(all_tags) > 0:
      output += '<span>Tag: </span>'

    for tag in all_tags:
      output += ('<a href="?tags__id__exact=%s">%s</a> '%(tag.pk, tag.title))
    return output

  tag_list.allow_tags = True

  def get_form(self, request, obj=None, **kwargs):
    form = super(BaseDocumentAdmin, self).get_form(request, obj, **kwargs)
    form.base_fields['creator'].initial = request.user
    form.base_fields['users'].initial = [request.user]
    return form

  def add_view(self, request, form_url='', extra_context=None):
    default_response = super(BaseDocumentAdmin, self).add_view(request, 
      form_url, extra_context)

    if request.method == 'POST' and "batch" in request.POST:

      response = batch_upload_document_response(request)
      if response != None:
        return response

    return default_response


def batch_upload_document_response(request):
  try:
    latest_log_entry = LogEntry.objects.filter(action_flag=ADDITION).order_by('-action_time')[0]
    ct = ContentType.objects.get_for_id(latest_log_entry.content_type_id)
    obj = ct.get_object_for_this_type(pk=latest_log_entry.object_id)
    if obj:
      
      mime = MimeTypes()
      url = urllib.pathname2url(obj.media_url)
      mime_type = mime.guess_type(url)
      data = {
        "files":[
          {
            "url": obj.media_url,
            "thumbnailUrl": obj.image_thumbnail_url,
            "name": obj.title,
            "type": mime_type[0],
            "size": obj.media_file.size
          }
        ]
      }
      return HttpResponse(json.dumps(data), content_type='application/json')
  except:
    return None

class BaseSecureDocumentAccessInline(admin.StackedInline):
  
  def share_link(self, obj):
    if obj.pk:
      path = obj.get_share_url()
      return '<a href="{0}">{1}</a>'.format(path, path)
    else:
      return 'Click "Save and continue editing" to generate share URL'
  share_link.allow_tags = True

  form = SecureDocumentItemChangeForm

  extra = 0

  classes = ('grp-collapse grp-open',)
  inline_classes = ('grp-collapse grp-open',)


  fields = (
    ('title','description',),
    ('password'),
    ('expiration_date','share_link'),        
  )
  readonly_fields = ('share_link',)

  verbose_name = "Document Share Settings"
  verbose_name_plural = "Document Share Settings"
  
  

class BaseSecureDocumentAdmin(BaseDocumentAdmin):

  def get_secure_url(self, obj):
    url = obj.get_secure_url()
    if url:
      sets_url = reverse("admin:media_securedocumentset_changelist")
      return "<a href='%s'>Download</a>\
        <br /><br />Do not share this link with non-staff as it will \
        expire after %s seconds.<br />\
        Instead, use the share settings below to generate a link to \
        share outside the organization.\
        <br />To share multiple files at once, go to <a href='%s'>\
        Secure Document Sets</a>"%(url, settings.SECURE_DOCUMENT_LINK_LIFE,  sets_url)
    return ''
  get_secure_url.allow_tags = True

  list_display = ( 'admin_thumbnail', 'title', 'admin_description', 
    'display_size', 'size', 'created', 'modified', 'get_secure_url', )
  readonly_fields  = ('created','modified','admin_thumbnail','redirect_link', 
    'slug', 'get_secure_url', 'display_size', 'size') 
  fieldsets = (
    ( 'Media', { 'fields': ( 
      ('media_file',),
      ('admin_thumbnail','image',),
      ('display_size', 'size'),
      'title',
      'slug',
      'clean_filename_on_upload',
      'allow_file_to_override',
      'get_secure_url',
      'legacy_url',
      ('admin_description',),
      'tags',
      ) 
    } ),
    ("Meta", {
      'fields': (
        ('created','modified',),
        ('creator','users',),                
      ),
      'classes': ( 'grp-collapse', )
    })        
  )
  csv_fields = flatten_fieldsets(fieldsets)  

  def add_view(self, request, form_url='', extra_context=None):
    default_response = super(BaseSecureDocumentAdmin, self).add_view(request, form_url, extra_context)

    # print 'getting secure admin method? %s batch in request? %s'%(request.method, ("batch" in request.POST))
    if request.method == 'POST' and "batch" in request.POST:

      response = batch_upload_secure_document_response(request)
      if response != None:
        return response

    return default_response


def batch_upload_secure_document_response(request):
  try:
    latest_log_entry = LogEntry.objects.filter(action_flag=ADDITION).order_by('-action_time')[0]
    ct = ContentType.objects.get_for_id(latest_log_entry.content_type_id)
    obj = ct.get_object_for_this_type(pk=latest_log_entry.object_id)
    if obj:
      
      mime = MimeTypes()
      url = urllib.pathname2url(obj.media_url)
      mime_type = mime.guess_type(url)
      data = {
        "files":[
          {
            "url": obj.get_secure_url(),
            "thumbnailUrl": obj.image_thumbnail_url,
            "name": obj.title,
            "type": mime_type[0],
            "size": obj.media_file.size
          }
        ]
      }
      return HttpResponse(json.dumps(data), content_type='application/json')
  except:
    return None

class BaseSecureDocumentSetItemAdmin(admin.TabularInline):
  extra = 0
  
  autocomplete_lookup_fields = {
    'fk': ['document'],
    'm2m': []
  }
  raw_id_fields = ('document',)
  ordering = ('order',)

class BaseSecureDocumentSetAdmin(admin.ModelAdmin):
  change_password_form_template = None
  inlines = [
    BaseSecureDocumentSetItemAdmin,
  ]

  form = SecureDocumentSetChangeForm
  add_form = SecureDocumentSetCreateForm

  autocomplete_lookup_fields = {
    'fk': ['creator'],
    'm2m': ['users']
  }
  raw_id_fields = ('creator','users',)
  

  def get_share_url(self, obj):
    url = obj.get_secure_url()
    if url:
      return "Share Link <a href='%s'>%s</a>"%(url, url)
    return ''
  get_share_url.allow_tags = True

  list_display = ('title', 'slug', 'get_share_url')
  
  fieldsets = (
    ( 'Core', { 'fields': ( 
      'title',
      'description',
      'password',
      ('expiration_date', 'get_share_url')
      
      ) 
    } ),
    ("Meta", {
      'fields': (
        ('created','modified',),
        ('creator','users',),                
      ),
      'classes': ( 'grp-collapse', 'grp-closed' )
    })        
  )
  readonly_fields = ('created', 'modified', 'get_share_url',)
  csv_fields = flatten_fieldsets(fieldsets)  

