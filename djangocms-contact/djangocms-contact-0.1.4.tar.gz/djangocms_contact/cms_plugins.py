from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cms.models.pluginmodel import CMSPlugin

from djangocms_contact.forms import ContactForm


class ContactFormPlugin(CMSPluginBase):
    """This plugin allows users to add a contact form on any page."""

    name = _('Contact form')
    model = CMSPlugin
    render_template = 'djangocms_contact/plugins/contact_form.html'

    def render(self, context, instance, placeholder):
        context['contact_form'] = ContactForm()
        return context

plugin_pool.register_plugin(ContactFormPlugin)
