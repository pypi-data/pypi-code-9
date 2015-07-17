from jinja2 import nodes


__all__ = ['BlockDoesNotExist', 'BlockRenderer']


class BlockDoesNotExist(Exception):
    """Used in our renderer to handle when a block is missing"""
    pass


class BlockRenderer(object):
    """Our base class from which all others extend from."""

    def __init__(self):
        raise NotImplementedError

    def is_xhr(self):
        """Return if the request was performed via xhr.

        Returns:
            bool: True if request was performed via xhr. False otherwise.
        """
        raise NotImplementedError

    def get_template(self, template_name):
        """Return a template object.

        Args:
            template_name (str): The name of the template to get.
        """
        raise NotImplementedError

    def get_path(self):
        """Return the path of the request.

        Returns:
            str: The path of the request.
        """
        return self.request.path

    def get_block_iter(self, blocks):
        """Returns an iterable version of a dict.

        Note:
            Python 3 does not have iteritems() and instead uses items().
        """
        try:
            return blocks.iteritems()
        except AttributeError:
            return blocks.items()

    def build_json(self, block_funcs):
        """Build the json for the blocks.

        Args:
            block_funcs (dict): The block names and their function.

        Returns:
            dict: The list of blocks and the path of the request.
        """
        response = list()

        items = list()

        for name, selector in self.get_block_iter(self.blocks):
            try:
                response.append({
                    'name': name,
                    'selector': selector,
                    'content': ''.join(block_funcs[name](self.context))
                })
            except KeyError:
                raise BlockDoesNotExist(
                    "Block {0} could not be found.".format(name)
                )

        return {
            'blocks': response,
            'url': self.get_path()
        }

    def build_response(self, block_funcs):
        """Return the json response.

        Args:
            block_funcs (dict): The block names and their function.
        """
        raise NotImplementedError

    def get_template_blocks(self, template):
        """Return the list of block functions for a template.

        Args:
            template: The template to load the block list from.

        Returns:
            list: The list of blocks and their function.
        """
        raise NotImplementedError

    def new_context(self, template):
        """Return a new context for a template.

        Args:
            template: The template to load the block list from.
        """
        raise NotImplementedError

    def render_blocks(self):
        """Build the bocks and return the response."""
        source = self.jinja_env.loader.get_source(
            self.jinja_env, self.template_name
        )[0]
        parsed = self.jinja_env.parse(source)

        blocks = dict()
        new_context = None
        extend_node = parsed.find(nodes.Extends)

        if extend_node:
            extend_template = self.get_template(extend_node.template.value)
            blocks = self.get_template_blocks(extend_template)
            new_context = self.new_context(extend_template)
        else:
            new_context = self.new_context(self.template)

        for name, func in self.get_block_iter(self.get_template_blocks(
            self.template)):
            blocks[name] = func

        return self.build_response(blocks)

    def render_template(self):
        """Render the template when not called via xhr."""
        raise NotImplementedError

    def render(self):
        """Render the block list or the full template."""
        if self.is_xhr():
            return self.render_blocks()
        else:
            return self.render_template()
