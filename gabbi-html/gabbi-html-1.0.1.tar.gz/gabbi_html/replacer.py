import re

from lxml import html
from gabbi.case import HTTPTestCase

from . import _parse_selector


REGEX = re.compile(HTTPTestCase._replacer_regex("RESPONSE_HTML"))


def replace_response_html(self, message):
    """
    replaces a CSS selector with the corresponding value from the previous request
    """

    def _replacer(match):
        selector, attribute = _parse_selector(match.group("arg"))

        doc = html.fromstring(self.prior.output)
        nodes = doc.cssselect(selector)
        node_count = len(nodes)
        if node_count == 0:
            raise ValueError("no matching elements for '%s'" % selector)
        elif node_count > 1:
            raise ValueError("more than one matching element for '%s'" % selector)
        node = nodes[0]

        if attribute:
            try:
                return node.attrib[attribute]
                # TODO: take `<base>` into account for relative URIs
            except KeyError:
                raise ValueError("missing attribute '%s' on element matching '%s'" %
                        (attribute, selector))
        else:
            return node.text

    return REGEX.sub(_replacer, message)
