# -*- coding: utf-8 -*-

import inspect
import copy

from django.template.loader import render_to_string
from django.core.urlresolvers import reverse
from django.test.runner import DiscoverRunner
from rest_framework.test import APITestCase, APIClient

from . import conf
from .collector import DocCollector, json_pretty_print

COLLECTOR = DocCollector()


class DocDiscoverRunner(DiscoverRunner):
    def run_tests(self, test_labels, extra_tests=None, **kwargs):
        ret = super(DocDiscoverRunner, self).run_tests(test_labels, extra_tests=None, **kwargs)
        COLLECTOR.render()
        return ret


class DocAPIClient(APIClient):
    def _base_environ(self, **request):
        request.update(conf.REQUEST_KWARGS)
        return super(APIClient, self)._base_environ(**request)

    def generic(self, method, path, data, content_type, **extra):
        response = super(DocAPIClient, self).generic(
            method, path, data, content_type, **extra)

        if response.status_code in (200, 201, 204, 400, 401):
            content_type = response.request.get('CONTENT_TYPE', content_type)
            response.request['CONTENT_TYPE'] = content_type

        COLLECTOR.add(self._detect_testcase(), self._make_doc(response, data))
        return response

    def get(self, path, data=None, **extra):
        if 'json' in extra.get('format', ''):
            extra['content_type'] = 'application/json'
        response = super(DocAPIClient, self).generic('GET', path, data, **extra)
        COLLECTOR.add(self._detect_testcase(), self._make_doc(response, data))
        return response

    def _encode_data(self, data, format=None, content_type=None):
        if not data:
            if format in ('json', 'jsonp'):
                return u'', 'application/json'
            elif format == 'html':
                return u'', 'html'
            else:
                return u'', 'application/txt'

        return super(DocAPIClient, self)._encode_data(data, format, content_type)

    def _detect_testcase(self):
        try:
            selfs = [x[0].f_locals.get('self') for x in inspect.stack()]
            return [x for x in selfs if isinstance(x, DocAPITestCase)][0]
        except IndexError:
            return

    def _make_doc(self, response, data=None):
        context = {
            'headers': [(k, v) for k, v in response.request.items()
                        if k == k.upper() and unicode(v)],
            'request_data': json_pretty_print(data),
            'response_data': json_pretty_print(response.content),
            'status': response.status_code,
        }

        if 'json' in response.request.get('CONTENT_TYPE', ''):
            context['type'] = 'json'
        elif 'html' in response.request.get('CONTENT_TYPE', ''):
            context['type'] = 'html'
        else:
            context['type'] = 'txt'

        return render_to_string(conf.REQUEST_TEMPLATE, context)


class DocAPITestCase(APITestCase):
    client_class = DocAPIClient
    caption = u'Caption'
    description = u'Description'

    def __call__(self, result=None):
        testMethod = getattr(self, self._testMethodName)
        COLLECTOR.add(self, testMethod.__doc__)
        return super(DocAPITestCase, self).__call__(result)

    def doc(self, text):
        COLLECTOR.add(self, text)

    def _url(self, viewname):
        if viewname:
            if isinstance(viewname, (list, tuple)):
                return reverse(viewname[0], args=viewname[1:])
            elif isinstance(viewname, dict):
                view_name = copy.deepcopy(viewname)
                return reverse(view_name.pop('viewname'), kwargs=view_name)
            elif viewname[0] != '/':
                return reverse(viewname)
        return viewname

    def get(self, viewname, data=None, format='json'):
        return self.client.get(self._url(viewname), format)

    def put(self, viewname, data=None, format='json'):
        return self.client.put(self._url(viewname), data, format)

    def post(self, viewname, data=None, format='json'):
        return self.client.post(self._url(viewname), data, format)

    def patch(self, viewname, data=None, format='json'):
        return self.client.patch(self._url(viewname), data, format)

    def delete(self, viewname, data=None, format='json'):
        return self.client.delete(self._url(viewname), data, format)
