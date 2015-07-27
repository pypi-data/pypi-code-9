import re
import traceback

import django.http
import django.template
import django.template.loader
import django.utils.translation

from django.conf import settings
from django.contrib import messages
from django.core.cache import cache

from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404, HttpResponseServerError, HttpResponsePermanentRedirect
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from grappelli.views.related import AutocompleteLookup

from .models import LegacyURL, LegacyURLReferer
from .forms import *
from .management.commands.find_old_links import import_links



def get_legacy_url(request):    

    path = request.path
    if path.startswith("/"):
        path = path[1:]

    return parse_legacy_url(request, path)
    
def parse_legacy_url(request, path):

    is_valid = is_valid_path(request)


    if is_valid == False or path is None or path == '' or path == '/':
        raise Http404(_("No path for legacy url"))

    if settings.DEBUG:
        print "Get legacy url for %s"%(path)

    try:
        legacy_url = LegacyURL.objects.get(url=path)
        
        if legacy_url._redirect_path:
            if settings.DEBUG:
                print "Legacy URL: redirect found %s = %s"%(path, legacy_url._redirect_path)
            return HttpResponsePermanentRedirect(legacy_url._redirect_path)

        else:

            if settings.DEBUG:
                print "Legacy URL: redirect exists but isn't redirected. %s"%(legacy_url)           

            #legacy url exists, but hasn't been hooked up yet.  
            raise Http404(_("Legacy URL redirect not specified."))                  

    except LegacyURL.DoesNotExist:

        if settings.LEGACY_URL_AUTO_CREATE_ON_404:

            redirect = create_redirect(path, request)

            if settings.DEBUG:
                print "Redirect for %s = %s"%(path, redirect)

            if redirect:
                return HttpResponsePermanentRedirect(redirect)
            else:   
                raise Http404(_("Legacy URL not found."))
        else:

            raise Http404(_("Legacy URL not found."))

def create_redirect(link, request):
    referer_url = request.META.get('HTTP_REFERER', None) if request else None

    if (referer_url and settings.LEGACY_URL_REQUIRE_REFERER_ON_CREATE) or not settings.LEGACY_URL_REQUIRE_REFERER_ON_CREATE:
        ignore_list = settings.LEGACY_URL_IGNORE_LIST
        for ignore in ignore_list:
            if ignore in link.lower():
                if settings.DEBUG:
                    print "Ignore  %s because it matches %s from the ignore list"%(link, ignore)
                return None

        if len(link) > 2048:
            #Probably not a real link if greater than 2000
            return None

        
        legacy_link, link_created = LegacyURL.objects.get_or_create(url=link)
        if settings.DEBUG:
            if link_created:
                print "Create legacy url for link %s"%(link)
            else:
                print "Legacy url %s exists"%(link)

        #Record refererer       
        if referer_url:
            referer, referer_created = LegacyURLReferer.objects.get_or_create(legacy_url=legacy_link,referer_url=referer_url,referer_title=referer_url)

        if link_created:
            #print "CREATED NEW LINK BASED ON LEGACY"
            legacy_link.title = link
            legacy_link.save()                          
        
        if legacy_link._redirect_path:
            return legacy_link._redirect_path

    
    return None
            
def test_reset(request):
    #RESET app for Selenium tests
    
    try:
        from django.contrib.auth import get_user_model
    except ImportError: # django < 1.5
        from django.contrib.auth.models import User
    else:
        User = get_user_model()

    try:
        test_user = User.objects.get(email=settings.TEST_USER)
        test_user.delete()
        messages.success(request, 'Test user deleted')
    except:
        pass

    return redirect('/')



#==============================================================================
# ADMIN VIEWS
#==============================================================================

def clear_cache(request):
    
    if not request.user or not request.user.is_staff:
        raise Http404()

    try:
        cache.clear()
        messages.success(request, 'The cache has been cleared.')
    except:
        messages.warning(request, 'There was an error while attempting to clear the cache: %s'%(traceback.format_exc()))

    return redirect('admin:index')




def admin_import_links( request ):    
    

    if not request.user or not request.user.is_staff:
        raise Http404()

    # Handle file upload
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        import_file = request.FILES.get('file', None)

        if import_file:
            results = import_links(import_file, request)

            messages.success(request, results)

        else:
            messages.warning(request, 'No .CSV file specified')
        

    else:
        form = UploadFileForm()
        pass

    

    # Render list page with the documents and the form
    return render_to_response(
        'admin/linksimport.html',
        {'form': form},
        context_instance=RequestContext(request)
    )

def is_valid_path(request):
    url = request.build_absolute_uri()
    val = URLValidator()
    try:
        val(url)
    except ValidationError, e:
        return False

    #TODO -- a better / more efficent character validator
    safechars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~:/?#[]@!$&'()*+,;=%"
    for char in list(request.path):
        if char not in safechars:
            return False

    return True

class FilteredAutocomplete(AutocompleteLookup):
    """ patch grappelli's autocomplete to let us control the queryset 
    by creating a autocomplete_queryset function on the model """
    def get_queryset(self):
        if hasattr(self.model, "autocomplete_queryset"):
            qs = self.model.autocomplete_queryset()
        else:
            qs = self.model._default_manager.all()
        qs = self.get_filtered_queryset(qs)
        qs = self.get_searched_queryset(qs)
        return qs.distinct()

def fallback_403(request):
  """
  Fallback 403 handler which prints out a hard-coded string patterned
  after the Apache default 403 page.

  Templates: None
  Context: None
  """
  return django.http.HttpResponseForbidden(
      django.utils.translation.gettext(
          """<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>403 Forbidden</title>
</head><body>
<h1>Forbidden</h1>
<p>You don't have permission to access %(path)s on this server.</p>
<hr>
</body></html>""") % {'path': request.path})

def access_denied(request, template_name='403.html'):
  """
  Default 403 handler, which looks for the  which prints out a hard-coded string patterned
  after the Apache default 403 page.

  Templates: `403.html`
  Context:
      request
          The django request object
  """
  t = django.template.loader.get_template(template_name)
  template_values = {}
  template_values['request'] = request
  return django.http.HttpResponseForbidden(
      t.render(django.template.RequestContext(request, template_values)))

