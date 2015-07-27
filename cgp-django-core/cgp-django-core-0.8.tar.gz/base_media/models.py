import urllib, os
import time
import uuid

from django.conf import settings
from django.core.files.temp import NamedTemporaryFile
from django.core.files import File
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import pre_save
from django.db.models import get_model
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.utils.module_loading import import_by_path
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.hashers import (
    check_password, make_password, is_password_usable)

import boto
from boto.s3.connection import S3Connection, Bucket, Key

from imagekit import ImageSpec
from imagekit.models import ImageSpecField
from imagekit.models import ProcessedImageField
from imagekit.admin import AdminThumbnail
from imagekit.processors import ResizeToFill, ResizeToFit

from .utils import unique_slugify


def generate_object_slug(instance, length=10):
    return uuid.uuid1().hex[:length]

def is_incremented_file(original, updated):
    """
    Return True if files are incremented versions of eachother: avatar.png, avatar-1.png, avatar-436.png
    """
    try:
        original_path_pieces = original.split(".")
        updated_path_pieces = updated.split(".")

        original_path_start = original_path_pieces[0].split("-")
        updated_path_start = updated_path_pieces[0].split("-")
        # print 'original_path_start: %s updated_path_start: %s'%(original_path_start, updated_path_start)

        are_same_start_path = original_path_start[0] == updated_path_start[0]
        # print 'are_same_start_path? %s == %s? %s'%(original_path_start[0], updated_path_start[0], are_same_start_path)
        if are_same_start_path==False:
            return False

        original_is_integer = True if len(original_path_start)==1 else isinstance( int(original_path_start[1]), int )
        updated_is_integer = True if len(updated_path_start)==1 else isinstance( int(updated_path_start[1]), int )
        increments_are_integers = original_is_integer and updated_is_integer

        # print 'increments_are_integers? %s , %s? %s'%(original_is_integer, updated_is_integer, increments_are_integers)
        if increments_are_integers==False:
            return False

        return True

    except:
        return False



def _media_file_name( instance, filename, file_attribute_name, folder, model_name ):
    
    file, extension = os.path.splitext( filename )
    media_file = getattr(instance, file_attribute_name)

    if instance.clean_filename_on_upload:
        
        filename     = "%s%s"%(slugify(file[:245]), extension)
        filename     = filename.lower()

    full_path = '/'.join( [ folder, filename ] )
    exists = media_file.storage.exists(full_path)

    #If we are changing the image, delete the previous image:
    if instance.pk:
        media_model = get_model(model_name.split('.')[0], model_name.split('.')[1])
        current_instance = media_model.objects.get(pk=instance.pk)
        current_path = str(current_instance.image)

        if full_path != current_path:
            if is_incremented_file(full_path, current_path) == False:
                # print 'Delete previous media: %s'%(current_path)
                current_media_file = getattr(current_instance, file_attribute_name)
                current_media_file.storage.delete(current_path)

    
    #Handle case if file of the same name already exists
    if exists:
        if instance.allow_file_to_override==True:
            # print 'Delete media with same name: %s'%(full_path)
            media_file.storage.delete(full_path)
        else:
            counter = 1
            starting_path = full_path
            while exists == True:
                counter += 1
                full_path = starting_path.replace(extension, '-%s%s'%(counter, extension))
                exists = media_file.storage.exists(full_path)
            # print 'Increment filename to get unique: %s'%(full_path)

    

    return full_path


def image_title_file_name( instance, filename ):    

    folder = '/'.join( [ 'media', 'image' ] )
    full_path = _media_file_name(instance, filename, 'image', folder, settings.IMAGE_MODEL)
    return full_path


def document_file_name( instance, filename ):
    
    folder = '/'.join( [ 'media', 'document' ] )
    full_path = _media_file_name(instance, filename, 'media_file', folder, settings.DOCUMENT_MODEL)
    return full_path


def gussy_path(url):
    
    file, extension = os.path.splitext( url )

    split = file.split('/')
    file_name = split[-1]
    file_name = file_name.replace("_", "-")
    words = file_name.split("-")
    cleaned_extension = u"(%s)"%extension[1:].upper() if len(extension) > 0 else ''
    combined = ' '.join(words).title()

    return u"%s %s"%(combined, cleaned_extension)   

def displaybytes(bytes):
    if bytes < 1024:
        return "%sB"%(bytes)
    kb = (bytes / 1024)
    if kb < 1024:
        return '%sKB'%(kb)

    mb = (kb / 1024)
    if mb < 1024:
        return '%sMB'%(mb)

    gb = (mb / 1024)
    return '%sGB'%(gb)


class BaseMediaTag(models.Model):

    title = models.CharField(_('Title'), max_length=255)
    slug = models.CharField(_('Unique Text ID'), max_length=255, blank=True, 
        unique=True, db_index=True)

    admin_description = models.TextField(_("Administrative Description"), blank = True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, 
        null=True, related_name='%(class)s_created_by', on_delete=models.SET_NULL)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, 
        null=True, related_name='%(class)s_modified_by', on_delete=models.SET_NULL)

    created = models.DateTimeField(_('Created Date'), auto_now_add=True, 
        blank=True, null=True)
    modified = models.DateTimeField(_('Modified Date'), auto_now=True, 
        blank=True, null=True)

    @property
    def page_title(self):
        return self.title

    def save(self, *args, **kwargs):

        # -- Make sure slug is unique
        if self.slug and self.slug != '':
            unique_slugify(self, self.slug)
        elif self.title and self.title != '':
            unique_slugify(self, self.title)  
        else:
            unique_slugify(self, "Untitled %s"%(self.__class__.__name__))    

        # -- Always lowercase slug:
        if self.slug:
            self.slug = self.slug.lower()
        
        super(BaseMediaTag, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return self.title

    class Meta:
        abstract = True
 

class BaseMedia( models.Model ):

       
    title = models.CharField(_("title"), max_length=255, help_text="Title is required", blank=True, null=True)

    try:
        is_searchable = models.BooleanField( _("Is Searchable"), default = settings.MEDIA_SEARCHABLE_BY_DEFAULT, help_text="Allow this file to be indexed and searchable by the public.")
    except:
        is_searchable = models.BooleanField( _("Is Searchable"), default = False, help_text="Allow this file to be indexed and searchable by the public.")

    clean_filename_on_upload = models.BooleanField( _("Clean filename on upload"), default = True, help_text="This removes spaces, special characters, and capitalization from the file name for more consistent naming." )

    allow_file_to_override = models.BooleanField( _("Allow file to override exiting file with the same name"), default = True )

    legacy_url = models.CharField(_("Legacy URL"), max_length=255, blank=True, db_index=True)    

    # -- Meta Data
    admin_description = models.TextField(_("Administrative Description"), blank = True, 
        help_text='Add administrative description to help others find and use this element.' )
    
    size = models.BigIntegerField(null=True, blank=True, help_text='File size in bytes')
    display_size = models.CharField(_("Display Size"), max_length=255, blank=True, null=True)   

    creator = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_(u"Creator"), blank=True, null=True, related_name="%(app_label)s_%(class)s_related", on_delete=models.SET_NULL)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name=_(u"Users"), blank=True)

    created = models.DateTimeField(_('Created Date'), auto_now_add=True, 
        blank=True, null=True)
    modified = models.DateTimeField(_('Modified Date'), auto_now=True, 
        blank=True, null=True)

    tags = models.ManyToManyField('media.MediaTag', blank=True, related_name='%(app_label)s_%(class)s_tags')

    class Meta:
        abstract = True

    @property
    def page_title(self):
        return self.title

    def save(self, *args, **kwargs):

        if not self.title:
            self.title = 'Untitled'

        

        super(BaseMedia, self).save(*args, **kwargs)

class BaseImage( BaseMedia ):

    image = models.ImageField(upload_to=image_title_file_name, help_text="To ensure a precise color replication in image variants, make sure an sRGB color profile has been assigned to each image.")
    
    # -- Variations
    thumbnail_jpg = ImageSpecField( source='image', format='JPEG', 
        processors=[ResizeToFit(150, 150)], options={'quality': 90})
    thumbnail_png = ImageSpecField( source='image', format='PNG', 
        processors=[ResizeToFit(150, 150)], options={'quality': 90})

    credit = models.CharField(_("Credit"), max_length=255, blank=True)
    caption = models.TextField(_("Caption"), blank = True )
    alt = models.CharField(_("Alt Text"), max_length=255, blank=True)

    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)

    use_png = models.BooleanField( default = False, 
        verbose_name='Use .PNG instead of .JPG', help_text="PNG files are much larger but better in some cases, such as for vector images")

    variants = ('thumbnail',)
    
    def get_image_sources(self):
        sources = []
        main_url = self.image_url
        if main_url:
            sources.append(main_url)

        for variant in self.variants:
            variant_url = self.get_variant_url(variant)
            if variant_url:
                sources.append(variant_url)

        return sources

    @property
    def thumbnail(self):
        if self.use_png:
            return self.thumbnail_png
        else:
            return self.thumbnail_jpg

    @property
    def image_url(self):
        try:
            return self.image.url
        except:
            return None

    @property
    def image_size(self):
        try:
            return self.image.size
        except:
            return None

    @property
    def image_width(self):
        try:
            return self.image.width
        except:
            return None

    @property
    def image_height(self):
        try:
            return self.image.height
        except:
            return None


    @property
    def thumbnail_url(self):
        try:
            return self.thumbnail.url
        except:
            return None

    @property
    def thumbnail_width(self):
        try:
            return self.thumbnail.width
        except:
            return None

    @property
    def thumbnail_height(self):
        try:
            return self.thumbnail.height
        except:
            return None

    def get_variant_url(self, variant_name):
        try:
            field = getattr(self, variant_name)
            return field.url
        except:
            return None 

    def get_variant_width(self, variant_name):
        try:
            field = getattr(self, variant_name)
            return field.width
        except:
            return None  


    def get_variant_height(self, variant_name):
        try:
            field = getattr(self, variant_name)
            return field.height
        except:
            return None  
    

    def get_variant_link(self, variant_name, include_dimensions=False):
        #dimensions is expensive operation
        try:
            field = getattr(self, variant_name)
            gussied_name = variant_name.replace("_", " ").title()
            
            if include_dimensions:
                return '<a href="%s" data-img="%s" data-alt="%s" data-credit="%s" data-caption="%s">%s (%spx x %spx)</a><br />'\
                    %(field.url, field.url, self.get_alt(), self.credit, self.caption, gussied_name, field.width, field.height)
            else:
                return '<a href="%s" data-img="%s" data-alt="%s" data-credit="%s" data-caption="%s">%s</a><br />'\
                    %(field.url, field.url, self.get_alt(), self.credit, self.caption, gussied_name)
        except:
            return ''

    def get_alt(self):
        if self.alt:
            return self.alt
        return self.title

    @staticmethod
    def autocomplete_search_fields():
        return ("id__iexact", "title__icontains", "credit__icontains", "alt__icontains", "caption__icontains",'admin_description__icontains', 'legacy_url__icontains')


    def __unicode__(self):
        if self.title:
            return ("%s")%(self.title)
        elif self.caption:
            return ("%s %s")%(self.caption, self.credit)
        elif self.legacy_url:
            return ("Image previously %s")%(self.legacy_url)
        else:
            return ("Image %s")%(self.pk)


    class Meta:
        abstract = True

    def save(self, *args, **kwargs):

        #Use filename for title if not specified.
        if self.image and not self.title:
            
            self.title = gussy_path(self.image.url)

        if self.image:
            self.width = self.image_width
            self.height = self.image_height
            self.size = self.image_size
            self.display_size = displaybytes(self.image_size)
        else:
            self.width = None
            self.height = None
            self.size = None
            self.display_size = None
            

        super(BaseImage, self).save(*args, **kwargs)
        
        

class BaseDocument( BaseMedia ):

    image = models.ForeignKey('Image', null=True, blank=True, related_name="%(app_label)s_%(class)s_related", on_delete=models.SET_NULL) 
    media_file = models.FileField(upload_to=document_file_name, blank=True, help_text="Documents, i.e. PDFs or Word docs")
    

    @staticmethod
    def autocomplete_search_fields():
        return ("id__iexact", "title__icontains", 'admin_description__icontains', 'legacy_url__icontains')

    def get_document_link(self):
        try:
            return '<a href="%s">%s</a><br />'%(self.media_url, self.title)
        except:
            return None

    @property
    def media_url(self):
        try:
            return self.media_file.url
        except:
            return None

    @property
    def image_url(self):
        try:
            return self.image.image_url
        except:
            return None

    @property
    def image_thumbnail_url(self):
        try:
            return self.image.thumbnail_url
        except:
            return None

    @property
    def file_size(self):
        try:
            return self.media_file.size
        except:
            return None

    def get_absolute_url(self):
      return self.media_url

    def get_redirect_link(self):

        try:
            return reverse('document_redirect_view', kwargs={'pk':self.pk})
        except:
           return None

    def __unicode__(self):
        if self.title:
            return ("%s")%(self.title)
        elif self.legacy_url:
            return ("Document previously %s")%(self.legacy_url)
        else:
            return ("Document %s")%(self.pk)


    def save(self, *args, **kwargs):

        #Use filename for title if not specified.
        if self.media_file and not self.title:
            self.title = gussy_path(self.media_file.url)

        if self.media_file:
            self.size = self.file_size
            self.display_size = displaybytes(self.file_size)
        else:
            self.size = None
            self.display_size = None

        super(BaseDocument, self).save(*args, **kwargs)

    class Meta:
        abstract = True





class BaseSecureDocument( BaseMedia ):

    def get_storage():
        storage = import_by_path(settings.SECURE_DOCUMENT_STORAGE)()
        return storage


    image = models.ForeignKey(settings.IMAGE_MODEL, null=True, blank=True, related_name="%(app_label)s_%(class)s_related", on_delete=models.SET_NULL) 
    try:
        media_file = models.FileField(upload_to=document_file_name, blank=True, help_text="Documents, i.e. PDFs or Word docs",storage=get_storage())
    except:
        media_file = models.FileField(upload_to=document_file_name, blank=True, help_text="Documents, i.e. PDFs or Word docs")
    

    slug = models.CharField(_("slug"), max_length=50, blank=True, null=True, unique=True)
    

    @staticmethod
    def autocomplete_search_fields():
        return ("id__iexact", "title__icontains", 'admin_description__icontains', 'legacy_url__icontains')

    def get_document_link(self):
        try:
            return '<a href="%s">%s</a><br />'%(self.media_url, self.title)
        except:
            return None

    def get_share_url(self):
        if self.slug:
            try:
                return reverse('secure_document_view', kwargs={'slug':self.slug})
            except:
               return None
        return None

    def generate_authorized_link(self, duration_seconds):

        s3 = S3Connection(settings.AWS_ACCESS_KEY_ID,
                            settings.AWS_SECRET_ACCESS_KEY,
                            is_secure=True)
        # Create a URL valid for 60 seconds.
        filepath = self.media_file.name
        return s3.generate_url(duration_seconds, 'GET',
                            bucket=settings.AWS_STORAGE_SECURE_BUCKET_NAME,
                            key=filepath,
                            force_http=True)

    def get_secure_url(self):
        return self.generate_authorized_link(settings.SECURE_DOCUMENT_LINK_LIFE)
        

    @property
    def media_url(self):
        try:
            return self.media_file.url
        except:
            return None

    @property
    def image_url(self):
        try:
            return self.image.image_url
        except:
            return None

    @property
    def image_thumbnail_url(self):
        try:
            return self.image.thumbnail_url
        except:
            return None

    @property
    def file_size(self):
        try:
            return self.media_file.size
        except:
            return None

    def get_absolute_url(self):
      return self.media_url

    def __unicode__(self):
        if self.title:
            return ("%s")%(self.title)
        elif self.legacy_url:
            return ("Document previously %s")%(self.legacy_url)
        else:
            return ("Document %s")%(self.pk)


    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = generate_object_slug(self)

        if self.media_file:
            self.size = self.file_size
            self.display_size = displaybytes(self.file_size)
        else:
            self.size = None
            self.display_size = None


        #Use filename for title if not specified.
        if self.media_file and not self.title:
            self.title = gussy_path(self.media_file.url)

        super(BaseSecureDocument, self).save(*args, **kwargs)

        #Make the media file private
        if self.media_file:
            conn = boto.s3.connection.S3Connection(
                settings.AWS_ACCESS_KEY_ID,
                settings.AWS_SECRET_ACCESS_KEY)
            bucket = conn.create_bucket(settings.AWS_STORAGE_SECURE_BUCKET_NAME)
            k = boto.s3.key.Key(bucket)

            k.key = self.media_file.name
            k.set_acl('private')

    class Meta:
        abstract = True


class BaseAccess( models.Model ):
    title = models.CharField(_("title"), max_length=255, help_text="For what / to whom are you granting access?")
    description = models.TextField(_("Description"), blank = True, null=True)

    expiration_date = models.DateTimeField(_('Expiration Date'), blank=True, null=True)
    password = models.CharField(_('password'), max_length=128, blank=True, null=True)

    slug = models.CharField(_("slug"), max_length=50, blank=True, null=True, unique=True)


    admin_description = models.TextField(_("Administrative Description"), blank = True, 
        help_text='Add administrative description to help others find and use this image.' )
   
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_(u"Creator"), blank=True, null=True, related_name="%(app_label)s_%(class)s_related")
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name=_(u"Users"), blank=True)

    created = models.DateTimeField(_('Created Date'), auto_now_add=True, 
        blank=True, null=True)
    modified = models.DateTimeField(_('Modified Date'), auto_now=True, 
        blank=True, null=True)

    def __unicode__(self):
        return ("%s")%(self.title)


    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        def setter(raw_password):
            self.set_password(raw_password)
            self.save(update_fields=["password"])
        return check_password(raw_password, self.password, setter)

    def set_unusable_password(self):
        # Sets a value that will never be a valid hash
        self.password = make_password(None)

    def has_usable_password(self):
        return is_password_usable(self.password)

    @property
    def password_key(self):
        return '%s_password_%s'%(self.__class__.__name__.lower(), self.slug)

    def is_authorized(self, request):        
        stored_password = request.session.get(self.password_key, None)
        return (not self.password or (stored_password and self.check_password(stored_password)))

    def get_share_url(self):
        #Override in implementation
        return None

    def get_secure_url(self):
        #Override in implementation
        return None

    def get_items(self):
        try:
            model = get_model(settings.SECURE_DOCUMENT_SET_ITEM_MODEL.split('.')[0], settings.SECURE_DOCUMENT_SET_ITEM_MODEL.split('.')[1])
            return model.objects.filter(parent=self).order_by('order')
        except:
            return []

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = generate_object_slug(self)

        super(BaseAccess, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.title

    class Meta:
        abstract = True


class BaseSecureDocumentAccess( BaseAccess ):

    try:
        document = models.ForeignKey(settings.SECURE_DOCUMENT_MODEL, null=True, on_delete=models.SET_NULL)
    except:
        pass

    def get_share_url(self):
        if self.slug:
            try:
                return reverse('secure_document_item_view', kwargs={'slug':self.document.slug, 'access_slug':self.slug})
            except:
               return None
        return None

    def get_secure_url(self):
        if self.document:
            return self.document.generate_authorized_link(settings.SECURE_DOCUMENT_LINK_LIFE)

        return None

    class Meta:
        abstract = True
        verbose_name = "Document Share Settings"
        verbose_name_plural = "Document Share Settings"

class BaseSecureDocumentSet( BaseAccess ):
    

    def get_items(self):
        try:
            model = get_model(settings.SECURE_DOCUMENT_SET_ITEM_MODEL.split('.')[0], settings.SECURE_DOCUMENT_SET_ITEM_MODEL.split('.')[1])
            return model.objects.filter(parent=self).order_by('order')
        except:
            return []

    def get_share_url(self):
        if self.slug:
            try:
                return reverse('secure_document_set_view', kwargs={'slug':self.slug})
            except:
               return None
        return None

    def get_secure_url(self):
        return self.get_share_url()

    class Meta:
        abstract = True
  

class BaseSecureDocumentSetItem( models.Model ):

    try:
        parent = models.ForeignKey(settings.SECURE_DOCUMENT_SET_MODEL, null=True, on_delete=models.SET_NULL)
        document = models.ForeignKey(settings.SECURE_DOCUMENT_MODEL, null=True, on_delete=models.SET_NULL)
    except:
        pass
    order = models.PositiveIntegerField(default=1)
    description = models.TextField(_("Description"), blank = True, null=True)

    def get_secure_url(self):    
        return self.document.get_secure_url()
        

    class Meta:
        abstract = True
        ordering = ['order',]



# register the signal
try:
    #pre 1.7
    image_model = get_model(settings.IMAGE_MODEL.split('.')[0], settings.IMAGE_MODEL.split('.')[1])
    document_model = get_model(settings.DOCUMENT_MODEL.split('.')[0], settings.DOCUMENT_MODEL.split('.')[1])

except:
    image_model = settings.IMAGE_MODEL
    document_model = settings.DOCUMENT_MODEL


@receiver(pre_delete, sender=image_model, dispatch_uid='image_delete_signal')
def remove_image_file_from_s3(sender, instance, using, **kwargs):
    try:
        delete_file_on_delete = settings.IMAGE_MODEL_DELETE_FILE_ON_DELETE
    except:
        delete_file_on_delete = False

    if delete_file_on_delete:

        #Figure out what bucket to delete
        delete_bucket = None
        if hasattr(instance, 'variants') and instance.variants:
            for variant in instance.variants:
                field = getattr(instance, variant)
                delete_bucket = "/".join(str(field).split('/')[:-1])

            try:
                if delete_bucket:
                    conn = boto.s3.connection.S3Connection(
                        settings.AWS_ACCESS_KEY_ID,
                        settings.AWS_SECRET_ACCESS_KEY)

                    bucket = Bucket(conn, settings.AWS_MEDIA_BUCKET_NAME)

                    for key in bucket.list(prefix=delete_bucket):
                        # print 'delete: %s'%(key)
                        key.delete()               

            except:
                pass

        try:
            instance.image.delete(save=False)  
        except:
            pass

@receiver(pre_delete, sender=document_model, dispatch_uid='document_delete_signal')
def remove_document_file_from_s3(sender, instance, using, **kwargs):
    try:
        delete_file_on_delete = settings.DOCUMENT_MODEL_DELETE_FILE_ON_DELETE
    except:
        delete_file_on_delete = False

    if delete_file_on_delete:
        try:
            instance.media_file.delete(save=False)  
        except:
            pass            


