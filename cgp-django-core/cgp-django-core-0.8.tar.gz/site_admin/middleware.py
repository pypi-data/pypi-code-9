import logging
import time

import django.http
import django.template
from django.conf import settings
from django.db import connection
from django.contrib import auth
from django.contrib.auth import load_backend
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import RemoteUserBackend
from django.core.exceptions import ImproperlyConfigured
from django.utils.functional import SimpleLazyObject
from django.contrib.sites.models import Site
from django.http import HttpResponseRedirect

from django.conf import settings

class SiteMiddlewear(object):
    def process_request(self, request):
        try:

            request.site = Site.objects.get_current()
        except:
            request.site = {
                'domain': '',
                'name': settings.GRAPPELLI_ADMIN_TITLE,
            }



class CustomSettingsMiddlewear(object):
    def process_request(self, request):

        try:

            all_settings = settings.CUSTOM_SETTINGS
            for setting in all_settings:
                if hasattr(settings, setting):
                    value = getattr(settings, setting)
                    setattr(request, setting, value)
                    # print "Added %s to request %s"%(setting, getattr(request, setting))
        except:
            pass

class UseSearchIndexSettingsMiddlewear(object):
    def process_request(self, request):
        
        setting = 'USE_SEARCH_INDEX'
        from site_admin.utils.search_index import use_search_index
        setattr(request, setting, use_search_index)
        # print '- adding %s to request: %s'%(setting, getattr(request, setting))

class ImpersonateMiddleware(object):
    def process_request(self, request):
        request.impersonating = None
        request.original_user = None
        
        if hasattr(request, 'user') and request.user and request.user.is_authenticated() and  request.user.is_superuser and "__impersonate" in request.GET:
            request.session['impersonate_id'] = int(request.GET["__impersonate"])
        elif "__unimpersonate" in request.GET:
            if "impersonate_id" in request.session:
                del request.session['impersonate_id']

            if '__unimpersonate' in request.GET:
                new_query = request.GET.copy()
                del new_query['__unimpersonate']
                new_path = "%s?%s"%(request.path, new_query.urlencode())
                return HttpResponseRedirect(new_path)
        
        if hasattr(request, 'user') and request.user and request.user.is_authenticated() and request.user.is_superuser and 'impersonate_id' in request.session:
            try:
                UserModel = get_user_model()
                user = UserModel._default_manager.get(pk=request.session['impersonate_id'])
                request.original_user = request.user
                request.impersonating = request.user = user   
                

                if '__impersonate' in request.GET:
                    new_query = request.GET.copy()
                    del new_query['__impersonate']
                    new_path = "%s?%s"%(request.path, new_query.urlencode())
                    return HttpResponseRedirect(new_path)


            except:
                pass


class AdminLoggedInCookieMiddlewear(object):
    def process_response(self, request, response):

        is_staff = hasattr(request, 'user') and request.user and request.user.is_authenticated() and request.user.is_staff
        if is_staff and not request.COOKIES.get('admin_logged_in'):
            response.set_cookie("admin_logged_in", '1')
        elif not is_staff and request.COOKIES.get('admin_logged_in'):
            response.delete_cookie("admin_logged_in")
        return response

class UserIDCookieMiddlewear(object):
    def process_response(self, request, response):

        is_logged_in = hasattr(request, 'user') and request.user and request.user.is_authenticated()
        if is_logged_in and not request.COOKIES.get('user_id'):
            response.set_cookie("user_id", request.user.id)
        elif not is_logged_in and request.COOKIES.get('user_id'):
            response.delete_cookie("user_id")
        return response
                


class Django403Middleware(object):
  """Replaces vanilla django.http.HttpResponseForbidden() responses
  with a rendering of 403.html
  """
  def process_response(self, request, response):
    # If the response object is a vanilla 403 constructed with
    # django.http.HttpResponseForbidden() then call our custom 403 view
    # function
    if isinstance(response, django.http.HttpResponseForbidden) and \
        set(dir(response)) == set(dir(django.http.HttpResponseForbidden())):
      import views
      try:
        return views.access_denied(request)
      except django.template.TemplateDoesNotExist, e:
        return views.fallback_403(request)

    return response


class LoggingMiddleware(object):
    
    def process_request(self, request):
        self.start_time = time.time()

    def process_response(self, request, response):
        try:    
            remote_addr = request.META.get('REMOTE_ADDR')    
            if remote_addr in getattr(settings, 'INTERNAL_IPS', []):
                remote_addr = request.META.get('HTTP_X_FORWARDED_FOR') or remote_addr
            user_email = "-" 
            extra_log = ""
            if hasattr(request,'user'):
                user_email = getattr(request.user, 'email', '-')
            req_time = time.time() - self.start_time
            content_len = len(response.content)
            if settings.DEBUG:
                sql_time = sum(float(q['time']) for q in connection.queries) * 1000
                extra_log += " (%s SQL queries, %s ms)" % (len(connection.queries), sql_time)
            logging.info("%s %s %s %s %s %s (%.02f seconds)%s" % (remote_addr, user_email, request.method, request.get_full_path(), response.status_code, content_len, req_time, extra_log))
        except Exception, e:
            logging.error("LoggingMiddleware Error: %s" % e)
        return response