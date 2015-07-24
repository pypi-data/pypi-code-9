# -*- coding: utf-8 -*-

from django.conf import settings  # noqa
from django.utils.translation import ugettext_lazy as _

from appconf import AppConf


class MasonryConf(AppConf):
    DEFAULT = 'default'

    CHILD_CLASSES = ()

    STYLES = (
        (DEFAULT, _('Default')),
    )

    TEMPLATES = (
        (DEFAULT, _('Default')),
    )

    INCLUDE_JS_MASONRY = True

    ITEM_SELECTOR = '.grid-item'

    COLUMN_WIDTH_SELECTOR = '.grid-sizer'

    GUTTER_SELECTOR = '.gutter-sizer'

    class Meta:
        prefix = 'djangocms_masonry'
