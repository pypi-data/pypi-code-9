from docutils.nodes import Text
from docutils.parsers.rst.directives.body import CodeBlock
from okapi.core.exceptions import InvalidHeaderException

from okapi.rst.nodes import headers_block
from okapi.settings import settings
from okapi.core.utils import parse_headers


class HeadersDirective(CodeBlock):
    """
    Extends RST with ``.. code:: headers`` directive.

    Usage::

        .. code:: headers

            Authentication: topsecrettoken
            Accept-Language: en,fr

    """
    template_name = 'headers.html'

    def run(self):
        """
        Parse headers from source.

        :return: List of created nodes
        :rtype: list[headers_block]
        """
        headers = {}
        try:
            headers = parse_headers(self.content)
        except InvalidHeaderException as e:
            settings.log.error(str(e))
            settings.internal.status = False

        settings.headers.visible = headers
        node = headers_block(headers, Text(self.render_headers(headers)))

        return [node]

    def render_headers(self, headers):
        """
        Render headers with template file.

        :param headers: Dictionary with headers.
        :type headers: dict

        :return: Rendered HTML
        :rtype: str
        """
        template = settings.template.env.get_template(self.template_name)
        return template.render(headers=headers)
