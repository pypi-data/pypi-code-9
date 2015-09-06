from setuptools import setup

version = '2.0.0'
name = 'pyHTMLParser'
short_description = 'A simple html parser that constructs DOM tree.'
long_description = """\
It is aimed to provide jquery like API.

Example
-------

.. code-block:: python

    from pyHTMLParser.Query import Q_open, Q_close, Q
    
    Q_open('http://www.example.com')
    
    second_target_link = Q('a[href$="-target.html"]:nth-child(2)')
    print(second_target_link.attr('href'))

    >>> some-target.html
    
    Q_close()

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
    keywords = ['parse', 'html', 'jquery', 'parser', 'tree', 'DOM'],
    author = 'Jun Ishibashi',
    author_email = 'ishibashijun@gmail.com',
    url = 'http://ishibashijun.github.io/pyHTMLParser/'
)
