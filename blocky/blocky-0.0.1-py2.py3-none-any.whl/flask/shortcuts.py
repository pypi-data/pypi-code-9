from flask.views import MethodView

from . import FlaskBlockRenderer


__all__ = ['BlockRenderView', 'render_template']


class BlockRenderView(MethodView):
    """Class view to enable partial rendering."""
    template_name = None  # The template for the view
    default_blocks = {}
    blocks = {}

    def render_template(self, **kwargs):
        """Render the class view template using FlaskBlockRenderer.

        Args:
          kwargs: The context kwargs to pass into the renderer.
        """
        block_list = self.default_blocks.copy()
        block_list.update(self.blocks)

        return FlaskBlockRenderer(
            self.template_name, block_list, **kwargs
        ).render()


def render_template(template_name, block_dict, **kwargs):
    """Render a template using FlaskBlockRenderer.

    Args:
        template_name (str): The name of the template to render.

        block_dict (dict): The blocks to render.

        kwargs: The context kwargs to pass into the renderer.
    """
    return FlaskBlockRenderer(template_name, block_dict, **kwargs).render()
