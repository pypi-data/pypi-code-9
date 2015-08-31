"""
Contains application CRUD view definitions.
"""
from django.http import Http404

from wagtailplus.utils.views import crud

from ..forms import EmailLinkForm
from ..forms import ExternalLinkForm
from ..models import Link


class CreateView(crud.CreateView):
    """
    CRUD create link view.
    """
    def get(self, request, *args, **kwargs):
        """
        Returns GET response.

        :param request: the request instance.
        :rtype: django.http.HttpResponse.
        """
        return self.render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        """
        Returns context dictionary for view.

        :rtype: dict.
        """
        kwargs.update({
            'view':             self,
            'email_form':       EmailLinkForm(),
            'external_form':    ExternalLinkForm(),
            'type_email':       Link.LINK_TYPE_EMAIL,
            'type_external':    Link.LINK_TYPE_EXTERNAL,
        })

        # If a form has been submitted, update context with
        # the submitted form value.
        if 'form' in kwargs:
            submitted_form = kwargs.pop('form')
            if isinstance(submitted_form, EmailLinkForm):
                kwargs.update({'email_form': submitted_form})
            elif isinstance(submitted_form, ExternalLinkForm):
                kwargs.update({'external_form': submitted_form})

        return kwargs

    def get_form_class(self):
        """
        Override because this view actually uses two form classes.
        """
        return None

    def post(self, request, *args, **kwargs):
        """
        Returns POST response.

        :param request: the request instance.
        :rtype: django.http.HttpResponse.
        """
        form        = None
        link_type   = int(request.POST.get('link_type', 0))

        if link_type == Link.LINK_TYPE_EMAIL:
            form = EmailLinkForm(**self.get_form_kwargs())
        elif link_type == Link.LINK_TYPE_EXTERNAL:
            form = ExternalLinkForm(**self.get_form_kwargs())

        if form:
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        else:
            raise Http404()

class UpdateView(crud.UpdateView):
    """
    CRUD update link view.
    """
    def get_form_class(self):
        """
        Returns form class to use in the view.

        :rtype: django.forms.ModelForm.
        """
        if self.object.link_type == Link.LINK_TYPE_EMAIL:
            return EmailLinkForm
        elif self.object.link_type == Link.LINK_TYPE_EXTERNAL:
            return ExternalLinkForm

        return None
