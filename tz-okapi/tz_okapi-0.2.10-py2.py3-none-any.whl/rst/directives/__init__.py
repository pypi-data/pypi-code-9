from docutils.parsers.rst import directives
from docutils.parsers.rst.directives import body

from okapi.rst.directives.headers import HeadersDirective
from okapi.rst.directives.request import RequestDirective


def load_directives():
    """
    Loads custom directives to docutils register. It has to be called before
    start of rendering.
    """
    directives.register_directive('code', CodeBlock)


class CodeBlock(body.CodeBlock):
    """
    Custom directive which extends ``.. code::``.
    """

    directives = {
        'headers': HeadersDirective,
        'request': RequestDirective
    }

    @property
    def type(self):
        """
        Returns type of code directive (``headers``, ``request``, etc.)

        :return: type of directive
        :rtype: str
        """
        try:
            return self.arguments[0]
        except IndexError:
            pass

    def run(self):
        if not self.type or self.type not in self.directives:
            return super(CodeBlock, self).run()

        directive_cls = self.directives[self.type]

        inst = directive_cls(self.name, self.arguments, self.options,
                             self.content, self.lineno, self.content_offset,
                             self.block_text, self.state,
                             self.state_machine)
        return inst.run()
