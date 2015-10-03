# coding: utf-8

"""informer views"""

from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View

from django.conf import settings

from informer.checker.base import BaseInformer, InformerException


class DefaultView(View):
    """
    Default view used for Angular JS web application
    """
    template = 'django-informer-index.html'

    def get(self, request):
        """
        GET /informer/
        """

        data = {
            'URL': reverse('default-informer')
        }

        return render(request, self.template, data, content_type='text/html')


class InformerDiscoverView(View):
    """
    Discover URL's from each informer registered on settings
    """

    def get(self, request):
        """
        GET /informer/discover/
        """

        DJANGO_INFORMERS = getattr(settings, 'DJANGO_INFORMERS', ())

        informers = []

        for namespace, classname in DJANGO_INFORMERS:
            name = classname.replace('Informer', '').lower()
            urlname = 'informer-%s' % name

            informer = {
                'name': name,
                'url': reverse(urlname)
            }

            informers.append(informer)

        return JsonResponse({'informers': informers})


class InformerView(View):
    """
    Get result from a specific Informer
    """

    def get(self, request, namespace, classname):
        """
        GET /informer/:name/
        """

        result = {
            'name': classname,
            'operational': None,
            'message': 'pending'
        }

        try:
            cls = BaseInformer.get_class(namespace, classname)

            informer = cls()

            operational, message = informer.check()

            result['operational'] = operational
            result['message'] = message
        except InformerException as error:
            result['message'] = '%s' % error

        return JsonResponse(result)
