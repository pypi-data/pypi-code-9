from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect

from wordpress_auth_lite.utils import get_login_url


def wordpress_login_required(fn, *args, **kwargs):
    def wrapped(request, *args, **kwargs):
        if not request.wordpress_user:
            redirect_to = request.build_absolute_uri(request.path)
            return redirect(get_login_url() + "?redirect_to=" + redirect_to)
        else:
            return fn(request, *args, **kwargs)
    return wrapped
