import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template import engines

from ..base import BlockRenderer


__all__ = ['DjangoBlockRenderer']


class DjangoBlockRenderer(BlockRenderer):
    def __init__(self, request, template_name, blocks, context=None):
        """Prepare the renderer.

        Args:
            request (django.http.HttpRequest): The request object.

            template_name (str): The name of the template to render.

            blocks (dict): The dict of blocks to render.

            context (dict): The context to pass into the renderer.
        """
        self.template_name = template_name
        self.blocks = blocks
        self.context = context

        self.request = request

        self.engine = engines['jinja2']
        self.jinja_env = self.engine.env

        self.template = self.get_template(self.template_name)

    def is_xhr(self):
        return self.request.is_ajax()

    def get_template_blocks(self, template):
        return template.template.blocks

    def new_context(self, template):
        return template.template.new_context(self.context)

    def get_template(self, template_name):
        return self.engine.get_template(template_name)

    def build_response(self, block_funcs):
        return JsonResponse(self.build_json(block_funcs))

    def render_template(self):
        return HttpResponse(
            self.template.render(context=self.context, request=self.request)
        )
