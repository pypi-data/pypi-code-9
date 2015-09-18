# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404, redirect
from django.views import generic
from django.core.exceptions import PermissionDenied
from django.template import RequestContext
from django.utils.http import urlquote_plus
from django.forms import ModelForm
from django.template import loader
from django.http import HttpResponse
from rapid.registry import registry, Action, MenuEntry
from rapid.wrappers import InstanceData, ModelData, FieldData
from rapid import permissions
from rapid.widgets import RapidSelector, RapidRelationReadOnly
from rapid.filters import FilterSet
import math

def _build_uri(request, params):
    param_string = "&".join(["%s=%s"%(urlquote_plus(k), urlquote_plus(params[k])) for k in params.keys()])
    base = request.build_absolute_uri().split("?")[0]
    return base + "?" + param_string

def _copy_dict(dc):
    d = {}
    for k in dc.keys():
        d[k] = dc[k]
    return d

def _replace_param(request, param_name, param_value):
    get = _copy_dict(request.GET)
    get[param_name] = param_value
    return _build_uri(request, get)

def is_ajax_request(request):
    # X-Requested-With: XMLHttpRequest
    w = request.META.get('HTTP_X_REQUESTED_WITH')
    if w:
        return True
    return False

class ListView(generic.list.ListView):
    template_name = 'rapid/bare/list.html'
    action_name = ''
    registers_per_page = 50
    number_of_edge_pages = 5
    number_of_middle_pages = 5
    fields = None

    class Pagination:
        def __init__(self, request, page, number_of_edge_pages, number_of_middle_pages, registers_per_page, total_pages):
            self.request = request
            self.number_of_edge_pages = number_of_edge_pages
            self.number_of_middle_pages = number_of_middle_pages
            self.registers_per_page = registers_per_page
            self.page = page
            self.total_pages = total_pages

        def _page_and_uri(self, pages):
            get2 = _copy_dict(self.request.GET)
            for p in pages:
                get2['page'] = p
                yield (p, _build_uri(self.request, get2))

        def start_numbers(self):
            """
            Números das páginas que serão listadas no começo da paginação.
            """
            e = self.number_of_edge_pages
            for i in range(1, min(e+1, self.page)):
                yield i

        def start(self):
            """
            Números e URL páginas que serão listadas no começo da paginação.
            """
            return self._page_and_uri(self.start_numbers())

        def before_numbers(self):
            """
            Números das páginas que serão listadas na paginação antes da atual.
            """
            m = self.number_of_middle_pages
            for i in range(max(self.page - m, m), self.page):
                yield i

        def before(self):
            """
            Números e URL das páginas que serão listadas na paginação antes da atual.
            """
            return self._page_and_uri(self.before_numbers())

        def after_numbers(self):
            """
            Números das páginas que serão listadas na paginação depois da atual.
            """
            m = self.number_of_middle_pages
            e = self.number_of_edge_pages
            for i in range(self.page + 1, min(self.page + m + 1, self.total_pages - e + 1)):
                yield i

        def after(self):
            """
            Números e URL das páginas que serão listadas na paginação depois da atual.
            """
            return self._page_and_uri(self.after_numbers())

        def end_numbers(self):
            """
            Números das páginas que serão listadas no final da paginação.
            """
            e = self.number_of_edge_pages
            for i in range(max(self.page + 1, self.total_pages - e + 1), self.total_pages + 1):
                yield i

        def end(self):
            """
            Números e URLs das páginas que serão listadas no final da paginação.
            """
            return self._page_and_uri(self.end_numbers())

        def separate_end(self):
            """
            Indica se deve haver um separador entre o começo da paginação e as páginas antes da atual.
            """
            return self.page < self.total_pages - self.number_of_edge_pages - self.number_of_middle_pages

        def separate_start(self):
            """
            Indica se deve haver um separador entre as páginas depois da atual e o fim da paginação.
            """
            return self.page > self.number_of_edge_pages + self.number_of_middle_pages

        def get_page(self, queryset):
            return queryset[self.registers_per_page*(self.page-1):self.registers_per_page*self.page]

    class View:
        order_param = 'order'

        def __init__(self, request, action_name, model, queryset, fields, pagination):
            self.request = request
            self.model = model
            self.action_name = action_name
            self._fields = fields

            q = queryset

            self.filters = FilterSet.from_request(ModelData(self.model), request)
            if self.filters:
                q = q.filter(**self.filters.query_dict())
                self.queryset = q

            total = q.count()
            pagination.total_pages = int(math.ceil(total / pagination.registers_per_page))

            order = request.GET.get(self.order_param)
            if order:
                q = q.order_by(order)
            self.queryset = pagination.get_page(q)

        def values(self):
            for o in self.queryset:
                if self._fields:
                    c = InstanceData(o, request=self.request, fields=self._fields)
                else:
                    c = InstanceData(o, request=self.request)
                if c.has_permission(self.request, self.action_name):
                    yield c

        def fields(self):
            order_param = self.order_param
            request = self.request

            class FieldParams:
                def __init__(self, field):
                    self.field = field

                def order_up_url(self):
                    return _replace_param(request, order_param, self.field.bare_name())

                def order_down_url(self):
                    return _replace_param(request, order_param, u'-' + self.field.bare_name())

                def add_filter_url(self):
                    pass

                def del_filter_url(self):
                    pass
            for f in ModelData(self.model, request=self.request, fields=self._fields).fields():
                f.view = FieldParams(f)
                yield f

    def get(self, request, **kwargs):
        mdata = ModelData(self.model, request)
        if not mdata.has_permission(request, self.action_name):
            raise PermissionDenied
        #De forma similar ao get de ListView, recupera os objetos e verifica
        #se pode mostrar uma lista vazia.
        object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()

        # Agora, popula o contexto com os request processors e os dados específicos
        # da listagem nos SA.
        context = RequestContext(request).flatten()
        context.update(kwargs)
        total_pages = int(math.ceil(object_list.count() / self.registers_per_page))
        page = int(request.GET.get('page', 1))
        p = self.Pagination(request, page, self.number_of_edge_pages,
                                      self.number_of_middle_pages, self.registers_per_page,
                                      total_pages)
        context['pages'] = p
        context['model'] = ModelData(self.model, request, fields=self.fields)
        context['view'] = self.View(request, self.action_name, self.model, object_list, self.fields, p)
        default_ordering = self.model._meta.ordering if hasattr(self.model._meta, 'ordering') else ''
        ordering = request.GET.get('order', default_ordering)
        offset = (page - 1) * self.registers_per_page
        self.object_list = object_list[offset: offset + self.registers_per_page]
        context[self.get_context_object_name(object_list)] = object_list
        context['object_list'] = object_list
        context = self.get_context_data(**context)
        self.object_list = object_list

        return self.render_to_response(context)

class ReadView(generic.detail.DetailView):
    template_name = 'rapid/bare/detail.html'
    action_name = ''
    request = None

    def get_object(self, request=None):
        return get_object_or_404(self.model, pk=self.kwargs['pk'])

    def get(self, request, pk, **kwargs):
        context = RequestContext(request).flatten()
        context.update(kwargs)

        obj = self.get_object(self.request)
        context['object'] = obj
        context[self.get_context_object_name(obj)] = obj

        cd = InstanceData(obj, request=request)
        if not cd.has_permission(request, self.action_name):
            raise PermissionDenied
        excludes = request.GET.get('exclude')
        if excludes:
            cd.excludes = excludes.split(",")
        self.object = cd
        context['object_data'] = cd

        context = self.get_context_data(**context)

        return self.render_to_response(context)

def _get_form(request, model):
    default_relations_bare = request.GET.get('default')
    widgets = []
    default_relations = []
    default_relations_fields = []
    if default_relations_bare:
        default_relations_fields = default_relations_bare.split(",")
        default_relations = [(x, int(y)) for (x, y) in (f.split(":") for f in default_relations_fields)]
        default_relations_fields = [x for x, y in default_relations]
        for (x, y) in default_relations:
            f = FieldData(getattr(model, x).field, request)
            widgets.append((x, RapidRelationReadOnly(f.related_model())))
    ask_relations = []
    for f in ModelData(model).local_fields():
        if f.is_relation() and unicode(f.bare_name()) not in default_relations_fields:
            ask_relations.append(f)
    widgets += [(f.bare_name(), RapidSelector(f)) for f in ask_relations if f.related_model().has_permission(request, 'select')]
    #ModelForm.Meta tem atributos com esses mesmos nomes,
    #então eu tenho que renomear.
    form_model = model
    form_widgets = dict(widgets)

    class CForm(ModelForm):
        def __init__(self, *args, **kwargs):
            initial = kwargs.get('initial', {})
            for (k, v) in default_relations:
                initial[k] = v
            kwargs['initial'] = initial
            super(CForm, self).__init__(*args, **kwargs)

        class Meta:
            model = form_model
            fields = '__all__'
            widgets = form_widgets
    return CForm



class CreateView(generic.edit.CreateView):
    template_name = 'rapid/bare/create.html'
    action_name = ''

    object = None

    fields = '__all__'

    def request_form(self, request):
        return _get_form(request, self.model)

    def get(self, request, **kwargs):
        context = RequestContext(request).flatten()
        context.update(kwargs)

        cd = ModelData(self.model, request=request)
        if not cd.has_permission(request, self.action_name):
            raise PermissionDenied
        context['model_data'] = cd

        parent_model = self.model
        parent_fields = self.fields

        if request.POST:
            context['form'] = self.request_form(request)(request.POST, request.FILEs)
        else:
            context['form'] = self.request_form(request)()

        context = self.get_context_data(**context)

        return self.render_to_response(context)

    def post(self, request, **kwargs):
        m = ModelData(self.model, request=request)
        if m.has_permission(request, self.action_name):
            f = self.request_form(request)(request.POST, request.FILES)
            if f.is_valid():
                f.save()
                return redirect(m.list_url())
            return self.get(request, **kwargs)
        raise PermissionDenied()

class UpdateView(generic.edit.UpdateView):
    template_name = 'rapid/bare/update.html'
    action_name = ''

    fields = '__all__'

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, pk=self.kwargs['pk'])

    def request_form(self, request):
        return _get_form(request, self.model)

    def get(self, request, pk, **kwargs):
        context = RequestContext(request).flatten()
        context.update(kwargs)

        obj = self.get_object()
        context['object'] = obj
        context[self.get_context_object_name(obj)] = obj

        cd = InstanceData(obj, request=request)
        if not cd.has_permission(request, self.action_name):
            raise PermissionDenied
        self.object = cd
        context['object_data'] = cd

        if request.POST:
            context['form'] = self.request_form(request)(request.POST, request.FILES, instance=obj)
        else:
            context['form'] = self.request_form(request)(instance=obj)

        context = self.get_context_data(**context)

        return self.render_to_response(context)

    def post(self, request, pk, **kwargs):
        obj = self.get_object()
        m = InstanceData(obj, request=request)
        if m.has_permission(request, self.action_name):
            f = self.request_form(request)(request.POST, request.FILES, instance=obj)
            if f.is_valid():
                if f.instance.pk != obj.pk:
                    raise PermissionDenied
                f.save()
                return redirect(m.list_url())
            self.form = f
            return self.get(request, pk, **kwargs)
        raise PermissionDenied


class DeleteView(generic.edit.DeleteView):
    template_name = 'rapid/bare/delete.html'
    action_name = ''

    fields = '__all__'

    def __init__(self, **kwargs):
        super(DeleteView, self).__init__(**kwargs)
        self.success_url = ModelData(self.model).list_url()

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, pk=self.kwargs['pk'])

    def get(self, request, *args, **kwargs):
        obj = InstanceData(self.get_object())
        if not obj.has_permission(request, self.action_name):
            raise PermissionDenied
        return super(DeleteView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        obj = InstanceData(self.get_object())
        if not obj.has_permission(request, self.action_name):
            raise PermissionDenied
        return super(DeleteView, self).post(request, *args, **kwargs)


class SelectView(ListView):
    """
    Apresenta uma lista selecionavel de objetos, para
    o preenchimento de relações.
    """
    template_name = 'rapid/bare/select.html'


def bare_or_main(view):
    main_window_template = "rapid/main_window.html"

    def vw(request, *args, **kwargs):
        resp = view(request, *args, **kwargs)
        bare = is_ajax_request(request)
        if bare:
            if resp.status_code >= 300 and resp.status_code <= 399:
                # I'll interpret redirects as successful POST,
                # thus, the response'll get replaced by something with
                # a header that says "success!"
                ret = HttpResponse('')
                ret['X-FORM-STATUS:'] = 'success'
                return ret
        if not bare and resp.status_code == 200 and request.method != "HEAD":
            resp.render()
            body = resp.content
            main_win = loader.get_template(main_window_template)
            context = RequestContext(request)
            context.update({'body_text': body, 'this_url': request.get_full_path()})
            resp.content = main_win.render(context, request)
        return resp
    return vw

def update_form_class(form):
    class F(UpdateView):
        def request_form(self, request):
            return form
    return F

