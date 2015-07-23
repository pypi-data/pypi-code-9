from docutils import nodes
from docutils.writers import html4css1


class HTMLTranslator(html4css1.HTMLTranslator):
    def visit_request_block(self, node):
        self.body.append(node.astext())
        raise nodes.SkipNode

    def visit_headers_block(self, node):
        self.body.append(node.astext())
        raise nodes.SkipNode

    def visit_table(self, node):
        self.context.append(self.compact_p)
        self.compact_p = True
        classes = ' '.join([
            'table', 'table-striped', 'table-hover', self.settings.table_style
        ]).strip()
        self.body.append(
            self.starttag(node, 'table', CLASS=classes))


class HTMLWriter(html4css1.Writer):
    def __init__(self):
        html4css1.Writer.__init__(self)
        self.translator_class = HTMLTranslator
