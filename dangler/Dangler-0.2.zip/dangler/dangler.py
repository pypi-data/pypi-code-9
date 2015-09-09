r"""
Dangler v0.2
>>> get_trailing_spaces("dad\n   ")
3
>>> get_trailing_spaces("dad\n \n   ")
3
>>> get_leading_spaces("\n   dad")
3
>>> get_leading_spaces("  \n   dad")
3
>>> undangle("<html>\n<body>")
'\n<html><body></body></html>'
>>> undangle("<html>\n<body>\n <div>")
'\n<html><body><div></div></body></html>'
>>> undangle("<html>\n<body>\n  <div>\n     div content")
'\n<html><body><div>\n\n     div content</div></body></html>'
>>> undangle("<html>\n<body>\n  <div>\n     div content\n div content line 2")
'\n<html><body><div>\n\n     div content\n div content line 2</div></body></html>'
>>> undangle("<html>\n<body>\n  <div>\n    <div>\n     div content\n div content line 2")
'\n<html><body><div><div>\n\n     div content\n div content line 2</div></div></body></html>'
>>> undangle("<html>\n<body>\n  <div>\n     <div>\n  div content\n div content line 2")
'\n<html><body><div><div></div></div>\n\n  div content\n div content line 2</body></html>'
>>> undangle("<html>\n<body>\n  <div>\n     <div>\n   div content\n div content line 2")
'\n<html><body><div><div></div>\n\n   div content\n div content line 2</div></body></html>'
>>> undangle('<html>\n<body>\n    <div>\n        div content\n        <span>\n            span content\n\n        more div content\n')
'\n<html><body><div>\n\n        div content\n        <span>\n\n            span content</span>\n        more div content\n</div></body></html>'
"""

from html.parser import HTMLParser
from bs4 import BeautifulSoup
import argparse
import re

TRAILING_SPACE_REGEX = re.compile("\n( *)$")
LEADING_SPACE_REGEX = re.compile('\n( *)\S')

def test_helper(string):
    return re.sub("\n|( ( +))", "", string)

def get_trailing_spaces(string):
    """get trailing spaces after a new line"""
    m = TRAILING_SPACE_REGEX.search(string)
    if m is not None:
        return len(m.group(1))
    else:
        return None

def get_leading_spaces(string):
    """get leading spaces after a new line"""
    m = LEADING_SPACE_REGEX.search(string)
    if m is not None:
        return len(m.group(1))
    else:
        return None

class Node:
    def __init__(self, html_parser_data, indent):
        if indent is None:
            raise Exception("Cannot detect indent for %s" % repr(str(html_parser_data)))
        self._html_parser_data = html_parser_data
        self._indent = indent
        self._children = []
        self._parent = None

    def __str__(self):
        return self._html_parser_data

    def addChild(self, child):
        if child._indent > self._indent:
            child._parent = self
            self._children.append(child)
            if isinstance(child, Tag):
                return child
            else:
                return self
        else:
            if self._parent:
                return self._parent.addChild(child)
            else:
                self._children.append(child)
                return child

class Tag(Node):
    def _getOpen(self):
        tag_name, attributes = self._html_parser_data
        if attributes:
            attr_list = ' ' + ' '.join(['%s="%s"' % t for t in attributes])
        else:
            attr_list = ''
        return '<%s%s>' % (tag_name, attr_list)

    def _getClose(self):
        tag_name, _ = self._html_parser_data
        return '</%s>' % (tag_name)

    def __str__(self):
        return "%s%s%s" % (self._getOpen(),
                           ''.join([str(child) for child in self._children]),
                           self._getClose())

class StartEndTag(Node):
    def __str__(self):
        tag_name, attributes = self._html_parser_data
        if attributes:
            attr_list = ' ' + ' '.join(['%s="%s"' % t for t in attributes])
        else:
            attr_list = ''
        return "<%s%s/>" % (tag_name, attr_list)

class Data(Node):
    def addChild(self, child):
        if child._indent > self._indent:
            raise Exception("Trying to add children for a Data node!")
        else:
            if self._parent:
                self._parent.addChild(child)
            else:
                print(repr(self._html_parser_data), child._html_parser_data)
                raise Exception("Don't have parent to add data node to")

class Dangler(HTMLParser):
    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self._current_indent = 0
        self._current_tag = None
        self._root = None
        self._declaration = ""

    def _add_node_to_tree(self, node):
        if self._current_tag:
            self._current_tag = self._current_tag.addChild(node)
        else:
            self._current_tag = node
            self._root = node
        self._current_indent = None

    def handle_starttag(self, tag, attributes):
        self._add_node_to_tree(Tag((tag, attributes), self._current_indent))

    def handle_endtag(self, tag):
        raise Exception("End tag found at %s" % tag)

    def handle_startendtag(self, tag, attributes):
        self._add_node_to_tree(StartEndTag((tag, attributes), self._current_indent))

    def handle_data(self, data):
        # data is split at two newlines with only whitespace characters
        # between them. Then indention of each piece is found out separately
        # an added to the tree separately. This enables text content to be added
        # to a higher level tag. For example, imagine this html content
        # <div>
        #   content for div <span>Span content</span> div content continued
        # 
        # Without this code, the above html will not be able to be represented.
        #
        # <div>
        #    content for div
        #    <span>
        #        Span Content
        #    div content continued
        #
        # The above code will not work, because the last line, 'div content continued'
        # will get added under the span itself.
        # with this code, you can represent it as shown below
        # <div>
        #    content for div
        #    <span>
        #        Span Content
        #
        #    div content continued
        # By using two line breaks in a row, the indentation is recalculated for the
        # last line, and will be correctly added to the parent div, instead of the span
        for data_slug in ['\n'+s  for s in re.split("\n *\n", data)]:
            if not data_slug.isspace():
                self._add_node_to_tree(Data(data_slug, get_leading_spaces(data_slug)))
        self._current_indent = get_trailing_spaces(data)

    def handle_decl(self, decl):
        self._declaration = "<!%s>" % decl

    def handle_entityref(self, name):
        self._add_node_to_tree(Data("&%s;" % name, self._current_indent))

class TagFixer:
    ''' A hack to work around the fact that html parser treats script and style
        tags as special cases and will not trigger a start_tag event if a closing
        tag is not found. So this class converts script tags to something else and
        converts it back after undangling'''
    def __init__(self):
        self._last_suffix = 0
        self._replace_slugs = {}

    def fixTags(self, src):
        # cache for previously resolved replace strings.
        # when a certain element is to be replaced, a string that is not
        # found elsewhere in the document is calculated by appending a integer
        # suffix and incrementing it until it is unique. This cache is to
        # prevent re-computation of this suffix for previously seen tags
        replace_source = {}
        def get_replacement(match):
            slug = match.group(0)
            if slug in replace_source:
                return replace_source[slug]
            else:
                while True:
                    suffixed = "%s-%s" % ('replaced', self._last_suffix) 
                    if suffixed in src:
                        self._last_suffix += 1
                    else:
                        self._last_suffix += 1
                        break
                replace_source[slug] = suffixed
                # mapping between replaced strings and original strings
                # so that we can restore them after undangling
                self._replace_slugs[suffixed] = slug
                return suffixed
        ret = re.sub("script", get_replacement, src, count=0, flags=re.M|re.I)
        return re.sub("style", get_replacement, ret, count=0, flags=re.M|re.I)

    def unfixTags(self, src):
        for look_for, replace in self._replace_slugs.items():
            src = src.replace(look_for, replace)
        return src

def undangle(src):
    dangler = Dangler(strict=False, convert_charrefs=False)
    dangler.feed(src)
    undangled = dangler._declaration + '\n' +  str(dangler._root)
    return undangled

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()
    with open(args.filename, 'r') as ifile:
        tag_fixer = TagFixer()
        src = ifile.read()
        src = tag_fixer.fixTags(src)
        undangled = undangle(src)
        undangled = tag_fixer.unfixTags(undangled)
        soup = BeautifulSoup(undangled, "html5lib")
        print(soup.prettify(formatter="html"))

if __name__ == "__main__":
    import doctest
    doctest.testmod()
