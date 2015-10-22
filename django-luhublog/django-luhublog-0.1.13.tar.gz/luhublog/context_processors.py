# -*- encoding: utf-8 -*-

from luhublog.models import Entry, Blog

BLOG = Blog.objects.get_blog()

def blog_info(request):
	return {'blog' : BLOG }
