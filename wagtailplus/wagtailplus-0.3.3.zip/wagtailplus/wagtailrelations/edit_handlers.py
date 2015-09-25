"""
Contains application edit handlers.
"""
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from wagtail.wagtailadmin.edit_handlers import EditHandler


class BaseRelatedPanel(EditHandler):
    template = 'wagtailrelations/edit_handlers/related.html'

    def __init__(self, instance=None, form=None):
        super(BaseRelatedPanel, self).__init__(instance, form)
        self.instance = instance

    def render(self):
        context = {'self': self}

        return mark_safe(
            render_to_string(self.template, context)
        )

class RelatedPanel(object):
    @staticmethod
    def bind_to_model(model):
        base = {'model': model}
        return type(str('_RelatedPanel'), (BaseRelatedPanel,), base)
