from collections import OrderedDict
from datetime import datetime
from errno import EEXIST
from json import dumps
from json import loads
from os import makedirs
from os.path import dirname

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.core.exceptions import ImproperlyConfigured
from django.db.models import Model
from django.db.models.query import QuerySet
from django.forms.models import model_to_dict
from django.http import Http404
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.template import RequestContext
from django.utils.decorators import method_decorator
from django.utils.functional import Promise
from django.views.decorators.gzip import gzip_page
from django.views.generic import View

from weasyprint import HTML

from pages.models import MenuPage
from pages.models import Page
from pages.models import PageContents
from pages.models import PageFooter
from pages.models import PageHeader
from pages.models import Template

from localization.models import Language


HTTP_CONTENT_TYPE = 'http_content_type'
HTTP_ACCEPT       = 'http_accept'


def write_file(path, contents):
    try:
        makedirs(dirname(path))
    except OSError as exception:
        if exception.errno != EEXIST:
            raise

    with open(path, 'w') as file:
        file.write(contents)


class HtmlGenerator(object):
    def __get_output(self, request, page, context_data):
        try:
            contents = PageContents.objects.get(page=page, language=request.LANGUAGE_ID).contents
        except PageContents.DoesNotExist:
            contents = ''

        try:
            header = PageHeader.objects.get(page=page, language=request.LANGUAGE_ID).header.contents
        except PageHeader.DoesNotExist:
            header = ''

        try:
            footer = PageFooter.objects.get(page=page, language=request.LANGUAGE_ID).footer.contents
        except PageFooter.DoesNotExist:
            footer = ''

        context_data.update({
            'cdn_prefix': settings.PROJECT_CDN_PREFIX,
            'page':       page,
            'contents':   contents,
            'header':     header,
            'footer':     footer })

        context_data.update(csrf(request))
        template = loader.get_template(page.template.path)
        context = RequestContext(request, context_data)

        return template.render(context)

    def __call__(self, request, page, context_data):
        redirect_url = context_data.get('__redirect_url', None)
        dump_path = context_data.get('__dump_path', None)

        if redirect_url:
            if dump_path:
                output = self.__get_output(request, page, context_data)

                write_file(dump_path, output)

            return HttpResponseRedirect(redirect_url)
        else:
            output = self.__get_output(request, page, context_data)

            if dump_path:
                write_file(dump_path, output)

            return HttpResponse(output, content_type='text/html; charset=utf-8')


class JsonGenerator(object):
    def __materialize(self, level, value):
        if level > 256:
            return str(value)
        elif isinstance(value, QuerySet):
            result = []

            for item in value:
                result.append(self.__materialize(level + 1, item))

            return result
        elif isinstance(value, Model):
            model_dict = model_to_dict(value)
            result = {}

            try:
                secret_field_names = value._get_secret_field_names()

                for secret_field_name in secret_field_names:
                    del model_dict[secret_field_name]
            except AttributeError:
                pass

            for key in model_dict:
                result[key] = self.__materialize(level + 1, model_dict[key])

            result.update({ 'type': value._meta.model_name })

            return result
        elif isinstance(value, Promise):
            return str(value)
        elif isinstance(value, list):
            result = []

            for item in value:
                result.append(self.__materialize(level + 1, item))

            return result
        elif isinstance(value, dict):
            result = {}

            for key in value:
                result[key] = self.__materialize(level + 1, value[key])

            return result
        elif not isinstance(value, str) and hasattr(value, '__iter__'):
            result = []

            for item in value:
                result.append(self.__materialize(level + 1, item))

            return result
        elif isinstance(value, int):
            return value
        else:
            return str(value)

    def __get_output(self, request, page, context_data):
        context_data.update({'page': page.path})
        context_data.update(csrf(request))
        context_data = self.__materialize(0, context_data)

        if settings.DEBUG:
            return dumps(context_data, ensure_ascii=False, sort_keys=True, check_circular=True, indent=4, allow_nan=False)
        else:
            return dumps(context_data, ensure_ascii=False, sort_keys=True, check_circular=False)

    def __call__(self, request, page, context_data):
        redirect_url = context_data.get('__redirect_url', None)
        dump_path = context_data.get('__dump_path', None)

        if redirect_url:
            if dump_path:
                del context_data['__redirect_url']
                del context_data['__dump_path']

                output = self.__get_output(request, page, context_data)

                write_file(dump_path, output)

            return HttpResponseRedirect(redirect_url)
        else:
            if dump_path:
                del context_data['__dump_path']

                output = self.__get_output(request, page, context_data)

                write_file(dump_path, output)
            else:
                output = self.__get_output(request, page, context_data)

            return HttpResponse(output, content_type='application/json; charset=utf-8')


class PdfGenerator(object):
    def __get_output(self, request, page, context_data):
        try:
            contents = PageContents.objects.get(page=page, language=request.LANGUAGE_ID).contents
        except PageContents.DoesNotExist:
            contents = ''

        try:
            header = PageHeader.objects.get(page=page, language=request.LANGUAGE_ID).header.contents
        except PageHeader.DoesNotExist:
            header = ''

        try:
            footer = PageFooter.objects.get(page=page, language=request.LANGUAGE_ID).footer.contents
        except PageFooter.DoesNotExist:
            footer = ''

        context_data.update({
            'cdn_prefix': settings.PROJECT_CDN_PREFIX,
            'page':       page,
            'contents':   contents,
            'header':     header,
            'footer':     footer })

        context_data.update(csrf(request))
        template = loader.get_template(page.template.path)
        context = RequestContext(request, context_data)
        content = template.render(context)
        html = HTML(string=content, base_url=request.build_absolute_uri('/'))
        html_document = html.render()

        return html_document.write_pdf()

    def __call__(self, request, page, context_data):
        redirect_url = context_data.get('__redirect_url', None)
        dump_path = context_data.get('__dump_path', None)

        if redirect_url:
            if dump_path:
                output = self.__get_output(request, page, context_data)

                write_file(dump_path, output)

            return HttpResponseRedirect(redirect_url)
        else:
            output = self.__get_output(request, page, context_data)

            if dump_path:
                write_file(dump_path, output)

            response = HttpResponse(output, content_type='application/pdf')
            filename = context_data.get('filename', None)

            if filename:
                response['Content-Disposition'] = 'attachment; filename="{0}"'.format(filename)
            else:
                response['Content-Disposition'] = 'attachment; filename="document.pdf"'

            return response


class ContextViewMixin(object):
    def __any_data(self, request, page, **kwargs):
        return {}

    def __get_data(self, request, page, **kwargs):
        return {}

    def __set_data(self, request, page, **kwargs):
        return {}

    def __del_data(self, request, page, **kwargs):
        return {}

    def __try_call(self, name, request, page, **kwargs):
        if hasattr(self, name):
            call = getattr(self, name)

            if callable(call):
                return call(request, page, **kwargs)

        return {}

    def get_context_data(self, request, page, **kwargs):
        result = {}

        for base_type in reversed(type(self).mro()):
            result.update(self.__try_call('_{0}__any_data'.format(base_type.__name__), request, page, **kwargs))
            result.update(self.__try_call('_{0}__get_data'.format(base_type.__name__), request, page, **kwargs))

        return result

    def set_context_data(self, request, page, **kwargs):
        result = {}

        for base_type in reversed(type(self).mro()):
            result.update(self.__try_call('_{0}__any_data'.format(base_type.__name__), request, page, **kwargs))
            result.update(self.__try_call('_{0}__set_data'.format(base_type.__name__), request, page, **kwargs))

        return result

    def del_context_data(self, request, page, **kwargs):
        result = {}

        for base_type in reversed(type(self).mro()):
            result.update(self.__try_call('_{0}__any_data'.format(base_type.__name__), request, page, **kwargs))
            result.update(self.__try_call('_{0}__del_data'.format(base_type.__name__), request, page, **kwargs))

        return result


class PageViewMixin(object):
    def __init__(self):
        self._page_cache = {}

    def get_page(self, request, path_parts):
        try:
            path = Page.objects.get_path_from_parts(*path_parts)
            page = self._page_cache.get(path, None)

            if not page:
                page = Page.objects.prefetch_related('pageproperties', 'pageproperties__property').get(path=path)
                page.load_properties(request.LANGUAGE_ID)
                self._page_cache[path] = page

            return page
        except Page.DoesNotExist:
            raise Page.DoesNotExist("Page does not exist.\nQueried for \"{0}\"".format(path))
        except Page.MultipleObjectsReturned:
            raise Http404

    def get_pages(self, request, path_parts_list):
        paths = [Page.objects.get_path_from_parts(*path_parts) for path_parts in path_parts_list]
        pages = Page.objects.filter(path__in=paths)
        pages = pages.prefetch_related('pageproperties', 'pageproperties__property')

        if len(pages) != len(path_parts_list):
            raise Page.DoesNotExist("At least one page does not exist.\nQueried for \"{0}\"".format('\", \"'.join(paths)))

        page_map = {}

        for page in pages:
            page.load_properties(request.LANGUAGE_ID)
            page_map[page.path] = page

        return [page_map[path] for path in paths]


class VirtualPageViewMixin(object):
    def get_template_path(self):
        return 'virtual.html'

    def get_page(self, request, page_path):
        page = Page()
        page.id = 0
        page.path = page_path
        page.is_published = True
        page.template = Template()
        page.template.id = 0
        page.template.path = self.get_template_path()

        return page


class MultiTypeResponseMixin(object):
    def _get_accepted_media_type(self, media_range):
        media_range_parts = media_range.split(';')
        content_type, content_subtype = media_range_parts[0].split('/', 1)
        content_params = {}
        priority = 1.0

        for media_range_part in media_range_parts[1:]:
            param_key, param_value = media_range_part.split('=', 1)
            param_key = param_key.strip()
            param_value = param_value.strip()

            if param_key == 'q':
                priority = float(param_value)
            else:
                content_params[param_key] = param_value

        return (priority, content_type, content_subtype, content_params)

    def _get_accepted_media_types(self, http_accept):
        accepted_media_types = []

        for media_range in http_accept.split(','):
            if not media_range == '*/*':
                accepted_media_types.append(self._get_accepted_media_type(media_range))

        return accepted_media_types

    def _get_preferred_media_type(self, accepted_media_types, supported_media_types):
        preferred_supported_priority = -1.0
        preferred_supported_content_type = 'text'
        preferred_supported_content_subtype = 'html'

        for supported_media_type in supported_media_types:
            supported_content_type, supported_content_subtype = supported_media_type

            for accepted_media_type in accepted_media_types:
                accepted_priority, accepted_content_type, accepted_content_subtype, accepted_content_params = accepted_media_type

                if accepted_priority > preferred_supported_priority:
                    if (accepted_content_type == '*') or (accepted_content_type == supported_content_type):
                        if (accepted_content_subtype == '*') or (accepted_content_subtype == supported_content_subtype):
                            preferred_supported_priority = accepted_priority
                            preferred_supported_content_type = supported_content_type
                            preferred_supported_content_subtype = supported_content_subtype

        return preferred_supported_content_type, preferred_supported_content_subtype

    def get_request_media_type(self, request, supported_types):
        content_type = request.META.get('CONTENT_TYPE', 'text/html')
        accepted_media_types = self._get_accepted_media_types(content_type)

        if HTTP_CONTENT_TYPE in request.GET:
            accepted_media_types.insert(0, self._get_accepted_media_type(request.GET[HTTP_CONTENT_TYPE]))

        accepted_media_types = sorted(accepted_media_types, key=lambda x: -x[0])

        return self._get_preferred_media_type(accepted_media_types, supported_types)

    def get_response_media_type(self, request, supported_types):
        http_accept = request.META.get('HTTP_ACCEPT', 'text/html')
        accepted_media_types = self._get_accepted_media_types(http_accept)

        if HTTP_ACCEPT in request.GET:
            accepted_media_types.insert(0, self._get_accepted_media_type(request.GET[HTTP_ACCEPT]))

        accepted_media_types = sorted(accepted_media_types, key=lambda x: -x[0])

        return self._get_preferred_media_type(accepted_media_types, supported_types)

    def is_html(self, content_type, content_subtype):
        return (content_type == 'text') and (content_subtype == 'html')

    def is_json(self, content_type, content_subtype):
        return ((content_type == 'application') and (content_subtype == 'json')) or ((content_type == 'text') and (content_subtype == 'json'))

    def is_pdf(self, content_type, content_subtype):
        return (content_type == 'application') and (content_subtype == 'pdf')


class PageHtmlViewBase(ContextViewMixin, MultiTypeResponseMixin):
    def __any_data(self, request, page, **kwargs):
        return {
            'language_id':   request.LANGUAGE_ID,
            'language_code': request.LANGUAGE_CODE,
            'languages':     self.get_languages(request) }

    def get_languages(self, request):
        return Language.objects.filter(is_published=True)

    def get_menu_pages(self, request, menu_code):
        menu_pages = MenuPage.objects.filter(menu__code=menu_code, page__is_published=True)
        menu_pages = menu_pages.select_related('page')
        menu_pages = menu_pages.prefetch_related('page__pageproperties', 'page__pageproperties__property')

        for menu_page in menu_pages:
            menu_page.page.load_properties(request.LANGUAGE_ID)
            yield menu_page.page

    def __get_request_media_type(self, request):
        return self.get_request_media_type(request, [('application', 'json'), ('text', 'json'), ('text', 'html')])

    def __get_response_media_type(self, request):
        return self.get_response_media_type(request, [('application', 'json'), ('application', 'pdf'), ('text', 'json'), ('text', 'html')])

    def do_get(self, request, path_parts, **kwargs):
        response_content_type, response_content_subtype = self.__get_response_media_type(request)
        page = self.get_page(request, path_parts)
        context_data = self.get_context_data(request, page, **kwargs)

        if self.is_html(response_content_type, response_content_subtype):
            return self.html(request, page, context_data)
        elif self.is_json(response_content_type, response_content_subtype):
            return self.json(request, page, context_data)
        elif self.is_pdf(response_content_type, response_content_subtype):
            return self.pdf(request, page, context_data)
        else:
            raise ImproperlyConfigured('Preferred response content type = "{0}/{1}"'.format(response_content_type, response_content_subtype))

    def do_set(self, request, path_parts, **kwargs):
        request_content_type, request_content_subtype = self.__get_response_media_type(request)

        if 'json' in request.POST:
            request.JSON = loads(request.POST['json'], object_pairs_hook=OrderedDict)
        elif 'json' in request.FILES:
            request.JSON = loads(request.FILES['json'].read().decode('UTF-8'), object_pairs_hook=OrderedDict)
        elif self.is_json(request_content_type, request_content_subtype):
            request.JSON = loads(request.body.decode('UTF-8'), object_pairs_hook=OrderedDict)
        else:
            request.JSON = None

        response_content_type, response_content_subtype = self.__get_response_media_type(request)
        page = self.get_page(request, path_parts)
        context_data = self.set_context_data(request, page, **kwargs)

        if self.is_html(response_content_type, response_content_subtype):
            return self.html(request, page, context_data)
        elif self.is_json(response_content_type, response_content_subtype):
            return self.json(request, page, context_data)
        elif self.is_pdf(response_content_type, response_content_subtype):
            return self.pdf(request, page, context_data)
        else:
            raise ImproperlyConfigured('Preferred response content type = "{0}/{1}"'.format(response_content_type, response_content_subtype))

    def do_del(self, request, path_parts, **kwargs):
        response_content_type, response_content_subtype = self.__get_response_media_type(request)
        page = self.get_page(request, path_parts)
        context_data = self.del_context_data(request, page, **kwargs)

        if self.is_html(response_content_type, response_content_subtype):
            return self.html(request, page, context_data)
        elif self.is_json(response_content_type, response_content_subtype):
            return self.json(request, page, context_data)
        elif self.is_pdf(response_content_type, response_content_subtype):
            return self.pdf(request, page, context_data)
        else:
            raise ImproperlyConfigured('Preferred response content type = "{0}/{1}"'.format(response_content_type, response_content_subtype))


class PageJsonViewBase(ContextViewMixin, MultiTypeResponseMixin):
    def __get_request_media_type(self, request):
        return self.get_request_media_type(request, [('application', 'json'), ('application', 'pdf'), ('text', 'json'), ('text', 'html')])

    def __get_response_media_type(self, request):
        return self.get_response_media_type(request, [('application', 'json'), ('text', 'json')])

    def do_get(self, request, path_parts, **kwargs):
        response_content_type, response_content_subtype = self.__get_response_media_type(request)
        page = self.get_page(request, path_parts)
        context_data = self.get_context_data(request, page, **kwargs)

        if self.is_json(response_content_type, response_content_subtype):
            return self.json(request, page, context_data)
        else:
            raise ImproperlyConfigured('Preferred response content type = "{0}/{1}"'.format(response_content_type, response_content_subtype))

    def do_set(self, request, path_parts, **kwargs):
        request_content_type, request_content_subtype = self.__get_request_media_type(request)

        if 'json' in request.POST:
            request.JSON = loads(request.POST['json'], object_pairs_hook=OrderedDict)
        elif 'json' in request.FILES:
            request.JSON = loads(request.FILES['json'].read().decode('UTF-8'), object_pairs_hook=OrderedDict)
        elif self.is_json(request_content_type, request_content_subtype):
            request.JSON = loads(request.body.decode('UTF-8'), object_pairs_hook=OrderedDict)
        else:
            request.JSON = None

        response_content_type, response_content_subtype = self.__get_response_media_type(request)
        page = self.get_page(request, path_parts)
        context_data = self.set_context_data(request, page, **kwargs)

        if self.is_json(response_content_type, response_content_subtype):
            return self.json(request, page, context_data)
        else:
            raise ImproperlyConfigured('Preferred response content type = "{0}/{1}"'.format(response_content_type, response_content_subtype))

    def do_del(self, request, path_parts, **kwargs):
        response_content_type, response_content_subtype = self.__get_response_media_type(request)
        page = self.get_page(request, path_parts)
        context_data = self.del_context_data(request, page, **kwargs)

        if self.is_json(response_content_type, response_content_subtype):
            return self.json(request, page, context_data)
        else:
            raise ImproperlyConfigured('Preferred response content type = "{0}/{1}"'.format(response_content_type, response_content_subtype))


class PathPartHandlerBase(View, object):
    def get_path_parts(self, kwargs):
        parts = []
        count = 0

        for index in range(0, 10):
            name = 'path{0}'.format(index)
            part = kwargs.get(name)

            if part:
                parts.append(part)
                count = index + 1
            else:
                parts.append('{}')

        return parts[0:count]


class AnonymousHandlerBase(PathPartHandlerBase):
    @method_decorator(gzip_page)
    def get(self, request, **kwargs):
        return self.do_get(request, self.get_path_parts(kwargs), **kwargs)

    @method_decorator(gzip_page)
    def put(self, request, **kwargs):
        return self.do_set(request, self.get_path_parts(kwargs), **kwargs)

    @method_decorator(gzip_page)
    def post(self, request, **kwargs):
        return self.do_set(request, self.get_path_parts(kwargs), **kwargs)

    @method_decorator(gzip_page)
    def delete(self, request, **kwargs):
        return self.do_del(request, self.get_path_parts(kwargs), **kwargs)


class AuthenticatedHandlerBase(PathPartHandlerBase):
    @method_decorator(login_required)
    def get(self, request, **kwargs):
        return self.do_get(request, self.get_path_parts(kwargs), **kwargs)

    @method_decorator(login_required)
    def put(self, request, **kwargs):
        return self.do_set(request, self.get_path_parts(kwargs), **kwargs)

    @method_decorator(login_required)
    def post(self, request, **kwargs):
        return self.do_set(request, self.get_path_parts(kwargs), **kwargs)

    @method_decorator(login_required)
    def delete(self, request, **kwargs):
        return self.do_del(request, self.get_path_parts(kwargs), **kwargs)


class AnonymousPageHtmlView(AnonymousHandlerBase, PageViewMixin, PageHtmlViewBase):
    def __init__(self):
        PageViewMixin.__init__(self)
        self.html = HtmlGenerator()
        self.json = JsonGenerator()
        self.pdf  = PdfGenerator()


class AuthenticatedPageHtmlView(AuthenticatedHandlerBase, PageViewMixin, PageHtmlViewBase):
    def __init__(self):
        PageViewMixin.__init__(self)
        self.html = HtmlGenerator()
        self.json = JsonGenerator()
        self.pdf  = PdfGenerator()


class AnonymousPageJsonView(AnonymousHandlerBase, PageViewMixin, PageJsonViewBase):
    def __init__(self):
        PageViewMixin.__init__(self)
        self.json = JsonGenerator()


class AuthenticatedPageJsonView(AuthenticatedHandlerBase, PageViewMixin, PageJsonViewBase):
    def __init__(self):
        PageViewMixin.__init__(self)
        self.json = JsonGenerator()


class VirtualAnonymousPageHtmlView(AnonymousHandlerBase, VirtualPageViewMixin, PageHtmlViewBase):
    def __init__(self):
        self.html = HtmlGenerator()
        self.json = JsonGenerator()
        self.pdf  = PdfGenerator()


class VirtualAuthenticatedPageHtmlView(AuthenticatedHandlerBase, VirtualPageViewMixin, PageHtmlViewBase):
    def __init__(self):
        self.html = HtmlGenerator()
        self.json = JsonGenerator()
        self.pdf  = PdfGenerator()


class VirtualAnonymousPageJsonView(AnonymousHandlerBase, VirtualPageViewMixin, PageJsonViewBase):
    def __init__(self):
        self.json = JsonGenerator()


class VirtualAuthenticatedPageJsonView(AuthenticatedHandlerBase, VirtualPageViewMixin, PageJsonViewBase):
    def __init__(self):
        self.json = JsonGenerator()


class DefaultHtmlView(AnonymousPageHtmlView):
    def __init__(self):
        self.html = HtmlGenerator()
        self.json = JsonGenerator()
        self.pdf  = PdfGenerator()

    def __get_data(self, request, page, **arguments):
        menu_pages = self.get_menu_pages(request, 'default')

        return { 'menu_pages': menu_pages }


class SiteMapXmlView(View):
    @method_decorator(gzip_page)
    def get(self, request):
        pages = PageContents.objects.filter(page__is_published=True, language__is_published=True)
        now = datetime.now()

        return render(
            request,
            'pages/sitemap.xml',
            {
                'host': settings.ALLOWED_HOSTS[0],
                'pages': pages,
                'now': now
            },
            content_type='text/xml charset=utf-8')
