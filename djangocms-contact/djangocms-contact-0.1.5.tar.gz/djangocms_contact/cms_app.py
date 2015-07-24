from django.utils.translation import ugettext_lazy as _

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool


class ContactApp(CMSApp):
    name = _('Contact')
    urls = ['djangocms_contact.urls']
    app_name = 'djangocms_contact'

apphook_pool.register(ContactApp)
