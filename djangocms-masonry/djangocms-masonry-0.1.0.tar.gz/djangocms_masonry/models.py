# -*- coding: utf-8 -*-

from __future__ import unicode_literals

try:
    import json
except ImportError:
    from django.utils import simplejson as json

from django.db import models
from django.utils.translation import ugettext as _

from cms.models import CMSPlugin
from jsonfield import JSONField

from .conf import settings


class AbstractMasonryBase(CMSPlugin):
    extra_options = JSONField(_('JSON options'), blank=True, default={})

    class Meta:
        abstract = True


class Masonry(AbstractMasonryBase):
    column_width = models.PositiveSmallIntegerField(
        default=80,
        blank=True,
        null=True,
        help_text=_('Aligns items to a horizontal grid.')
    )
    percent_position = models.BooleanField(
        default=False,
        help_text=(
            'Sets item positions in percent values, rather than pixel values.'
            'percentPosition: true works well with percent-width items, as items '
            'will not transition their position on resize.'),
    )
    gutter = models.PositiveSmallIntegerField(
        default=0,
        help_text=_(
            'Adds horizontal space between item elements.'),
    )
    stamp = models.CharField(
        default='',
        blank=True,
        max_length=128,
        help_text=_(
            'Specifies which elements are stamped within the layout.'
            'Isotope will layout items below stamped elements.'),
    )
    is_fit_width = models.BooleanField(
        default=False,
        help_text=_(
            'Sets the width of the container to fit the available number of columns, based '
            'the size of container\'s parent element. When enabled, you can center the '
            'container with CSS.'),
    )
    is_origin_left = models.BooleanField(
        default=True,
        help_text=_(
            'Controls the horizontal flow of the layout. By default, item elements '
            'start positioning at the left, with isOriginLeft: true. Set isOriginLeft: false '
            'for right-to-left layouts.'),
    )
    is_origin_top = models.BooleanField(
        default=True,
        help_text=_(
            'Controls the vertical flow of the layout. By default, item elements start '
            'positioning at the top, with isOriginTop: true. Set isOriginTop: false '
            'for bottom-up layouts. It’s like Tetris!'),
    )

    style = models.CharField(
        _('style'),
        max_length=255,
        choices=settings.DJANGOCMS_MASONRY_STYLES,
        default=settings.DJANGOCMS_MASONRY_STYLES[0][0],
        help_text=_('CSS class'), )
    template = models.CharField(
        _('template'),
        max_length=255,
        choices=settings.DJANGOCMS_MASONRY_TEMPLATES,
        default=settings.DJANGOCMS_MASONRY_TEMPLATES[0][0], )

    def get_style(self):
        if self.style and self.style != settings.DJANGOCMS_MASONRY_DEFAULT:
            return self.style
        return ''

    def get_masonry_options(self):
        options = {
            'itemSelector': settings.DJANGOCMS_MASONRY_ITEM_SELECTOR,
            'columnWidth': self.get_column_width(),
            'gutter': self.gutter,
            'percentPosition': self.percent_position,
            'isFitwidth': self.is_fit_width,
            'isOriginLeft': self.is_origin_left,
            'isOriginTop': self.is_origin_top,


        }

        if self.extra_options:
            options.update(self.extra_options)

        return options

    def get_column_width(self):
        if self.column_width:
            if str(self.column_width).isdigit():
                return int(self.column_width)
            else:
                return self.column_width
            return self.column_width

        return settings.DJANGOCMS_MASONRY_COLUMN_WIDTH_SELECTOR
