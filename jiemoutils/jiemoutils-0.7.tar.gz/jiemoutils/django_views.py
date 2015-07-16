from django.core.context_processors import csrf
from mako.lookup import TemplateLookup
from mako import exceptions
from django import http
import inspect


def none_empty(o):
    return o if o else ''


def csrf_token(request):
    return '<input type="hidden" name="csrfmiddlewaretoken" value="%s" />' % csrf(request)["csrf_token"]


def model_from_form(obj, form):
    cd = form.cleaned_data
    for v in vars(obj):
        if v in cd:
            setattr(obj, v, cd[v])


class TemplateRender(object):

    def __init__(self, template_dirs, imports):
        myimport = ['from jiemoutils.django_views import none_empty, csrf_token']
        if imports:
            myimport.extend(imports)
        self.lookup = TemplateLookup(
            directories=template_dirs,
            input_encoding='utf-8',
            output_encoding='utf-8',
            default_filters=['none_empty', 'h', ],
            imports=myimport,
        )

    def render_to_response(self, filename, ctx):
        try:
            tp = self.lookup.get_template(filename)
            cont = tp.render(**ctx)
            return http.HttpResponse(cont)
        except :
            return http.HttpResponse(exceptions.html_error_template().render())


class ModuleHandler(object):

    def __init__(self, module):
        fs = inspect.getmembers(module, inspect.isfunction)
        self.funcs = {}
        for func in fs:
            if func[0].startswith('v_'):
                self.funcs[func[0]] = func[1]

    def handle(self, request, func_name):
        fname = 'v_' + func_name
        if fname not in self.funcs:
            return http.HttpResponseNotFound('page not found')
        return self.funcs[fname](request)
