# coding=utf-8

import urlparse
import httplib2
import urllib2 


from django import http
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.core.exceptions import PermissionDenied
from django.core.files.base import ContentFile
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import Q
from django.db.models import get_model
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseForbidden, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic.edit import UpdateView, CreateView, FormView
from django.views.generic import ListView, DetailView, RedirectView, DeleteView
from django.views.generic.base import TemplateView


from haystack.query import SearchQuerySet, SQ
from site_admin.utils.search_index import use_search_index

from boto.s3.connection import S3Connection

from .models import *
from .forms import *

class BaseAdminImageMediaPickerView(ListView):
    
    template_name = "media/admin_image_picker.html"
    paginate_by = 48
    
    def get_queryset(self):
        
        if self.request.user and self.request.user.is_authenticated() and self.request.user.is_staff:
            # if use_search_index:

            #     if 'q' in self.request.GET and self.request.GET['q']!= '':               

            #         queryset = SearchQuerySet().models(self.model).auto_query(self.request.GET['q'])
            #     else:
            #         queryset = SearchQuerySet().models(self.model)
                    
            # else:


            if 'q' in self.request.GET and self.request.GET['q']!= '':
                query = self.request.GET['q']
                queryset = self.model.objects.filter(
                    Q(title__icontains=query) |
                    Q(caption__icontains=query) | 
                    Q(credit__icontains=query) | 
                    Q(admin_description__icontains=query) ).order_by('-id')    
            else:
                queryset = self.model.objects.all().order_by('-id')

            return queryset

        else:

            raise PermissionDenied

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(BaseAdminImageMediaPickerView, self).dispatch(*args, **kwargs)



class BasePublicImagePickerView(ListView):
    
    template_name = "media/public_image_picker.html"
    paginate_by = 24
    
    def get_queryset(self):
        
        if self.request.user and self.request.user.is_authenticated():

            if use_search_index:
                queryset = SearchQuerySet().models(self.model).filter(users_ids__in=[self.request.user.id]).order_by('title')
            else:
                queryset = self.model.objects.filter(users__in=[self.request.user]).order_by('-id')
            
                
            return queryset

        else:
            raise PermissionDenied

class BaseImageListView(ListView):
    
    template_name = "media/image_list.html"
    paginate_by = 24
    
    def get_queryset(self):
        
        if self.request.user and self.request.user.is_authenticated():

            if use_search_index:
                queryset = SearchQuerySet().models(self.model).filter(users_ids__in=[self.request.user.id]).order_by('title')
            else:
                queryset = self.model.objects.filter(users__in=[self.request.user]).order_by('-id')

            return queryset
            
        else:
            raise PermissionDenied  


class BaseImageAddView(CreateView):
    
    #form_class = ImageAddForm
    template_name = 'media/image_add.html'

    def get_success_url(self):
        next = self.request.POST.get('next', None)
        if next:
            return next
        else:
            return reverse('image_list_view')

    def form_valid(self, form):
        messages.success(self.request, 'Your image has been uploaded.')
        return super(BaseImageAddView, self).form_valid(form)

class BaseImageEditView(UpdateView):
    
    #form_class = ImageAddForm
    template_name = 'media/image_add.html'

    def get(self, request, *args, **kwargs):
        obj = self.get_object()

        if request.user and request.user.is_authenticated():
            #related_user = obj.users.filter(pk=request.user.pk)
            
            if obj.creator == request.user:
                return super(BaseImageEditView, self).get(request, **kwargs)
            else:
                raise PermissionDenied
        else:
            raise PermissionDenied

    def get_success_url(self):
        return reverse('image_list_view')

    def form_valid(self, form):
        messages.success(self.request, 'Your image has been updated.')
        return super(BaseImageEditView, self).form_valid(form)        
            
class BaseImageDeleteView(DeleteView):
    #model = get_model(settings.IMAGE_MODEL.split('.')[0], settings.IMAGE_MODEL.split('.')[1])
    success_url = reverse_lazy('image_list_view')
    template_name = 'media/image_delete.html'



    def get(self, request, *args, **kwargs):
        obj = self.get_object()

        if request.user and request.user.is_authenticated():
            if obj.creator == request.user:
                return super(BaseImageDeleteView, self).get(request, **kwargs)
            else:
                raise PermissionDenied
        else:
            raise PermissionDenied

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user and request.user.is_authenticated():
            if obj.creator == request.user:
                return super(BaseImageDeleteView, self).post(request, **kwargs)
            else:
                raise PermissionDenied
        else:
            raise PermissionDenied

class BaseAdminDocumentMediaPickerView(ListView):
    
    template_name = "media/admin_document_picker.html"
    paginate_by = 48
    
    def get_queryset(self):
        
        if self.request.user and self.request.user.is_authenticated() and self.request.user.is_staff:
            if use_search_index:

                if 'q' in self.request.GET and self.request.GET['q']!= '':               

                    queryset = SearchQuerySet().models(self.model).auto_query(self.request.GET['q'])
                else:
                    queryset = SearchQuerySet().models(self.model)
                    
            else:


                if 'q' in self.request.GET and self.request.GET['q']!= '':
                    query = self.request.GET['q']
                    queryset = self.model.objects.filter(
                        Q(title__icontains=query) | 
                        Q(admin_description__icontains=query) ).order_by('-id')    
                else:
                    queryset = self.model.objects.all().order_by('-id')

            return queryset

        else:

            raise PermissionDenied

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(BaseAdminDocumentMediaPickerView, self).dispatch(*args, **kwargs)


class BasePublicDocumentPickerView(ListView):
    
    template_name = "media/public_document_picker.html"
    paginate_by = 48
    
    def get_queryset(self):
        
        if self.request.user and self.request.user.is_authenticated():

            queryset = self.model.objects.filter(users__in=[self.request.user]).order_by('-id')

            if use_search_index:
                queryset = SearchQuerySet().models(self.model).filter(users__in=[self.request.user.id])
            else:
                queryset = self.model.objects.filter(users__in=[self.request.user]).order_by('-id')
            
                
            return queryset
            
        else:
            raise PermissionDenied  

class BaseDocumentListView(CreateView):

    template_name = "media/document_list.html"
    paginate_by = 24
    
    def get_queryset(self):
        
        if self.request.user and self.request.user.is_authenticated():

            if use_search_index:
                queryset = SearchQuerySet().models(self.model).filter(users_ids__in=[self.request.user.id]).order_by('title')
            else:
                queryset = self.model.objects.filter(users__in=[self.request.user]).order_by('-id')

            return queryset
            
        else:
            raise PermissionDenied  


class BaseDocumentAddView(CreateView):

    #form_class = ImageAddForm
    template_name = 'media/document_add.html'

    def get_success_url(self):
        next = self.request.POST.get('next', None)
        if next:
            return next
        else:
            return reverse('document_list_view')

    def form_valid(self, form):
        messages.success(self.request, 'Your image has been uploaded.')
        return super(BaseImageAddView, self).form_valid(form)

class BaseDocumentEditView(UpdateView):
    
    #form_class = ImageAddForm
    template_name = 'media/document_add.html'

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        
        if request.user and request.user.is_authenticated():
            if obj.creator == request.user:
                return super(BaseImageEditView, self).get(request, **kwargs)
            else:
                raise PermissionDenied
        else:
            raise PermissionDenied

    def get_success_url(self):
        return reverse('document_list_view')

    def form_valid(self, form):
        messages.success(self.request, 'Your image has been updated.')
        return super(BaseImageEditView, self).form_valid(form)  


class BaseDocumentDeleteView(DeleteView):
    #model = get_model(settings.IMAGE_MODEL.split('.')[0], settings.IMAGE_MODEL.split('.')[1])
    success_url = reverse_lazy('document_list_view')
    template_name = 'media/document_delete.html'



    def get(self, request, *args, **kwargs):
        obj = self.get_object()

        if request.user and request.user.is_authenticated():
            if obj.creator == request.user:
                return super(BaseDocumentDeleteView, self).get(request, **kwargs)
            else:
                raise PermissionDenied
        else:
            raise PermissionDenied

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user and request.user.is_authenticated():
            if obj.creator == request.user:
                return super(BaseDocumentDeleteView, self).post(request, **kwargs)
            else:
                raise PermissionDenied
        else:
            raise PermissionDenied        
    
class BaseImageVariantRedirectView(DetailView):

    def get(self, request, *args, **kwargs):
        obj = self.get_object()

        variant = self.kwargs.get('variant_name', None)
        if variant:
            print "Return variant for %s"%(variant)

            url = obj.get_variant_url(variant)
            if url:
                return HttpResponseRedirect(url)
            else:
                raise Http404(_("Image variant %s not available"%(variant)))
        else:
            raise Http404(_("Image variant not specified"))

class BaseDocumentRedirectView(DetailView):

    def get(self, request, *args, **kwargs):
        obj = self.get_object()

        media_url = obj.media_url
        if media_url:
            return HttpResponseRedirect(media_url)
        else:
            raise Http404(_("Document not available"))


class BaseSecureDocumentView(RedirectView):
    permanent = False

    def get_redirect_url(self, secure_document):
        return secure_document.generate_authorized_link(settings.SECURE_DOCUMENT_LINK_LIFE)

    def get(self, request, *args, **kwargs):
        m = get_object_or_404(self.model, slug=kwargs['slug'])
        u = request.user

        is_authorized_user = request.user.is_authenticated() and request.user.is_staff
        if is_authorized_user:
            if m.media_file:
                
                url = self.get_redirect_url(m)
                # The below is taken straight from RedirectView.
                if url:
                    if self.permanent:
                        return http.HttpResponsePermanentRedirect(url)
                    else:
                        return http.HttpResponseRedirect(url)
                else:
                    logger.warning('Gone: %s', self.request.path,
                                extra={
                                    'status_code': 410,
                                    'request': self.request
                                })
                    return http.HttpResponseGone()
            else:
                raise http.Http404
        else:
            raise http.Http404          

class BaseSecureDocumentItemView(DetailView):
    template_name = 'media/secure_document_item.html'
    #access_model = SecureDocumentAccess

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()        
        self.access = get_object_or_404(self.access_model, slug=kwargs['access_slug'])

        meets_password_requirements = self.access.is_authorized(request)      
        date_is_valid = not self.access.expiration_date or (self.access.expiration_date and self.access.expiration_date >= timezone.now())

        if meets_password_requirements and date_is_valid:
            return super(BaseSecureDocumentItemView, self).get(request, *args, **kwargs)
        else:

            if not meets_password_requirements:
                messages.warning(self.request, 'Please enter the password to access this document.')
                redirect_url = reverse('secure_document_item_access_view', kwargs={'slug':self.object.slug, 'access_slug':self.access.slug})

            elif not date_is_valid:
                messages.warning(self.request, 'This document is expired.')
                redirect_url = reverse('secure_document_item_expired_view', kwargs={'slug':self.object.slug, 'access_slug':self.access.slug})
            
            return HttpResponseRedirect(redirect_url)

    def get_context_data(self, **kwargs):
        context = super(BaseSecureDocumentItemView, self).get_context_data(**kwargs)
        context['access'] = self.access
        return context


class BaseSecureDocumentItemAccessView(FormView):
    template_name = 'media/secure_document_item_access.html'
    form_class = SecureDocumentItemAccessForm
    submitted_password = None
    submitted_password_correct = False
    object = None
    #success_url = '/thanks/'

    def get(self, request, *args, **kwargs):
        self.object = get_object_or_404(self.model, slug=self.kwargs['slug'])
        self.access = get_object_or_404(self.access_model, slug=self.kwargs['access_slug'])

        meets_password_requirements = self.access.is_authorized(request) 

        if meets_password_requirements:
            redirect_url = reverse('secure_document_item_view', kwargs={'slug':self.object.slug, 'access_slug':self.access.slug})
            return HttpResponseRedirect(redirect_url)

        return super(BaseSecureDocumentItemAccessView, self).get(request, *args, **kwargs) 

    def form_valid(self, form):
        self.object = get_object_or_404(self.model, slug=self.kwargs['slug'])
        self.access = get_object_or_404(self.access_model, slug=self.kwargs['access_slug'])

        self.submitted_password = form.cleaned_data['password']
        self.submitted_password_correct = self.access.check_password(self.submitted_password)

        print 'submitted_password? %s'%(self.submitted_password)
        print 'submitted_password_correct? %s'%(self.submitted_password_correct)
        
        redirect = self.get_success_url()
        response = HttpResponseRedirect(redirect)

        print 'redirect? %s'%(redirect)

        if self.submitted_password_correct:
            self.request.session[self.access.password_key] = self.submitted_password
            print 'password_key? %s'%(self.access.password_key)
        else:
            messages.error(self.request, 'The password you entered was incorrect.')
        return response

    def get_success_url(self):
        if self.submitted_password_correct:
            url = reverse('secure_document_item_view', kwargs={'slug':self.object.slug, 'access_slug':self.access.slug})
        else:
            url = reverse('secure_document_item_access_view', kwargs={'slug':self.object.slug, 'access_slug':self.access.slug})
        return url

    def get_context_data(self, **kwargs):
        context = super(BaseSecureDocumentItemAccessView, self).get_context_data(**kwargs)
        context['access'] = self.access
        return context


class BaseSecureDocumentItemExpiredView(DetailView):
    template_name = 'media/secure_document_item_expired.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()     
        self.access = get_object_or_404(self.access_model, slug=kwargs['access_slug'])   

        date_is_valid = not self.access.expiration_date or (self.access.expiration_date and self.access.expiration_date >= timezone.now())

        if date_is_valid:
            redirect_url = reverse('secure_document_item_view', kwargs={'slug':self.object.slug, 'access_slug':self.access.slug})
            return HttpResponseRedirect(redirect_url)

        return super(BaseSecureDocumentItemExpiredView, self).get(request, *args, **kwargs) 

    def get_context_data(self, **kwargs):
        context = super(BaseSecureDocumentItemExpiredView, self).get_context_data(**kwargs)
        context['access'] = self.access
        return context


class BaseSecureDocumentSetAccessView(FormView):
    template_name = 'media/secure_document_set_access.html'
    form_class = SecureDocumentSetAccessForm
    submitted_password = None
    submitted_password_correct = False
    object = None
    #success_url = '/thanks/'

    def get(self, request, *args, **kwargs):
        self.object = get_object_or_404(self.model, slug=self.kwargs['slug'])

        meets_password_requirements = self.object.is_authorized(request) 

        if meets_password_requirements:
            redirect_url = reverse('secure_document_set_view', kwargs={'slug':self.object.slug})
            return HttpResponseRedirect(redirect_url)

        return super(BaseSecureDocumentSetAccessView, self).get(request, *args, **kwargs) 

    def form_valid(self, form):
        self.object = get_object_or_404(self.model, slug=self.kwargs['slug'])

        self.submitted_password = form.cleaned_data['password']
        self.submitted_password_correct = self.object.check_password(self.submitted_password)
        
        redirect = self.get_success_url()
        response = HttpResponseRedirect(redirect)

        if self.submitted_password_correct:
            self.request.session[self.object.password_key] = self.submitted_password
        else:
            messages.error(self.request, 'The password you entered was incorrect.')
        return response

    def get_success_url(self):
        if self.submitted_password_correct:
            url = reverse('secure_document_set_view', kwargs={'slug':self.object.slug})
        else:
            url = reverse('secure_document_access_view', kwargs={'slug':self.object.slug})
        return url




class BaseSecureDocumentSetView(DetailView):
    template_name = 'media/secure_document_set.html'
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()        

        meets_password_requirements = self.object.is_authorized(request)      
        date_is_valid = not self.object.expiration_date or (self.object.expiration_date and self.object.expiration_date >= timezone.now())

        if meets_password_requirements and date_is_valid:
            return super(BaseSecureDocumentSetView, self).get(request, *args, **kwargs)
        else:

            if not meets_password_requirements:
                messages.warning(self.request, 'Please enter the password to access this document set.')
                redirect_url = reverse('secure_document_set_access_view', kwargs={'slug':self.object.slug})

            elif not date_is_valid:
                messages.warning(self.request, 'This document is expired.')
                redirect_url = reverse('secure_document_set_expired_view', kwargs={'slug':self.object.slug})

            
            return HttpResponseRedirect(redirect_url)

class BaseSecureDocumentSetExpiredView(DetailView):
    template_name = 'media/secure_document_set_expired.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()        

        date_is_valid = not self.object.expiration_date or (self.object.expiration_date and self.object.expiration_date >= timezone.now())

        if date_is_valid:
            redirect_url = reverse('secure_document_set_view', kwargs={'slug':self.object.slug})
            return HttpResponseRedirect(redirect_url)

        return super(BaseSecureDocumentSetExpiredView, self).get(request, *args, **kwargs) 

class BaseSecureDocumentSetItemView(RedirectView):
    permanent = False


    def get_redirect_url(self, secure_document):
        return secure_document.generate_authorized_link(settings.SECURE_DOCUMENT_LINK_LIFE)

    def get(self, request, *args, **kwargs):
        document = get_object_or_404(self.model, slug=kwargs['slug'])
        set = get_object_or_404(self.set_model, slug=kwargs['set_slug'])
        
        is_authorized_user = set.is_authorized(request)
        if is_authorized_user:
            if document.media_file:
                
                url = self.get_redirect_url(document)
                # The below is taken straight from RedirectView.
                if url:
                    if self.permanent:
                        return http.HttpResponsePermanentRedirect(url)
                    else:
                        return http.HttpResponseRedirect(url)
                else:
                    logger.warning('Gone: %s', self.request.path,
                                extra={
                                    'status_code': 410,
                                    'request': self.request
                                })
                    return http.HttpResponseGone()
            else:
                raise http.Http404
        else:
            messages.warning(self.request, 'Please enter the password to access this document.')
            redirect_url = reverse('secure_document_access_view', kwargs={'slug':set.slug})
            return HttpResponseRedirect(redirect_url)    



class BaseImageBatchView(TemplateView):      
    template_name = 'media/batch/images.html'  

class BaseSecureImageBatchView(TemplateView):      
    template_name = 'media/batch/secureimages.html'  

class BaseDocumentBatchView(TemplateView):      
    template_name = 'media/batch/documents.html'  

class BaseSecureDocumentBatchView(TemplateView):      
    template_name = 'media/batch/securedocuments.html'  



def get_legacy_media_url(request):  
    
    image_model = get_model(settings.IMAGE_MODEL.split('.')[0], settings.IMAGE_MODEL.split('.')[1])
    document_model = get_model(settings.DOCUMENT_MODEL.split('.')[0], settings.DOCUMENT_MODEL.split('.')[1])
    
    path = request.path
    if path.startswith("/"):
        path = path[1:]

    if path is None or path == '' or path == '/':
        raise Http404(_("No path for legacy media"))


    if settings.DEBUG:
        print "Legacy Media: Attempt to find media legacy url for %s"%(path)

    try:
        legacy_images = image_model.objects.filter(legacy_url=path)[0]

        has_image = legacy_image.image and hasattr(legacy_image.image, 'url')
        if has_image:
            if settings.DEBUG:
                print "Legacy Media: Image redirect found %s = %s"%(path, legacy_image.image.url)
            return HttpResponsePermanentRedirect(legacy_image.image.url)

        else:

            raise Http404(_("Legacy image has no new image specified."))
        

    except:

        if settings.DEBUG:
            print "Legacy Media: Image %s NOT FOUND - Try documents"%(path)
        try:
            legacy_media = document_model.objects.filter(legacy_url=path)[0]
            has_file = legacy_media.media_file and hasattr(legacy_media.media_file, 'url')

            if settings.DEBUG:
                print "Legacy Media: Found media file: %s has_file? %s"%(legacy_media.pk, has_file)

            if has_file:
                #print "Legacy Media: Document redirect found %s = %s"%(path, legacy_media.media_file.url)
                return HttpResponsePermanentRedirect(legacy_media.media_file.url)

            else:

                raise Http404(_("Legacy Media has no new media specified."))    


        except:   
            if settings.DEBUG:
                print "Legacy Media: Document %s NOT FOUND"%(path)

            if settings.MEDIA_LEGACY_URL_AUTO_CREATE_ON_404:

                print 'create redirect!'
                redirect = create_redirect(path, request)

                if settings.DEBUG:
                    print "Legacy Media: Redirect for %s = %s"%(path, redirect)

                if redirect:
                    return HttpResponsePermanentRedirect(redirect)
                else:   
                    raise Http404(_("Legacy Media URL not found."))

            raise Http404(_("Legacy Media URL Not found."))



def create_redirect(link, request):

    referer_url = request.META.get('HTTP_REFERER', None) if request else None


    if referer_url:
        description = u"404 encountered %s Referer: %s"%(link, referer_url)
    else:
        description = u"404 encountered %s"%(link)


   
    
    archive_domain = settings.MEDIA_LEGACY_URL_ARCHIVE_DOMAIN
    parsed_archive = urlparse.urlparse( archive_domain ).netloc
    current_domain = Site.objects.get_current().domain

    #WHOA -- NOT GOING TO WORK....
    if parsed_archive == current_domain:    
        return None


    try:
        image_suffixes = settings.MEDIA_IMAGE_EXTENSIONS
    except:
        image_suffixes = ['.png', '.jpg', '.jpeg', '.gif']

    try:
        doc_suffixes = settings.MEDIA_DOCUMENT_EXTENSIONS
    except:
        doc_suffixes = [
            '.doc', '.pdf', '.ppt', '.zip', '.gzip', '.mp3', '.rar', '.exe', 
            '.avi', '.mpg', '.tif', '.wav', '.mov', '.psd', '.ai', '.wma',
            '.eps','.mp4','.bmp','.indd','.swf','.jar','.dmg','.iso','.flv',
            '.gz','.fla','.ogg','.sql'
        ]
        

    is_image = False
    for suffix in image_suffixes:
        if suffix in link.lower():
            is_image = True

    is_doc = False
    for suffix in doc_suffixes:
        if suffix in link.lower():
            is_doc = True
    
    ignore_list = settings.MEDIA_LEGACY_URL_IGNORE_LIST
    for ignore in ignore_list:
        if ignore in link.lower():
            if settings.DEBUG:
                print "Legacy Media: Ignore  %s because it matches %s from the ignore list"%(link, ignore)
            return None

    if is_image or is_doc:
        if settings.DEBUG:
            print "Legacy Media: Create media redirect for %s. Is it an image? %s Is it a Doc? %s "%(link, is_image, is_doc)
        pass

    try:
        store_empty = settings.MEDIA_LEGACY_STORE_EMPTY_MEDIA
    except:
        store_empty = True
    
    #print 'is_image? %s link %s'%(is_image, link)
    if is_image:
        download_url = u"%s%s"%(archive_domain, link)
        model_image = migrate_image(link, download_url, description)
        
        if model_image.image:
            return model_image.image_url
        else:
            if store_empty == False:
                model_image.delete()


    elif is_doc:

        download_url = u"%s%s"%(archive_domain, link)
        model_doc = migrate_document(link, download_url, description)        

        if model_doc.media_file:
            return model_doc.media_url

        else:
            if store_empty == False:
                model_doc.delete()

    return None

def migrate_image(path, download_url, description):

    image_model = get_model(settings.IMAGE_MODEL.split('.')[0], settings.IMAGE_MODEL.split('.')[1])

    model_image, created = image_model.objects.get_or_create(legacy_url = path)
    has_image = model_image.image and hasattr(model_image.image, 'url')
    name = urlparse.urlparse(path).path.split('/')[-1]  
    
    if created or not has_image:
        
        gussied_name = gussy_path(name)
        model_image.title = (u"Image %s"%(gussied_name))
        model_image.admin_description = description
        model_image.save()

    if not has_image: 
        if settings.DEBUG:
            print "Legacy Media: Downloading legacy image %s"%(download_url)          

        try:
            content = ContentFile(urllib2.urlopen(url_fix(download_url)).read())#, timeout=15)             
            model_image.image.save(name, content, save=True)
        except:
            content = None
            if settings.DEBUG:
                print "WARNING WARNING: Image not found: "+str(url_fix(download_url))
        
    return model_image

def migrate_document(path, download_url, description):

    document_model = get_model(settings.DOCUMENT_MODEL.split('.')[0], settings.DOCUMENT_MODEL.split('.')[1])

    model_doc, created = document_model.objects.get_or_create(legacy_url = path)
    has_file = model_doc.media_file and hasattr(model_doc.media_file, 'url')
    name = urlparse.urlparse(path).path.split('/')[-1]

    if created:
        gussied_name = gussy_path(name)
        model_doc.title = (u"Document %s"%(gussied_name))
        model_doc.admin_description = description
        model_doc.save()

    if not has_file:
        name = urlparse.urlparse(download_url).path.split('/')[-1]                      
        if settings.DEBUG:
            print "Legacy Media: Downloading legacy document %s"%(download_url)

        try:
            content = ContentFile(urllib2.urlopen(url_fix(download_url)).read())
            model_doc.media_file.save(name, content, save=True)
        except:
            content = None
            print "WARNING WARNING: Document not found: "+str(url_fix(download_url))

    return model_doc   

def gussy_path(file_name):
    file_name = file_name.replace("_", " ")
    file_name = file_name.replace("-", " ")
    file_name = file_name.replace(".", " ")
    file_name = file_name.replace("  ", " ")    
    return file_name.title()

def url_fix(s, charset='utf-8'):
    """Sometimes you get an URL by a user that just isn't a real
    URL because it contains unsafe characters like ' ' and so on.  This
    function can fix some of the problems in a similar way browsers
    handle data entered by the user:

    >>> url_fix(u'http://de.wikipedia.org/wiki/Elf (Begriffsklärung)')
    'http://de.wikipedia.org/wiki/Elf%20%28Begriffskl%C3%A4rung%29'

    :param charset: The target charset for the URL if the url was
                    given as unicode string.
    """
    if isinstance(s, unicode):
        s = s.encode(charset, 'ignore')
    s.replace("`", "")
    scheme, netloc, path, qs, anchor = urlparse.urlsplit(s)
    path = urllib.quote(path, '/%')
    qs = urllib.quote_plus(qs, ':&=')
    return urlparse.urlunsplit((scheme, netloc, path, qs, anchor))


