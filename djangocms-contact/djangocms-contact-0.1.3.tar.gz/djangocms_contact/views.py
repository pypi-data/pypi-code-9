from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse, resolve
from django.views.generic import View

from djangocms_contact.forms import ContactForm


class ContactView(View):
    """
    View for the contact page.

    Note: current_app is required for apphooks because Django does not allow an
    other way of doing this.
    See <http://docs.django-cms.org/en/3.1.2/how_to/apphooks.html> for more
    details.
    """

    form_class = ContactForm
    template_name = 'djangocms_contact/contact.html'

    def get(self, request):
        """Show a contact page with a form."""
        current_app = resolve(request.path_info).namespace
        form = self.form_class()
        context = RequestContext(request, {'contact_form': form},
                                 current_app=current_app)
        return render(request, self.template_name, context_instance=context)

    def post(self, request):
        """
        Save mensaje and redirect to success page if the form is valid, or
        show the form and errors if invalid.
        """
        current_app = resolve(request.path_info).namespace
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('djangocms_contact:success',
                                                current_app=current_app))

        context = RequestContext(request, {'contact_form': form},
                                 current_app=current_app)
        return render(request, self.template_name, context_instance=context,
                      status=400)
