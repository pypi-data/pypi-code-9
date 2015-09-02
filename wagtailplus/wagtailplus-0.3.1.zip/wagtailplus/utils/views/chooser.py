"""
Contains application chooser view definitions.
"""
from django.http import Http404
from django.shortcuts import render

from wagtail.wagtailadmin.modal_workflow import render_modal_workflow
from wagtail.wagtailsearch.backends import get_search_backends

from .crud import IndexView


class ChooserView(IndexView):
    initial         = {}
    form_class      = None
    success_url     = None
    prefix          = None
    url_namespace   = None

    def form_invalid(self, form):
        """
        Processes an invalid form submittal.

        :param form: the form instance.
        :rtype: django.http.HttpResponse.
        """
        context = self.get_context_data(form=form)

        #noinspection PyUnresolvedReferences
        return render_modal_workflow(
            self.request,
            '{0}/chooser.html'.format(self.template_dir),
            '{0}/chooser.js'.format(self.template_dir),
            context
        )

    def form_valid(self, form):
        """
        Processes a valid form submittal.

        :param form: the form instance.
        :rtype: django.http.HttpResponse.
        """
        #noinspection PyAttributeOutsideInit
        self.object = form.save()

        # Index the link.
        for backend in get_search_backends():
            backend.add(self.object)

        #noinspection PyUnresolvedReferences
        return render_modal_workflow(
            self.request,
            None,
            '{0}/chosen.js'.format(self.template_dir),
            {'obj': self.get_json(self.object)}
        )

    def get(self, request, *args, **kwargs):
        """
        Returns GET response.

        :param request: the request instance.
        :rtype: django.http.HttpResponse.
        """
        #noinspection PyAttributeOutsideInit
        self.object_list    = self.get_queryset()
        context             = self.get_context_data(force_search=True)

        if self.form_class:
            context.update({'form': self.get_form()})

        if 'q' in request.GET or 'p' in request.GET:
            return render(
                request,
                '{0}/results.html'.format(self.template_dir),
                context
            )
        else:
            return render_modal_workflow(
                request,
                '{0}/chooser.html'.format(self.template_dir),
                '{0}/chooser.js'.format(self.template_dir),
                context
            )

    def get_form(self, form_class=None):
        """
        Returns an instance of the form to be used in this view.

        :param form_class: the form class to use.
        :rtype: django.forms.ModelForm.
        """
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(**self.get_form_kwargs())

    def get_form_class(self):
        """
        Returns the form class to use in this view.

        :rtype: class.
        """
        return self.form_class

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.

        :rtype: dict.
        """
        kwargs = {
            'initial':  self.get_initial(),
            'prefix':   self.get_prefix(),
        }

        #noinspection PyUnresolvedReferences
        if self.request.method in ('POST', 'PUT'):
            #noinspection PyUnresolvedReferences
            kwargs.update({
                'data':     self.request.POST,
                'files':    self.request.FILES,
            })

        if hasattr(self, 'object'):
            kwargs.update({'instance': self.object})

        return kwargs

    def get_initial(self):
        """
        Returns the initial data to use for forms on this view.

        :rtype: dict.
        """
        return self.initial.copy()

    def get_prefix(self):
        """
        Returns the prefix to use for forms on this view.

        :type: str.
        """
        return self.prefix

    #noinspection PyUnusedLocal
    def post(self, request, *args, **kwargs):
        """
        Returns POST response.

        :param request: the request instance.
        :rtype: django.http.HttpResponse.
        """
        #noinspection PyAttributeOutsideInit
        self.object_list    = self.get_queryset()
        form                = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

def chosen_view_factory(chooser_cls):
    """
    Returns a ChosenView class that extends specified chooser class.

    :param chooser_cls: the class to extend.
    :rtype: class.
    """
    class ChosenView(chooser_cls):
        #noinspection PyUnusedLocal
        def get(self, request, *args, **kwargs):
            """
            Returns GET response.

            :param request: the request instance.
            :rtype: django.http.HttpResponse.
            """
            #noinspection PyAttributeOutsideInit
            self.object = self.get_object()

            return render_modal_workflow(
                self.request,
                None,
                '{0}/chosen.js'.format(self.template_dir),
                {'obj': self.get_json(self.object)}
            )

        def get_object(self, queryset=None):
            """
            Returns chosen object instance.

            :param queryset: the queryset instance.
            :rtype: django.db.models.Model.
            """
            if queryset is None:
                queryset = self.get_queryset()

            pk = self.kwargs.get('pk', None)

            try:
                return queryset.get(pk=pk)
            except self.models.DoesNotExist:
                raise Http404()

        def post(self, request, *args, **kwargs):
            """
            Returns POST response.

            :param request: the request instance.
            :rtype: django.http.HttpResponse.
            """
            return self.get(request, *args, **kwargs)

    return ChosenView
