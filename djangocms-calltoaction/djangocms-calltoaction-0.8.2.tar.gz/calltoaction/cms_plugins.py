from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import CallToAction
from .settings import STYLES


class CallToActionPlugin(CMSPluginBase):
    model = CallToAction
    module = "Call to Action"
    name = "Call to Action"

    def get_render_template(self, context, instance, placeholder):
        return instance.call_to_action.style

    def render(self, context, instance, placeholder):
        context.update({
            'instance': instance, 'placeholder': placeholder,
            'call_to_action': instance.call_to_action
        })
        return context

plugin_pool.register_plugin(CallToActionPlugin)
