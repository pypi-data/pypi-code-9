from django.views.generic.base import TemplateView

from . import DjangoBlockRenderer


__all__ = ['BlockRenderView', 'render_template']


class BlockRenderView(TemplateView):
    """Class view to enable partial rendering."""
    default_blocks = {}
    blocks = {}

    def get_block_list(self):
        """Get the dict of blocks.

        Returns:
            dict: The compiled dict of blocks to render.
        """
        block_dict = self.default_blocks.copy()
        block_dict.update(self.blocks)
        return block_dict

    def get(self, request, *args, **kwargs):
        """Render the class template using DjangoBlockRenderer.

        Args:
            request (django.http.httpRequest): The request object.

            *args: Variable length argument list.

            **kwargs: The context to pass through to the renderer.
        """
        context = self.get_context_data(**kwargs)
        return DjangoBlockRenderer(
            request, self.template_name, self.get_block_list(), context
        ).render()


def render_template(request, template_name, block_dict, context=None):
    """Render a template using DjangoBlockRenderer.

    Args:
        request (django.http.HttpRequest): The request object.

        template_name (str): The name of the template to render.

        block_dict (dict): The blocks to render.

        context (dict): The context to pass into the renderer.
    """
    return DjangoBlockRenderer(
        request, template_name, block_dict, context=context
    ).render()
