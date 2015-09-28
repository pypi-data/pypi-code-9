from hmac import new
from time import time
from urllib.parse import urlencode
from urllib.parse import urlunsplit

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.views.defaults import permission_denied


@login_required
def freshdesk_login(request):
    host_name = request.GET.get('host_url', None)

    if not host_name:
        return permission_denied(request)

    shared_secret = settings.FRESHDESK_SHARED_SECRETS.get(host_name, None)

    if not shared_secret:
        return permission_denied(request)

    timestamp = int(time())
    auth_data = '{0}{1}{2}'.format(request.user.username, request.user.email, timestamp).encode('latin1')
    auth_hash = new(key=shared_secret, msg=auth_data, digestmod='MD5')

    query_dict = {
        'name': request.user.username,
        'email': request.user.email,
        'timestamp': timestamp,
        'hash': auth_hash.hexdigest()
    }

    location = urlunsplit(('https', host_name, '/login/sso', urlencode( [(key, query_dict[key]) for key in sorted(query_dict)] ), ''))

    return HttpResponseRedirect(location)


@login_required
def freshdesk_logout(request):
    host_name = request.GET.get('host_url', None)

    if not host_name:
        return permission_denied(request)

    location = urlunsplit(('https', host_name, '/', '', ''))

    return HttpResponseRedirect(location)
