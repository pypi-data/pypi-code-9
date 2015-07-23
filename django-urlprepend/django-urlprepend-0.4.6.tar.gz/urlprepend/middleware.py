import re

from django.contrib.sites.models import Site
from django.conf import settings
import django.core.exceptions
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.utils import translation
from django.utils.cache import patch_vary_headers
# TODO importing undocumented function
from django.utils.translation.trans_real import parse_accept_lang_header
from urlprepend import settings as urlprepend_settings
from urlprepend import utils
from urlparse import urlsplit, urlunsplit

import threading
_thread_locals = threading.local()

def is_prepend(request=None):
    """Returns boolean indicating if prepending is taking place"""
    if request:
        return (getattr(_thread_locals, 'IS_PREPEND', False) or (getattr(request, 'IS_PREPEND', False)))
    else:
        return getattr(_thread_locals, 'IS_PREPEND', False)

def current_prepend(request=None):
    """Returns the currently active prefix string if there is one in operation. If no prepending is taking place then '' is returned"""
    if is_prepend(request=request):
        # This attribute should always be there when is_prepend() is True
        if request and (getattr(request, 'prepend_string', None)):
            return request.prepend_string
        elif (getattr(_thread_locals, 'PREPEND_STRING', None)):
            return _thread_locals.PREPEND_STRING
        else:
            return ''
    else:
        return ''


class PrependURLMiddleware(object):
    """
   
    """

    def process_request(self, request):
        # Clear these at the start of each request
        request.IS_PREPEND = _thread_locals.IS_PREPEND = False
        request.prepend_string = _thread_locals.PREPEND_STRING = ""
        prepend, path = utils.strip_path(request.path_info)
        #logging.debug('using iframe %s for path %s' %(str(prepend=='i'), path))
        
        prepend_independant = utils.is_prepend_independent(path)        
        prepend_path = utils.prepend_path(path, prepend)
        if prepend_path != request.path_info:
            if request.META.get("QUERY_STRING", ""):
                prepend_path = "%s?%s" % (prepend_path,request.META['QUERY_STRING'])
            return HttpResponsePermanentRedirect(prepend_path)
        request.path_info = path
        if not prepend_independant:
            request.IS_PREPEND = (prepend != '')
            request.prepend_string = prepend
            _thread_locals.IS_PREPEND = request.IS_PREPEND
            _thread_locals.PREPEND_STRING = prepend

            if prepend != '':
                request.META['HTTP_X_URLPREPEND_STRING'] = prepend
                pass
        
    def process_response(self, request, response):
        if response.status_code == 404 and not request.path_info.endswith('/') and settings.APPEND_SLASH:
            # Redirect to same path but with / appended
            new_path = request.path + "/"
            if request.GET:
                new_path += '?' + request.META['QUERY_STRING']
            return HttpResponseRedirect(new_path)

        #rewrite all the urls to use /i/
        alter_url = is_prepend(request=request)
        prepend_string = current_prepend(request=request)
        if alter_url:
            current_domain = Site.objects.get(id=settings.SITE_ID).domain
            _regex = '(?P<prefix><a.*?href=")(?P<url>.*?)(?P<suffix>".*?>)'
            _anchor_regex = re.compile( _regex , re.IGNORECASE)
            def a_replacer( match ):
                # The URL is captured by a named group in the regex.
                url = match.group( 'url' )
                parts = urlsplit( url )
            
                if (not parts.netloc or current_domain in parts.netloc) and len(url) > 0 and url[0] != '#' and url[0] != '{' and url[0] != '?' and url[0] != '.' and url[0] != '$':

                    prefix = match.group( 'prefix' )
                    suffix = match.group( 'suffix' )

                    #check suffix for a target _blank or target _parent. If they exist then to not alter the url
                    _target_regex = '(.*?target=["\'])(?P<target>.*?)(["\'].*?)'
                    _target_attr_regex = re.compile( _target_regex , re.IGNORECASE)
                    target_attrs = _target_attr_regex.search(suffix)

                    ignore_url = False
                    if target_attrs and target_attrs.group( 'target' ):
                        if target_attrs.group( 'target' ) in urlprepend_settings.PREPEND_TARGET_ATTRIBUTES_TO_IGNORE:
                            ignore_url = True

                    if not ignore_url:
                        # tuple.
                        parts = list( parts )
                        replace_string = "/%s" % prepend_string
                        if replace_string not in parts[2]:
                            parts[2] = '/%s%s' %(prepend_string, parts[2])

                        # Replace the named group 'url' in the match with the
                        # new URL.

                        anchor = prefix + urlunsplit( parts ) + suffix
                    else:
                        anchor = prefix + url + suffix
                    
                else:
                    anchor = match.group()

                return anchor
            
            _form_regex = '(?P<prefix><form.*?action=")(?P<url>.*?)(?P<suffix>".*?>)'
            _compiled_form_regex = re.compile( _form_regex , re.IGNORECASE)
            def form_replacer( match ):
                # The URL is captured by a named group in the regex.
                url = match.group( 'url' )
                parts = urlsplit( url )
                # Append the Coral CDN suffix to the 'netloc' URL part,
                # assuming it's there. If not, we're looking at local
                # reference so no need to rewrite the URL.
                if (not parts.netloc or current_domain in parts.netloc) and len(url) > 0 and url[0] != '#' and url[0] != '.' and url[0] != '{' and url[0] != '?' and url[0] != '$':
                    
                    # tuple.
                    parts = list( parts )
                    replace_string = "/%s" % prepend_string
                    if replace_string not in parts[2]:
                        parts[2] = '/%s%s' %(prepend_string, parts[2])

    
                    # Replace the named group 'url' in the match with the
                    # new URL.
                    prefix = match.group( 'prefix' )
                    suffix = match.group( 'suffix' )
                    action = prefix + urlunsplit( parts ) + suffix
                else:
                    action = match.group()
                    
                return action
            
            _iframe_regex = '(?P<prefix><iframe.*?src=")(?P<url>.*?)(?P<suffix>".*?>)'
            _compiled_iframe_regex = re.compile( _iframe_regex , re.IGNORECASE)
            def iframe_replacer( match ):
                # The URL is captured by a named group in the regex.
                url = match.group( 'url' )
                parts = urlsplit( url )
                # Append the Coral CDN suffix to the 'netloc' URL part,
                # assuming it's there. If not, we're looking at local
                # reference so no need to rewrite the URL.
                if (not parts.netloc or current_domain in parts.netloc) and len(url) > 0 and url[0] != '#' and url[0] != '.' and url[0] != '{' and url[0] != '?' and url[0] != '$':
                    
                    # tuple.
                    parts = list( parts )
                    replace_string = "/%s" % prepend_string
                    if replace_string not in parts[2]:
                        parts[2] = '/%s%s' %(prepend_string, parts[2])
    
                    # Replace the named group 'url' in the match with the
                    # new URL.
                    prefix = match.group( 'prefix' )
                    suffix = match.group( 'suffix' )
                    src = prefix + urlunsplit( parts ) + suffix
                else:
                    src = match.group()
                    
                return src
    
            # Find all anchor tags in the response content and rewrite
            # them.
            response.content = _anchor_regex.sub( a_replacer, response.content )
            response.content = _compiled_form_regex.sub( form_replacer, response.content )
            response.content = _compiled_iframe_regex.sub( iframe_replacer, response.content )

            response['X-Urlprepend-String'] = prepend_string
            patch_vary_headers(response, ['X-Urlprepend-String'])
            
        return response
