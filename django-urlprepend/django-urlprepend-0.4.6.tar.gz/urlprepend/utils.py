from django.conf import settings
from django.core import urlresolvers
from django.contrib.sites.models import Site
from django.http import HttpResponseRedirect
from urlparse import urlsplit, urlunsplit
from urlprepend import settings as urlprepend_settings


def prepend_url(url, request=None):
    """Given a url, prefixes the current prefix to it and returns it"""
    if url:
        from urlprepend.middleware import is_prepend, current_prepend  # prevent circular references
        prepend_url = is_prepend(request=request)

        if prepend_url:
            current_site = Site.objects.get_current()
            current_domain = current_site.domain
            parts = urlsplit( url )
            if (not parts.netloc or current_domain in parts.netloc) and len(url) > 0 and url[0] != '#' and url[0] != '{' and url[0] != '?' and url[0] != '.' and url[0] != '$':
                # tuple.
                parts = list( parts )
                #check to see that this url hasn't been prepended already
                if not parts[2].startswith('/'+ current_prepend()):
                    parts[2] = '/'+ current_prepend() + parts[2]

                url =urlunsplit( parts )

    return url

class PrependHttpResponseRedirect(HttpResponseRedirect):

    def __init__(self, redirect_to):
        super(PrependHttpResponseRedirect, self).__init__(redirect_to)
        prepend, path = strip_path(redirect_to)
        #Need to check to see if it is already prepended
        self['Location'] = prepend_url(path)


def is_prepend_independent(path):
    """
    Returns whether the path is prepend-independent.
    """
    if urlprepend_settings.PREPEND_INDEPENDENT_MEDIA_URL and settings.MEDIA_URL\
    and path.startswith(settings.MEDIA_URL):
        return True
    for regex in urlprepend_settings.PREPEND_INDEPENDENT_PATHS:
        if regex.search(path):
            return True
    return False

def strip_path(path):
    """

    """
    check = urlprepend_settings.PATH_RE.match(path)
    if check:
        path_info = check.group('path') or '/'
        if path_info.startswith('/'):
            return check.group('prepend'), path_info
    return '', path

def prepend_path(path, prepend=''):
    """

    """
    if not prepend or is_prepend_independent(path):
        return path
    else:
        return ''.join([u'/', prepend, path])


def strip_script_prefix(url):
    """
    Strips the SCRIPT_PREFIX from the URL. Because this function is meant for
    use in templates, it assumes the URL starts with the prefix.
    """
    assert url.startswith(urlresolvers.get_script_prefix()),\
    "URL must start with SCRIPT_PREFIX: %s" % url
    pos = len(urlresolvers.get_script_prefix()) - 1
    return url[:pos], url[pos:]
