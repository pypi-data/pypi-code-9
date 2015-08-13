from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from cms.toolbar_pool import toolbar_pool
from cms.toolbar_base import CMSToolbar


@toolbar_pool.register
class ContactToolbar(CMSToolbar):

    def populate(self):
        menu = self.toolbar.get_or_create_menu('contact', _('Contact'))

        # Messages menuitem.
        url = reverse('admin:djangocms_contact_contactmessage_changelist')
        menu.add_modal_item(_('Messages'), url=url)
