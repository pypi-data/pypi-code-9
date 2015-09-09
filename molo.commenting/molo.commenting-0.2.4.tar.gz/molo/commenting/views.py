from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext as _

import django_comments
from django_comments.views.moderation import perform_flag
from django_comments.views.comments import post_comment


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


@login_required
def post_molo_comment(request, next=None, using=None):
    """
    Allows for posting of a Molo Comment, this allows comments to
    be set with the "user_name" as "Anonymous"
    """
    data = request.POST.copy()
    if 'submit_anonymously' in data:
        data['name'] = _('Anonymous')
    # replace with our changed POST data

    # ensure we always set an email
    data['email'] = request.user.email or 'blank@email.com'

    request.POST = data
    return post_comment(request, next=next, using=next)
