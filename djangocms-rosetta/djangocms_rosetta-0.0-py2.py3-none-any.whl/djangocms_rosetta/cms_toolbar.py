from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from cms.toolbar_pool import toolbar_pool
from cms.toolbar_base import CMSToolbar
#from cms.utils.urlutils import admin_reverse


@toolbar_pool.register
class PollToolbar(CMSToolbar):

    def populate(self):
        menu = self.toolbar.get_or_create_menu('rosetta-app', _('Translations'))
        
        for langid, language in settings.LANGUAGES:
            menu.add_link_item(
                language,
                url=reverse('rosetta-language-selection', kwargs={'langid': langid, 'idx':0}),
        )
