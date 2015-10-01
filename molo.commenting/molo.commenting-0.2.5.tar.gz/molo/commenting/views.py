from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils.translation import ugettext as _

import django_comments
from django_comments.views.moderation import perform_flag
from django_comments.views.comments import post_comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from molo.core.models import ArticlePage
from molo.commenting.models import MoloComment


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


def view_more_article_comments(request, page_id):
    article = get_object_or_404(ArticlePage, id=page_id)
    qs = MoloComment.objects.for_model(ArticlePage).filter(
        object_pk=page_id, parent__isnull=True)

    try:
        comments_per_page = settings.COMMENTS_PER_PAGE
    except AttributeError:
        comments_per_page = 20

    paginator = Paginator(qs, comments_per_page)
    page = request.GET.get('p', 1)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    return render(request, 'comments/comments.html', {
                  "self": article,
                  "comments": comments
                  })
