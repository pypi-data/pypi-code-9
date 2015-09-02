# -*- coding: utf-8 -*-

from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase

from .models import VideoPluginModel


class VideoEmbedPlugin(CMSPluginBase):

        model = VideoPluginModel
        name = ("Embedded Video")
        render_template = "cmsplugin_oembed/_video.html"

        def render(self, context, instance, placeholder):
            video = instance.video_url
            name = instance.name
            context.update({
                'name': name,
                'item': video,
            })

            return context

plugin_pool.register_plugin(VideoEmbedPlugin)
