from django.db import models
from parler.models import TranslatableModel, TranslatedFields
from django.utils.encoding import python_2_unicode_compatible
from cms.models import CMSPlugin

from cms.models.fields import PageField
from djangocms_text_ckeditor.fields import HTMLField
from filer.fields.image import FilerImageField

from .settings import STYLES


@python_2_unicode_compatible
class CallToActionRepository(TranslatableModel):
    code = models.CharField(max_length=50)
    style = models.CharField(
        max_length=200,
        choices=STYLES, default=STYLES[0][0])

    translations = TranslatedFields(
        content = HTMLField(blank=True),

        link_text = models.CharField(max_length=100, blank=True),
        link_custom = models.CharField(max_length=400, blank=True)
    )

    image = FilerImageField(null=True, blank=True)
    link_to_page = PageField(null=True, blank=True)

    class Meta:
        db_table = 'calltoaction_repository'
        verbose_name = 'Call to Action'
        verbose_name_plural = 'Call to Action Repository'

    def __str__(self):
        return self.code

    def get_absolute_url(self):
        if self.link_custom:
            return self.link_custom
        elif self.link_to_page:
            return self.link_to_page.get_absolute_url()
        else:
            return ''

    def rendered(self):
        from django.template.loader import get_template, Context
        return get_template(self.style).render(Context({'call_to_action': self}))


@python_2_unicode_compatible
class CallToAction(CMSPlugin):
    call_to_action = models.ForeignKey(CallToActionRepository)

    class Meta:
        db_table = 'calltoaction_plugins'

    def __str__(self):
        return self.call_to_action.code
