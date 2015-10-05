#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = u"Rafał Selewońko <rafal@selewonko.com>"


from django.http import Http404, HttpResponseRedirect
from django.utils.translation import ugettext as _
from django.views.generic import DetailView


class PageDetailView(DetailView):
    context_object_name = 'page'
    template_name = "pages/base.html"
    slug_field = 'slug'
    object = None

    def get(self, request, path):
        self.object = self.get_object()
        try:
            return HttpResponseRedirect(self.object.options.redirection_url)
        except AttributeError:
            pass
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_object(self, queryset=None):
        """
        Returns the object the view is displaying.

        By default this requires `self.queryset` and a `pk` or `slug`
        argument in the URLconf. This method overrides to return single
        object by `path`.
        """

        if self.object is not None:
            return self.object

        if queryset is None:
            queryset = self.get_queryset()

        path = self.kwargs.get('path', '')

        try:
            # Get the single item from the filtered queryset
            obj = queryset.get_by_path(path, slug_field=self.slug_field)
        except queryset.model.DoesNotExist:
            raise Http404(_("No %(verbose_name)s found matching the query") %
                          {'verbose_name': queryset.model._meta.verbose_name})
        return obj

    def get_template_names(self):
        if self.object.template_name:
            return [self.object.template_name]
        else:
            return super(PageDetailView, self).get_template_names()
