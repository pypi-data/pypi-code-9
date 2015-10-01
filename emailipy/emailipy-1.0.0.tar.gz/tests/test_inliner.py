import unittest

from emailipy.inliner import inline_css

class TestInliner(unittest.TestCase):
    def test_noop(self):
        """Verify html remains unchanged with no css passed"""
        html = '<div class="pink">test</div>'
        css = ''
        self.assertEqual(html, inline_css(html, css, pretty_print=False))

    def test_class_rule(self):
        """Verify classes are applied"""
        html = '<div class="pink">test</div>'
        css = '.pink { font-size: 1em; }'
        expected = '<div class="pink" style="font-size: 1em;">test</div>'
        result = inline_css(html, css, pretty_print=False)
        self.assertEqual(expected, result)

    def test_class_no_class(self):
        """Verify classes are applied only where intended"""
        html = '<span><div class="pink">test</div><div>t2</div></span>'
        css = '.pink { font-size: 1em; }'
        expected = '<span><div class="pink" style="font-size: 1em;">test</div><div>t2</div></span>'
        result = inline_css(html, css, pretty_print=False)
        self.assertEqual(expected, result)

    def test_classes_stripped(self):
        """Verify classes are stripped w/ remove_classes flag."""
        html = '<div class="pink">test</div>'
        css = '.pink { font-size: 1em; }'
        expected = '<div style="font-size: 1em;">test</div>'
        result = inline_css(html, css, remove_classes=True, pretty_print=False)
        self.assertEqual(expected, result)

    def test_element_rule(self):
        """Verify element rules are applied"""
        html = '<span><div class="pink">test</div><div>t2</div></span>'
        css = 'div { font-size: 1em; }'
        expected = '<span><div class="pink" style="font-size: 1em;">test</div><div style="font-size: 1em;">t2</div></span>'
        result = inline_css(html, css, pretty_print=False)
        self.assertEqual(expected, result)

    def test_css3_nth_child(self):
        """Check css3 nth-child support"""
        html = '<span><div>test</div><div>t2</div></span>'
        css = 'div:nth-child(2) { font-size: 1em; }'
        expected = '<span><div>test</div><div style="font-size: 1em;">t2</div></span>'
        result = inline_css(html, css, pretty_print=False)
        self.assertEqual(expected, result)

    def test_class_element_specificity(self):
        """Verify class rules override element rules"""
        html = '<span><div class="pink">test</div><div>t2</div></span>'
        css = 'div { font-size: 1em; } .pink { font-size: 2em; }'
        expected = '<span><div class="pink" style="font-size: 2em;">test</div><div style="font-size: 1em;">t2</div></span>'
        result = inline_css(html, css, pretty_print=False)
        self.assertEqual(expected, result)

    def test_important(self):
        """Verify `!important` is respected"""
        html = '<span><div class="pink">test</div><div>t2</div></span>'
        css = 'div { font-size: 1em !important; } .pink { font-size: 2em; }'
        expected = '<span><div class="pink" style="font-size: 1em;">test</div><div style="font-size: 1em;">t2</div></span>'
        result = inline_css(html, css, pretty_print=False)
        self.assertEqual(expected, result)

    def test_inline_styles(self):
        """Check if inline styles win the specificity war"""
        html = '<span><div class="pink" style="font-size: 1em;">test</div><div>t2</div></span>'
        css = 'div { font-size: 3em; } .pink { font-size: 2em; }'
        expected = '<span><div class="pink" style="font-size: 1em;">test</div><div style="font-size: 3em;">t2</div></span>'
        result = inline_css(html, css, pretty_print=False)
        self.assertEqual(expected, result)

    def test_invalid_rule(self):
        """Verify email styles are stripped"""
        html = '<div class="pink">test</div>'
        css = '.pink { opacity: 0.8; }'
        expected = '<div class="pink">test</div>'
        result = inline_css(html, css, pretty_print=False)
        self.assertEqual(expected, result)

    def test_invalid_rule_not_stripped(self):
        """Make sure we can turn off unsupported css stripping"""
        html = '<div class="pink">test</div>'
        css = '.pink { opacity: 0.8; }'
        expected = '<div class="pink" style="opacity: 0.8;">test</div>'
        result = inline_css(html, css, strip_unsupported_css=False, pretty_print=False)
        self.assertEqual(expected, result)

    def test_id_rule(self):
        """Verify classes are applied"""
        html = '<div id="pink">test</div>'
        css = '#pink { font-size: 1em; }'
        expected = '<div id="pink" style="font-size: 1em;">test</div>'
        result = inline_css(html, css, pretty_print=False)
        self.assertEqual(expected, result)

    def test_wildcard_rule(self):
        """Verify element rules are applied"""
        html = '<span><div class="pink">test</div><div>t2</div></span>'
        css = 'span * { font-size: 1em; }'
        expected = '<span><div class="pink" style="font-size: 1em;">test</div><div style="font-size: 1em;">t2</div></span>'
        result = inline_css(html, css, pretty_print=False)
        self.assertEqual(expected, result)

    def test_child_rule(self):
        """Verify element rules are applied"""
        html = '<span><div class="pink">test</div><div>t2</div></span>'
        css = 'span > div { font-size: 1em; }'
        expected = '<span><div class="pink" style="font-size: 1em;">test</div><div style="font-size: 1em;">t2</div></span>'
        result = inline_css(html, css, pretty_print=False)
        self.assertEqual(expected, result)

    def test_sibling_rule(self):
        """Verify element rules are applied"""
        html = '<span><div class="pink">test</div><div>t2</div></span>'
        css = 'span > div.pink ~ * { font-size: 1em; }'
        expected = '<span><div class="pink">test</div><div style="font-size: 1em;">t2</div></span>'
        result = inline_css(html, css, pretty_print=False)
        self.assertEqual(expected, result)
