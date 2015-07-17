#-*- coding: utf-8 -*-
import os
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.templatetags.static import static

from django.contrib.staticfiles import finders
from django.template import engines

@csrf_exempt
def render_static_file(request, static_file=None):
    if static_file is None:
        query_dict = request.POST
        static_file = query_dict['static_file']

    path_static_file = finders.find(static_file)
    f = open(path_static_file, 'r')
    data = f.read()

    t = engines['django'].from_string(data)
    # t = loader.get_template_from_string(data)
    c = RequestContext(request)
    return HttpResponse(t.render(c))

@csrf_exempt
def url_reverse(request, view=None, args=None):
    if view is None and args is None:
        query_dict = request.POST
        view = query_dict['view']
        args = query_dict['args']
    arg_list = args.split(',')
    return HttpResponse(reverse(view, args=arg_list))