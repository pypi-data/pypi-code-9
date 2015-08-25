from setuptools import setup

version = '1.6.1'
name = 'pyHTMLParser'
short_description = 'A simple html parser that constructs DOM tree.'
long_description = """\
It is aimed to provide jquery like API.

Example
-------

.. code-block:: python

    from pyHTMLParser.Parser import Parser
    
    parser = Parser()
    parser.open('http://www.example.com')
    links = parser.tag('a')
    for link in links:
        print(link.attr('href'))
    parser.close()

Documentation
-------------

`API Docs <http://ishibashijun.github.io/pyHTMLParser/>`_ .
"""

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Topic :: Internet :: WWW/HTTP',
    'Topic :: Text Processing :: Markup :: HTML'
]

setup(
    name = name,
    packages = ['pyHTMLParser'],
    version = version,
    description = short_description,
    long_description = long_description,
    classifiers = classifiers,
    license = 'MIT',
    keywords = ['parse', 'scrape', 'html',
                'parser', 'tree', 'DOM'],
    author = 'Jun Ishibashi',
    author_email = 'ishibashijun@gmail.com',
    url = 'http://ishibashijun.github.io/pyHTMLParser/'
)
