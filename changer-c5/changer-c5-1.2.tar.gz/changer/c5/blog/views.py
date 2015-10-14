from django.core.paginator import Paginator
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import get_object_or_404

from changer.c5.blog.models import Post

def list_posts(request):
    page = request.GET.get('page', 1)
    paginator = Paginator(Post.objects.all().order_by('-pub_date'), 5)
    context = {
        'paginator': paginator,
        'posts': paginator.page(page).object_list,
        'curpage': int(page)
        }
    return render_to_response('blog/listposts.html', context, context_instance=RequestContext(request))

def view_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    context = {'post': post}
    return render_to_response('blog/viewpost.html', context, context_instance=RequestContext(request))
