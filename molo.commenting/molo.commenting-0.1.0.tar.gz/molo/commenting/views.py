from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _

import django_comments
from django_comments.views.moderation import perform_flag


@login_required
def report(request, comment_id):
    """
    Flags a comment on GET.

    Redirects to whatever is provided in request.REQUESRT['next'].
    """

    comment = get_object_or_404(
        django_comments.get_model(), pk=comment_id, site__pk=settings.SITE_ID)

    next = request.GET.get('next') or comment.get_absolute_url()
    perform_flag(request, comment)
    messages.info(request, _('The comment has been reported.'))
    return HttpResponseRedirect(next)
