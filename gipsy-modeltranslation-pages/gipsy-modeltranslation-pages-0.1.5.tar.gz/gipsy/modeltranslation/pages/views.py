#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = u"Rafał Selewońko <rafal@selewonko.com>"


from gipsy.modeltranslation.pages.models import Page
from gipsy.pages.views_base import PageDetailView as PageDetailViewBase
from django.conf import settings
from django.http import Http404, HttpResponseRedirect


class PageDetailView(PageDetailViewBase):
    model = Page
    queryset = Page.objects.active()

    def get(self, request, path):
        try:
            # in currently activated language
            self.object = self.get_object()
        except Http404:
            # try in different languages
            for language_code, _ in settings.LANGUAGES:
                self.slug_field = 'slug_%s' % language_code
                try:
                    obj = self.get_object()
                except Http404:
                    pass
                else:
                    # different language is in fact same language
                    if obj.path == path:
                        self.object = obj
                    else:
                        return HttpResponseRedirect(obj.get_absolute_url())

        return super(PageDetailView, self).get(request, path)


page_detail = PageDetailView.as_view()
