from django.core.context_processors import csrf
from mako.lookup import TemplateLookup
from mako import exceptions
from django import http
import inspect


# 模板过滤器，None转化为字符串的结果为“None”，实际应用通常需要显示为“”，这个函数作为过滤器使用可以达到效果
def none_empty(o):
    return o if o else ''


# mako无法直接使用{%csrf%}，因此编写下面函数
def csrf_token(request):
    return '<input type="hidden" name="csrfmiddlewaretoken" value="%s" />' % csrf(request)["csrf_token"]


# 使用form中的数据填写obj中名字相同字段，采用反射的机制实现
def model_from_form(obj, form):
    cd = form.cleaned_data
    for v in vars(obj):
        if v in cd:
            setattr(obj, v, cd[v])


# 类封装了mako的模板render
class TemplateRender(object):

    # 设定相关的参数，传人模板路径，以及需要额外的import，相关的技术请查看mako文档
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

    # 渲染mako的模板，如果渲染过程中有异常，则显示mako的异常html，方便查找模板中的错误
    def render_to_response(self, filename, ctx):
        try:
            tp = self.lookup.get_template(filename)
            cont = tp.render(**ctx)
            return http.HttpResponse(cont)
        except :
            return http.HttpResponse(exceptions.html_error_template().render())


# 按照原有的django方式，添加一个新的页面需要修改urlpatterns，然后添加相关的处理函数，下面的类
# 会找到模块中所有以v_开头的函数，把相应页面交给相应的函数处理
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
