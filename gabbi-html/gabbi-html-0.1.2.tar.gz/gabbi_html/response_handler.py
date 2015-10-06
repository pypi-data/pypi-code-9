from lxml import html
from gabbi.handlers import ResponseHandler

from . import _parse_selector


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
