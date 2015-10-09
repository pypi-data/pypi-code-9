__author__ = 'vinay'

from django.test import TestCase

from .utils import parse_cms_template, NAMESPACE_DELIMITER


class CMSTests(TestCase):
    def test_basic_features(self):
        html = """
            <html>
                <head>
                </head>
                <body>
                    <h1 data-cms-content="h1" data-cms-attr="id:id" id="orig">hello</h1>
                </body>
            </html>
        """
        out = parse_cms_template(html, {})
        self.assertHTMLEqual(html, out)

        out = parse_cms_template(html, {"h1": "foo"})
        self.assertHTMLEqual(
            out, """
                <html>
                    <head>
                    </head>
                    <body>
                        <h1 data-cms-content="h1" data-cms-attr="id:id" id="orig">foo</h1>
                    </body>
                </html>
            """
        )

        self.assertHTMLEqual(
            parse_cms_template(html, {"id": "new_id"}),
            """
                <html>
                    <head>
                    </head>
                    <body>
                        <h1 data-cms-content="h1" data-cms-attr="id:id" id="new_id">hello</h1>
                    </body>
                </html>
            """
        )

    def test_advanced_features(self):
        html = """
            <html>
                <head>
                </head>
                <body>
                    <h1 data-cms-content="h1" data-cms-attr="id:id" id="orig">hello</h1>
                </body>
            </html>
        """
        out = parse_cms_template(
            html,
            {'h1': '<div data-cms-content="text"></div>'}
        )
        self.assertHTMLEqual(out, """
            <html>
                <head>
                </head>
                <body>
                    <h1 data-cms-content="h1" data-cms-attr="id:id" id="orig">
                    <div data-cms-content="text"></div>
                    </h1>
                </body>
            </html>
        """)

        out = parse_cms_template(
            html,
            {'h1': '<div data-cms-content="text"></div>',
             'h1' + NAMESPACE_DELIMITER + 'text': 'replaced'}
        )
        self.assertHTMLEqual(out, """
            <html>
                <head>
                </head>
                <body>
                    <h1 data-cms-content="h1" data-cms-attr="id:id" id="orig">
                    <div data-cms-content="text">replaced</div>
                    </h1>
                </body>
            </html>
        """)

        out = parse_cms_template(
            html,
            {'h1': '<div data-cms-attr="id:div_id" id="default">hi</div>',
             'h1' + NAMESPACE_DELIMITER + 'div_id': 'replaced'}
        )
        self.assertHTMLEqual(out, """
            <html>
                <head>
                </head>
                <body>
                    <h1 data-cms-content="h1" data-cms-attr="id:id" id="orig">
                    <div data-cms-attr="id:div_id" id="replaced">hi</div>
                    </h1>
                </body>
            </html>
        """)

        out = parse_cms_template(
            html,
            {'h1': '<div data-cms-content="content" data-cms-attr="id:div_id" id="default">hi</div>',
             'h1' + NAMESPACE_DELIMITER + 'div_id': 'replaced',
             'h1' + NAMESPACE_DELIMITER + 'content': 'new content'}
        )
        self.assertHTMLEqual(out, """
            <html>
                <head>
                </head>
                <body>
                    <h1 data-cms-content="h1" data-cms-attr="id:id" id="orig">
                    <div data-cms-content="content" data-cms-attr="id:div_id" id="replaced">new content</div>
                    </h1>
                </body>
            </html>
        """)

    def test_snippet_insertions(self):
        html = """
            <html>
                <head>
                </head>
                <body>
                    <h1 data-cms-content="h1" data-cms-attr="id:id" id="orig">hello</h1>
                </body>
            </html>
        """
        out = parse_cms_template(
            html,
            {'h1': '<div data-cms-include="namespace:cms_templates/snippet"></div>'}
        )
        self.assertHTMLEqual(out, """
            <html>
                <head>
                </head>
                <body>
                    <h1 data-cms-content="h1" data-cms-attr="id:id" id="orig">
                    <div data-cms-include="cms_templates/snippet" data-cms-namespace="namespace">
                    hehehe
                    <div data-cms-content="md:text">Hi</div>
                    </div>
                    </h1>
                </body>
            </html>
        """)

        out = parse_cms_template(
            html,
            {'h1': '<div data-cms-include="namespace:cms_templates/snippet"></div>',
             NAMESPACE_DELIMITER.join(('h1', 'namespace', 'text')): '##Heading##'}
        )
        self.assertHTMLEqual(out, """
            <html>
                <head>
                </head>
                <body>
                    <h1 data-cms-content="h1" data-cms-attr="id:id" id="orig">
                    <div data-cms-include="cms_templates/snippet" data-cms-namespace="namespace">
                    hehehe
                    <div data-cms-content="md:text"><h2>Heading</h2></div>
                    </div>
                    </h1>
                </body>
            </html>
        """)

        out = parse_cms_template(
            html,
            {'h1': '<div data-cms-include="namespace:cms_templates/snippet_2"></div>',
             NAMESPACE_DELIMITER.join(('h1', 'namespace', 'text2')): '##Heading##'}
        )
        self.assertHTMLEqual(out, """
            <html>
                <head>
                </head>
                <body>
                    <h1 data-cms-content="h1" data-cms-attr="id:id" id="orig">
                    <div data-cms-include="cms_templates/snippet_2" data-cms-namespace="namespace">
                    hehehe2
                    <div data-cms-content="md:text2"><h2>Heading</h2></div>
                    </div>
                    </h1>
                </body>
            </html>
        """)
