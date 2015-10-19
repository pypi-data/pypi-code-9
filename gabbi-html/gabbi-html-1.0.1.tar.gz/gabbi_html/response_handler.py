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
        if count is not None:
            test.assertEqual(node_count, count,
                    "expected %d elements matching '%s', found %d" % (count,
                            selector, node_count))
            if attribute: # XXX: this is the same as using an attribute selector!?
                for i, node in enumerate(nodes):
                    test.assertTrue(attribute in node.attrib,
                            "missing attribute '%s' on element #%d matching '%s'" %
                                    (attribute, i + 1, selector))
        else:
            test.assertNotEqual(node_count, 0, "no element matching '%s'" % selector)
            test.assertEqual(node_count, 1,
                    "'%s' content check must not target more than a single element" %
                            selector)
            node = nodes[0]
            if attribute:
                actual = node.attrib[attribute]
                test.assertEqual(actual, value,
                        "unexpected value for attribute '%s' on element matching '%s'" %
                                (attribute, selector))
            else:
                actual = node.text.strip()
                test.assertEqual(actual, value, "unexpected text value")
