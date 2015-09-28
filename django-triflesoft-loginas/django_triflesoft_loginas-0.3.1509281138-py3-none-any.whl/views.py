from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY
from django.contrib.auth import get_user_model
from django.contrib.auth import load_backend
from django.contrib.auth import login
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.defaults import page_not_found
from django.views.defaults import permission_denied


LOGINAS_IMPERSONATOR_ID_KEY = 'loginas_impersonator_id'
LOGINAS_IMPERSONATOR_FULLNAME_KEY = 'loginas_impersonator_full_name'


def __get_user(request, user_id):
    if user_id is None:
        return None

    try:
        backend = load_backend(request.session[BACKEND_SESSION_KEY])

        user = get_user_model().objects.get(id=user_id)
        user.backend = "%s.%s" % (backend.__module__, backend.__class__.__name__)

        return user
    except ObjectDoesNotExist:
        return None


def login_as(request):
    if not request.user.is_superuser:
        return permission_denied(request)

    try:
        id = request.GET.get('id', '0')
    except ValueError:
        return page_not_found(request)

    impersonator = request.user
    user = __get_user(request, id)

    login(request, user)

    request.session[LOGINAS_IMPERSONATOR_ID_KEY] = impersonator.id
    request.session[LOGINAS_IMPERSONATOR_FULLNAME_KEY] = impersonator.get_full_name()

    return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)


def logout_as(request):
    id = request.session.get(LOGINAS_IMPERSONATOR_ID_KEY, 0)

    if id == 0:
        return permission_denied(request)

    user = __get_user(request, id)

    login(request, user)

    return HttpResponseRedirect(reverse('admin:auth_user_changelist'))
