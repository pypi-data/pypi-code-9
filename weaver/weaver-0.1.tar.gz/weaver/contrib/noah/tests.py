import io
import unittest
from weaver.contrib.noah import utils

class TestNoah(unittest.TestCase) :
 def setUp(self):
     pass

 def tearDown(self):
    pass

 def test_bond(self):
     self.assertTrue(True)

class TestNoahUtils(unittest.TestCase):

    # --- Helpers
    def to_io(self, text):
        return io.StringIO(initial_value=unicode(text))

    # --- Tests
    def test_split_frontmatter_and_body_true(self):
        frontmatter = "---\nfoo\n---\n"
        fh = io.StringIO(initial_value=unicode(frontmatter))
        self.assertEqual(("foo\n", ""), utils.split_frontmatter_and_body(fh))

    def test_split_frontmatter_and_body_with_text(self):
        frontmatter = "---\nfoo\n---\nbar\n"
        fh = io.StringIO(initial_value=unicode(frontmatter))
        self.assertEqual(("foo\n", "bar\n"), utils.split_frontmatter_and_body(fh))

    def test_split_frontmatter_and_body_false_no_closing_dashes(self):
        not_frontmatter = "---\nfoo\nbarn"
        fh = io.StringIO(initial_value=unicode(not_frontmatter))
        self.assertEqual(("", not_frontmatter),utils.split_frontmatter_and_body(fh))

    def test_get_all_links(self):
        text = "[[foo]]"
        fh = self.to_io(text)
        self.assertEqual(["foo"], utils.get_all_links(fh))

    def test_get_all_links_w_multiple_links(self):
        text = "[[foo]] [[bar]]"
        fh = self.to_io(text)
        self.assertEqual(["foo", "bar"], utils.get_all_links(fh))

    def test_get_all_links_w_multiple_links_and_newline(self):
        text = "[[foo]] [[bar]]\n[[baz]]"
        fh = self.to_io(text)
        self.assertEqual(["foo", "bar", "baz"], utils.get_all_links(fh))




if __name__ == '__main__':
    unittest.main()
