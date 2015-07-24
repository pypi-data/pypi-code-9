try:
    import json
except ImportError:
    from django.utils import simplejson as json  # noqa

import django
from django.template.loader import select_template
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .conf import settings
from .models import Masonry


class MasonryPlugin(CMSPluginBase):
    name = _('Masonry')
    model = Masonry
    allow_children = True
    render_template = 'djangocms_masonry/default.html'
    child_classes = settings.DJANGOCMS_MASONRY_CHILD_CLASSES
    fieldsets = (
        (None, {
            'fields': (
                'column_width',
                'percent_position',
                'gutter',
                'stamp',
                'is_fit_width',
                'is_origin_left',
                'is_origin_top',
            )
        }),
        (_('Style'), {
            'fields': (
                'style',
                'template',
            ),
        }),
        (_('Extra'), {
            'classes': ('collapse', ),
            'fields': (
                'extra_options',
            ),
        }),
    )
    TEMPLATE_PATH = 'djangocms_masonry/%s.html'
    render_template = TEMPLATE_PATH % 'default'

    def render(self, context, instance, placeholder):
        template = select_template((
            self.TEMPLATE_PATH % instance.template,
            self.TEMPLATE_PATH % 'default')
        )

        if django.VERSION[1] >= 8:
            self.render_template = template.template
        else:
            self.render_template = template

        context = super(MasonryPlugin, self).render(context, instance, placeholder)
        context.update({
            'INCLUDE_JS_MASONRY': settings.DJANGOCMS_MASONRY_INCLUDE_JS_MASONRY,
            'style': instance.get_style(),
            'options': mark_safe(json.dumps(instance.get_masonry_options())),
        })

        return context


plugin_pool.register_plugin(MasonryPlugin)
