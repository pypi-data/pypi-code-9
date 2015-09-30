# -#- coding: utf-8 -#-

from django.db import models
from django.utils.translation import ugettext_lazy as _
from leonardo.module.web.models import Widget
from leonardo_module_links.models import Link

ON_CLICK_CHOICES = (
    ('go_to_page', _('go to linked page')),
    ('open_modal', _('open in modal window')),
    ('open_new_window', _('open new window')),
)


class LinkButtonWidget(Widget):
    link = models.ForeignKey(Link, verbose_name=_(
        "link"), related_name="%(app_label)s_%(class)s_related")
    detail = models.CharField(max_length=255, verbose_name=_(
        "on click action"), choices=ON_CLICK_CHOICES, default='go_to_page')

    class Meta:
        abstract = True
        verbose_name = _("link button")
        verbose_name_plural = _('link buttons')
