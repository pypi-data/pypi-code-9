import re

import gabbi.case

from lxml import html
from gabbi.handlers import ResponseHandler


REGEX = re.compile(gabbi.case.HTTPTestCase._replacer_regex("RESPONSE_HTML"))


def gabbi_response_handlers():
    return [HTMLResponseHandler]


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


# monkey-patch gabbi to include custom replacer
gabbi.case.REPLACERS += ["RESPONSE_HTML"]
gabbi.case.HTTPTestCase._response_html_replace = replace_response_html


class HTMLResponseHandler(ResponseHandler):

    test_key_suffix = "html"
    test_key_value = {}

    def preprocess(self, test):
        self.doc = html.fromstring(test.output)

    def action(self, test, item, value):
        try: # count
            count = int(value)
        except ValueError: # content
            count = None

        selector, attribute = _parse_selector(item)
        nodes = self.doc.cssselect(selector)
        node_count = len(nodes)
        if count:
            test.assertEqual(node_count, count,
                    "expected %d matching elements, found %d" % (count, node_count))
            if attribute: # XXX: this is the same as using an attribute selector!?
                for i, node in enumerate(nodes):
                    test.assertTrue(attribute in node.attrib,
                            "missing attribute '%s' on element #%d" %
                                    (attribute, i + 1))
        else:
            test.assertEqual(node_count, 1,
                    "content checks must not target more than a single element")
            node = nodes[0]
            if attribute:
                actual = node.attrib[attribute]
                test.assertEqual(actual, value,
                        "unexpected value for attribute '%s'" % attribute)
            else:
                actual = node.text.strip()
                test.assertEqual(actual, value, "unexpected text value")


def _parse_selector(selector):
    """
    extracts attribute name from selector, if any

    attributes are appended with `@<name>` (e.g. `a@href`)
    """
    attribute = None
    if "@" in selector:
        selector, attribute = selector.rsplit("@", 1)
    return selector, attribute
